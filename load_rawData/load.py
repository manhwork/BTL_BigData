import os
import sys
import math
import shutil
from pathlib import Path
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from huggingface_hub import hf_hub_download

def get_credentials_location():
    """Get credentials location based on OS (Windows vs Linux)"""
    home = Path.home()
    if sys.platform == "win32":
        return home / "AppData" / "Roaming" / "gcloud" / "application_default_credentials.json"
    else:
        # Linux/Mac
        return home / ".config" / "gcloud" / "application_default_credentials.json"

def get_gcs_jar_path():
    """Get or locate GCS connector jar"""
    jar_filename = "gcs-connector-hadoop3-latest.jar"
    current_dir = Path(__file__).parent
    jar_path = current_dir / jar_filename
    
    if jar_path.exists():
        return str(jar_path)
    
    home = Path.home()
    jar_in_home = home / jar_filename
    if jar_in_home.exists():
        return str(jar_in_home)
    
    # Try temp location on VM
    if not sys.platform.startswith("win"):
        temp_jars = Path("/tmp") / jar_filename
        if temp_jars.exists():
            return str(temp_jars)
    
    return str(jar_path)  # Return expected path even if not found yet

def create_spark_session(driver_memory_gb=8, executor_memory_gb=8, reserve_cores=1):
    # Get paths dynamically (works on local Windows and VM Linux)
    credentials_location = str(get_credentials_location())
    gcs_jar_path = str(get_gcs_jar_path())

    if not Path(credentials_location).exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_location}\nRun: gcloud auth application-default login")

    if not Path(gcs_jar_path).exists():
        raise FileNotFoundError(f"GCS connector jar not found: {gcs_jar_path}")

    # Resource tuning for local Spark (change these numbers if needed).
    total_cores = os.cpu_count() or 4
    spark_cores = max(1, total_cores - reserve_cores)
    default_parallelism = max(8, spark_cores * 2)
    shuffle_partitions = max(16, spark_cores * 4)
    jar_classpath = gcs_jar_path

    # Recreate Spark context so new config is applied on rerun.
    active_sc = SparkContext._active_spark_context
    if active_sc is not None:
        active_sc.stop()

    conf = (
        SparkConf()
            .setMaster(f"local[{spark_cores}]")
            .setAppName("test")
            .set("spark.driver.memory", f"{driver_memory_gb}g")
            .set("spark.executor.memory", f"{executor_memory_gb}g")
            .set("spark.default.parallelism", str(default_parallelism))
            .set("spark.sql.shuffle.partitions", str(shuffle_partitions))
            # Use classpath instead of spark.jars to avoid Windows winutils/chmod issue.
            .set("spark.driver.extraClassPath", jar_classpath)
            .set("spark.executor.extraClassPath", jar_classpath)
            .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
    )

    sc = SparkContext(conf=conf)
    hadoop_conf = sc._jsc.hadoopConfiguration()

    hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
    hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)

    spark = SparkSession.builder \
        .config(conf=sc.getConf()) \
        .getOrCreate()
    spark.conf.set("spark.sql.caseSensitive", "true")
    print(f"Spark cores: {spark_cores}/{total_cores}")
    print(f"Driver memory: {driver_memory_gb}g, Executor memory: {executor_memory_gb}g")
    print(f"defaultParallelism={default_parallelism}, shufflePartitions={shuffle_partitions}")
    return spark,sc

def _estimate_output_files_from_json_size(
    json_file_path,
    target_parquet_file_mb=128,
    estimated_compression_ratio=0.30,
    min_files=1,
    max_files=200,
):
    """
    Estimate output parquet file count from source JSON size.

    estimated_parquet_size ~= json_size * estimated_compression_ratio
    output_files ~= estimated_parquet_size / target_parquet_file_mb
    """

    json_size_bytes = os.path.getsize(json_file_path)
    target_bytes = target_parquet_file_mb * 1024 * 1024

    estimated_parquet_bytes = max(1, int(json_size_bytes * estimated_compression_ratio))
    estimated_files = math.ceil(estimated_parquet_bytes / target_bytes)

    output_files = max(min_files, min(max_files, estimated_files))
    return output_files, json_size_bytes, estimated_parquet_bytes

def _gcs_path_exists(gcs_path,sc):
    path = sc._jvm.org.apache.hadoop.fs.Path(gcs_path)
    fs = path.getFileSystem(sc._jsc.hadoopConfiguration())
    return fs.exists(path)

def clear_huggingface_cache():
    """Remove Hugging Face Hub cache folders to free disk space."""
    default_hf_home = Path.home() / ".cache" / "huggingface"
    hf_home = Path(os.environ.get("HF_HOME", str(default_hf_home)))

    default_hub_cache = hf_home / "hub"
    hub_cache = Path(os.environ.get("HUGGINGFACE_HUB_CACHE", str(default_hub_cache)))

    # Also check Windows default cache path if custom env vars are not set.
    candidate_paths = {hub_cache}
    if sys.platform == "win32":
        candidate_paths.add(Path.home() / "AppData" / "Local" / "huggingface" / "hub")

    removed_any = False
    for cache_path in candidate_paths:
        if cache_path.exists():
            shutil.rmtree(cache_path)
            print(f"Removed Hugging Face cache: {cache_path}")
            removed_any = True

    if not removed_any:
        print("No Hugging Face cache folder found to remove.")

def upload_meta_data(
    spark,
    category,
    target_parquet_file_mb=128,
    estimated_compression_ratio=0.30,
    max_output_files=200,
    compression_codec="gzip",
    clear_hf_cache=False,
):
    repo_id = "McAuley-Lab/Amazon-Reviews-2023"
    file_in_repo = f"raw/meta_categories/meta_{category}.jsonl"
    bronze_output_path = f"gs://amazon-reviews-lakehouse-data/bronze-zone/meta-data/{category}"

    if _gcs_path_exists(bronze_output_path, spark.sparkContext):
        print(f"Skip metadata category '{category}': output already exists at {bronze_output_path}")
        return

    print(f"Uploading metadata for category: {category}")

    local_file_path = hf_hub_download(
        repo_id=repo_id,
        filename=file_in_repo,
        repo_type="dataset",
    )

    num_files, json_size_bytes, estimated_parquet_bytes = _estimate_output_files_from_json_size(
        json_file_path=local_file_path,
        target_parquet_file_mb=target_parquet_file_mb,
        estimated_compression_ratio=estimated_compression_ratio,
        min_files=1,
        max_files=max_output_files,
    )

    json_size_gb = json_size_bytes / (1024 ** 3)
    estimated_parquet_gb = estimated_parquet_bytes / (1024 ** 3)

    print(f"Source JSON size: {json_size_gb:.2f} GB")
    print(f"Estimated parquet size: {estimated_parquet_gb:.2f} GB")
    print(f"Target parquet file size: {target_parquet_file_mb} MB")
    print(f"Calculated output files: {num_files}")
    print(f"Compression codec: {compression_codec}")

    df = spark.read.option("multiLine", "false").json(local_file_path)

    current_partitions = df.rdd.getNumPartitions()
    if num_files >= current_partitions:
        df_to_write = df.repartition(num_files)
        partition_action = "repartition"
    else:
        df_to_write = df.coalesce(num_files)
        partition_action = "coalesce"

    print(f"Input partitions: {current_partitions}, using {partition_action} -> {num_files}")

    (
        df_to_write
        .write
        .mode("overwrite")
        .option("compression", compression_codec)
        .parquet(bronze_output_path)
    )

    print(f"Finished writing parquet to: {bronze_output_path}")
    if clear_hf_cache:
        clear_huggingface_cache()

def upload_review_data(
    spark,
    category,
    target_parquet_file_mb=128,
    estimated_compression_ratio=0.30,
    max_output_files=200,
    compression_codec="gzip",
    clear_hf_cache=False,
):
    repo_id = "McAuley-Lab/Amazon-Reviews-2023"
    file_in_repo = f"raw/review_categories/{category}.jsonl"
    bronze_output_path = f"gs://amazon-reviews-lakehouse-data/bronze-zone/review-data/{category}"

    if _gcs_path_exists(bronze_output_path, spark.sparkContext):
        print(f"Skip review category '{category}': output already exists at {bronze_output_path}")
        return

    print(f"Uploading review data for category: {category}")

    local_file_path = hf_hub_download(
        repo_id=repo_id,
        filename=file_in_repo,
        repo_type="dataset",
    )

    num_files, json_size_bytes, estimated_parquet_bytes = _estimate_output_files_from_json_size(
        json_file_path=local_file_path,
        target_parquet_file_mb=target_parquet_file_mb,
        estimated_compression_ratio=estimated_compression_ratio,
        min_files=1,
        max_files=max_output_files,
    )

    json_size_gb = json_size_bytes / (1024 ** 3)
    estimated_parquet_gb = estimated_parquet_bytes / (1024 ** 3)

    print(f"Source JSON size: {json_size_gb:.2f} GB")
    print(f"Estimated parquet size: {estimated_parquet_gb:.2f} GB")
    print(f"Target parquet file size: {target_parquet_file_mb} MB")
    print(f"Calculated output files: {num_files}")
    print(f"Compression codec: {compression_codec}")

    df = spark.read.option("multiLine", "false").json(local_file_path)

    current_partitions = df.rdd.getNumPartitions()
    if num_files >= current_partitions:
        df_to_write = df.repartition(num_files)
        partition_action = "repartition"
    else:
        df_to_write = df.coalesce(num_files)
        partition_action = "coalesce"

    print(f"Input partitions: {current_partitions}, using {partition_action} -> {num_files}")

    (
        df_to_write
        .write
        .mode("overwrite")
        .option("compression", compression_codec)
        .parquet(bronze_output_path)
    )

    print(f"Finished writing parquet to: {bronze_output_path}")
    if clear_hf_cache:
        clear_huggingface_cache()

if __name__ == "__main__":
    spark, _ = create_spark_session(driver_memory_gb=10, executor_memory_gb=10,reserve_cores=1)
    # tam thoi bo Automotive
    categories = [
    "All_Beauty", "Amazon_Fashion", "Appliances", "Arts_Crafts_and_Sewing",
    "Automotive","Books", "CDs_and_Vinyl", "Cell_Phones_and_Accessories",
    "Clothing_Shoes_and_Jewelry", "Digital_Music", "Electronics", "Gift_Cards",
    "Grocery_and_Gourmet_Food", "Health_and_Household", "Health_and_Personal_Care",
    "Home_and_Kitchen", "Industrial_and_Scientific", "Kindle_Store",
    "Magazine_Subscriptions", "Movies_and_TV", "Musical_Instruments",
    "Office_Products", "Patio_Lawn_and_Garden", "Pet_Supplies", "Software",
    "Sports_and_Outdoors", "Subscription_Boxes", "Tools_and_Home_Improvement",
    "Toys_and_Games", "Video_Games", "Unknown"
    ]
    
    for data_type in ["meta", "review"]:
        for category in categories:
            if data_type == "meta":
                upload_meta_data(spark, category, compression_codec="gzip",clear_hf_cache=True)
            else:
                upload_review_data(spark, category, compression_codec="gzip", clear_hf_cache=True)

