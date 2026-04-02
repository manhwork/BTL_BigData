import os
import sys
import math
import shutil
from pathlib import Path
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

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
            .setAppName("bronze-to-silver")
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
    return spark, sc

def _estimate_output_files_from_parquet_size(
    parquet_file_path,
    target_parquet_file_mb=128,
    min_files=1,
    max_files=200,
):
    """
    Estimate output parquet file count from source parquet size.
    
    output_files ~= source_parquet_size / target_parquet_file_mb
    """
    parquet_size_bytes = os.path.getsize(parquet_file_path)
    target_bytes = target_parquet_file_mb * 1024 * 1024

    estimated_files = math.ceil(parquet_size_bytes / target_bytes)
    output_files = max(min_files, min(max_files, estimated_files))
    return output_files, parquet_size_bytes

def _gcs_path_exists(gcs_path, sc):
    path = sc._jvm.org.apache.hadoop.fs.Path(gcs_path)
    fs = path.getFileSystem(sc._jsc.hadoopConfiguration())
    return fs.exists(path)

def apply_etl_transformations(df, category, data_type="review"):
    """
    Apply ETL transformations to dataframe.
    
    Parameters:
    -----------
    df : pyspark.sql.DataFrame
        Input dataframe from bronze zone
    category : str
        Product category name
    data_type : str
        Type of data: 'review' or 'metadata'
    
    Returns:
    --------
    pyspark.sql.DataFrame
        Transformed dataframe
    """
    # TODO: Implement ETL logic here
    # Examples:
    # - Data validation and cleaning
    # - Schema normalization
    # - NULL handling
    # - Data deduplication
    # - Type casting
    # - Adding processing timestamps
    
    print(f"Applying ETL transformations for {data_type} category: {category}")
    
    # Placeholder: return dataframe as-is until ETL logic is defined
    return df

def clean_review_data(
    spark,
    category,
    target_parquet_file_mb=128,
    max_output_files=200,
    compression_codec="gzip",
):
    """
    Load review data from bronze zone, apply ETL transformations, 
    and write to silver zone.
    
    Parameters:
    -----------
    spark : pyspark.sql.SparkSession
        Spark session
    category : str
        Product category name
    target_parquet_file_mb : int
        Target file size in MB for output partitions
    max_output_files : int
        Maximum number of output files
    compression_codec : str
        Compression codec for output files
    """
    bronze_input_path = f"gs://amazon-reviews-lakehouse-data/bronze-zone/review-data/{category}"
    silver_output_path = f"gs://amazon-reviews-lakehouse-data/silver-zone/review-data/{category}"

    if _gcs_path_exists(silver_output_path, spark.sparkContext):
        print(f"Skip review category '{category}': output already exists at {silver_output_path}")
        return

    print(f"Processing review data for category: {category}")

    # Check if bronze data exists
    if not _gcs_path_exists(bronze_input_path, spark.sparkContext):
        print(f"Bronze zone data not found at {bronze_input_path}")
        return

    # Read from bronze zone
    print(f"Reading from bronze zone: {bronze_input_path}")
    df = spark.read.parquet(bronze_input_path)
    
    print(f"Source partition count: {df.rdd.getNumPartitions()}")
    print(f"Source record count: {df.count()}")

    # Apply ETL transformations
    df_transformed = apply_etl_transformations(df, category, data_type="review")

    # Get input file size estimate for repartitioning
    # Read first parquet file to estimate size
    try:
        # This is a simple estimation; adjust based on actual use case
        num_files, parquet_size_bytes = _estimate_output_files_from_parquet_size(
            parquet_file_path=bronze_input_path,
            target_parquet_file_mb=target_parquet_file_mb,
            min_files=1,
            max_files=max_output_files,
        )
    except:
        # If size estimation fails, use record count to estimate
        num_files = max(1, min(max_output_files, df_transformed.rdd.getNumPartitions()))

    parquet_size_gb = parquet_size_bytes / (1024 ** 3) if 'parquet_size_bytes' in locals() else 0

    print(f"Estimated input parquet size: {parquet_size_gb:.2f} GB")
    print(f"Target parquet file size: {target_parquet_file_mb} MB")
    print(f"Calculated output files: {num_files}")
    print(f"Compression codec: {compression_codec}")

    # Repartition/coalesce for optimal file sizes
    current_partitions = df_transformed.rdd.getNumPartitions()
    if num_files >= current_partitions:
        df_to_write = df_transformed.repartition(num_files)
        partition_action = "repartition"
    else:
        df_to_write = df_transformed.coalesce(num_files)
        partition_action = "coalesce"

    print(f"Input partitions: {current_partitions}, using {partition_action} -> {num_files}")

    # Write to silver zone
    (
        df_to_write
        .write
        .mode("overwrite")
        .option("compression", compression_codec)
        .parquet(silver_output_path)
    )

    print(f"Finished writing cleaned review data to: {silver_output_path}")

def clean_metadata(
    spark,
    category,
    target_parquet_file_mb=128,
    max_output_files=200,
    compression_codec="gzip",
):
    """
    Load metadata from bronze zone, apply ETL transformations, 
    and write to silver zone.
    
    Parameters:
    -----------
    spark : pyspark.sql.SparkSession
        Spark session
    category : str
        Product category name
    target_parquet_file_mb : int
        Target file size in MB for output partitions
    max_output_files : int
        Maximum number of output files
    compression_codec : str
        Compression codec for output files
    """
    bronze_input_path = f"gs://amazon-reviews-lakehouse-data/bronze-zone/meta-data/{category}"
    silver_output_path = f"gs://amazon-reviews-lakehouse-data/silver-zone/meta-data/{category}"

    if _gcs_path_exists(silver_output_path, spark.sparkContext):
        print(f"Skip metadata category '{category}': output already exists at {silver_output_path}")
        return

    print(f"Processing metadata for category: {category}")

    # Check if bronze data exists
    if not _gcs_path_exists(bronze_input_path, spark.sparkContext):
        print(f"Bronze zone data not found at {bronze_input_path}")
        return

    # Read from bronze zone
    print(f"Reading from bronze zone: {bronze_input_path}")
    df = spark.read.parquet(bronze_input_path)
    
    print(f"Source partition count: {df.rdd.getNumPartitions()}")
    print(f"Source record count: {df.count()}")

    # Apply ETL transformations
    df_transformed = apply_etl_transformations(df, category, data_type="metadata")

    # Get input file size estimate for repartitioning
    try:
        num_files, parquet_size_bytes = _estimate_output_files_from_parquet_size(
            parquet_file_path=bronze_input_path,
            target_parquet_file_mb=target_parquet_file_mb,
            min_files=1,
            max_files=max_output_files,
        )
    except:
        num_files = max(1, min(max_output_files, df_transformed.rdd.getNumPartitions()))

    parquet_size_gb = parquet_size_bytes / (1024 ** 3) if 'parquet_size_bytes' in locals() else 0

    print(f"Estimated input parquet size: {parquet_size_gb:.2f} GB")
    print(f"Target parquet file size: {target_parquet_file_mb} MB")
    print(f"Calculated output files: {num_files}")
    print(f"Compression codec: {compression_codec}")

    # Repartition/coalesce for optimal file sizes
    current_partitions = df_transformed.rdd.getNumPartitions()
    if num_files >= current_partitions:
        df_to_write = df_transformed.repartition(num_files)
        partition_action = "repartition"
    else:
        df_to_write = df_transformed.coalesce(num_files)
        partition_action = "coalesce"

    print(f"Input partitions: {current_partitions}, using {partition_action} -> {num_files}")

    # Write to silver zone
    (
        df_to_write
        .write
        .mode("overwrite")
        .option("compression", compression_codec)
        .parquet(silver_output_path)
    )

    print(f"Finished writing cleaned metadata to: {silver_output_path}")

if __name__ == "__main__":
    # Example usage:
    # spark, sc = create_spark_session(driver_memory_gb=8, executor_memory_gb=8)
    # 
    # # Process review data
    # clean_review_data(spark, category="Electronics")
    # clean_review_data(spark, category="Books")
    # 
    # # Process metadata
    # clean_metadata(spark, category="Electronics")
    # clean_metadata(spark, category="Books")
    # 
    # sc.stop()
    pass
