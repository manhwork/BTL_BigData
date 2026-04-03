
import subprocess
import sys

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import gcsfs
import gc
import time
import os
import signal
import subprocess


def _build_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName('AmazonReviews_Silver_Pipeline')
        .config('spark.jars.packages',
                'com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5')
        .config('spark.hadoop.fs.gs.impl',
                'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
        .config('spark.hadoop.fs.AbstractFileSystem.gs.impl',
                'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS')
        .config('spark.hadoop.google.cloud.auth.service.account.enable', 'true')
        .config('spark.sql.caseSensitive', 'true')
        .config('spark.driver.memory',          '6g')
        .config('spark.executor.memory',        '6g')
        .config('spark.memory.offHeap.enabled', 'true')
        .config('spark.memory.offHeap.size',    '2g')
        .config('spark.driver.maxResultSize',   '2g')
        .config('spark.sql.shuffle.partitions', '20')
        .config("spark.rapids.sql.concurrentGpuTasks", "2") # Cho phép 2 task GPU chạy song song
        .config("spark.driver.memory", "12g")              # Tăng RAM driver để gánh 2 luồng
        .config("spark.executor.memory", "12g")
        .getOrCreate()
    )


# Initialize Spark session
spark = _build_spark()
spark.sparkContext.setLogLevel('ERROR')
print(f'SparkSession khởi tạo thành công! (version {spark.version})')



def _force_kill_java() -> None:
    """Tìm và kill tất cả process 'java' đang chạy."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'pyspark'],
            capture_output=True, text=True
        )
        pids = [int(p) for p in result.stdout.strip().split() if p.isdigit()]
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if pids:
            print(f' Đã kill {len(pids)} JVM process: {pids}')
    except BaseException:
        pass


def restart_spark(wait: int = 12) -> None:

    global spark
    print(f'Đang restart SparkSession (chờ {wait}s)...')

    try:
        spark.stop()
    except BaseException:
        pass

    _force_kill_java()

    time.sleep(wait)
    gc.collect()

    spark = _build_spark()
    spark.sparkContext.setLogLevel('ERROR')
    print('SparkSession đã được khởi động lại!')


def is_jvm_crash(exc: BaseException) -> bool:

    crash_types = {
        'ConnectionRefusedError',
        'BrokenPipeError',
        'Py4JNetworkError',
        'Py4JJavaError',
        'Py4JError',
    }
    crash_msgs = [
        'connection refused',
        'answer from java side is empty',
        'java gateway process exited',
        'broken pipe',
        'an error occurred while calling',
    ]
    type_name = type(exc).__name__
    msg       = str(exc).lower()

    return (
        type_name in crash_types
        or any(s in msg for s in crash_msgs)
    )


def spark_safe_clear_cache() -> None:
    try:
        spark.catalog.clearCache()
    except BaseException:  
        pass


def spark_safe_unpersist(df) -> None:
    try:
        if df is not None:
            df.unpersist()
    except BaseException:
        pass


print('restart_spark(), is_jvm_crash(), spark_safe_clear_cache() đã sẵn sàng.')


fs = gcsfs.GCSFileSystem()

BUCKET         = 'amazon-reviews-lakehouse-data'
bronze_base    = f'{BUCKET}/bronze-zone'
silver_base    = f'{BUCKET}/silver-zone'
NUM_PARTITIONS = 20   


def scan_folders(gcs_path: str) -> list:
    try:
        entries = fs.ls(gcs_path)
    except FileNotFoundError:
        print(f'Không tìm thấy: {gcs_path}')
        return []
    folders = [e.split('/')[-1] for e in entries if fs.isdir(e)]
    return [
        f for f in folders
        if f and not f.startswith('_') and not f.startswith('.')
    ]


meta_folders   = scan_folders(f'{bronze_base}/meta-data/')
review_folders = scan_folders(f'{bronze_base}/review-data/')

print(f'Meta   : {len(meta_folders):>3} danh mục — {meta_folders}')
print(f'Review : {len(review_folders):>3} danh mục — {review_folders}')


_JUNK = ('', 'null', 'NULL', 'N/A', 'n/a', 'None', 'none', 'NaN', 'nan')


def clean_string_columns(df):
    for col_name, dtype in df.dtypes:
        if dtype == 'string':
            df = df.withColumn(col_name, F.trim(F.col(col_name)))
            df = df.withColumn(
                col_name,
                F.when(F.col(col_name).isin(*_JUNK), F.lit(None))
                 .otherwise(F.col(col_name))
            )
    return df


def safe_cast(df, col_name: str, target_type: str):
    raw = F.trim(F.col(col_name).cast('string'))
    return df.withColumn(
        col_name,
        F.when(raw.isin(*_JUNK), F.lit(None))
         .otherwise(F.col(col_name))
         .cast(target_type)
    )


print('✅ clean_string_columns() và safe_cast() đã sẵn sàng.')



def process_review_silver(df, cat_name):
    df = df.withColumn("source_category", F.lit(cat_name))

    df = clean_string_columns(df)

    raw_ts = F.trim(F.col("timestamp_raw").cast("string"))
    df = df.withColumnRenamed("timestamp", "timestamp_raw") \
           .withColumn("timestamp", F.to_timestamp(F.when(raw_ts.isin("", "null"), F.lit(None)).otherwise(F.col("timestamp_raw")) / 1000))

    raw_rating = F.trim(F.col("rating").cast("string"))
    df = df.withColumn("rating", F.when(raw_rating.isin("", "null"), F.lit(None)).otherwise(F.col("rating")).cast("byte"))

    raw_vp = F.trim(F.col("verified_purchase").cast("string"))
    df = df.withColumn("verified_purchase", F.when(raw_vp.isin("", "null"), F.lit(None)).otherwise(F.col("verified_purchase")).cast("boolean"))

    raw_hv = F.trim(F.col("helpful_vote").cast("string"))
    df = df.withColumn("helpful_vote", F.when(raw_hv.isin("", "null"), F.lit(None)).otherwise(F.col("helpful_vote")).cast("int"))

    review_drop_cols = ["user_id", "parent_asin", "rating", "timestamp", "verified_purchase", "helpful_vote"]
    df = df.dropna(subset=[c for c in review_drop_cols if c in df.columns])

    df = df.withColumn("text", F.regexp_replace(F.col("text").cast("string"), r"<[^>]*>", " ")) \
           .withColumn("text", F.regexp_replace(F.col("text"), r"https?://\S+|www\.\S+", "")) \
           .withColumn("text", F.regexp_replace(F.col("text"), r"[^a-zA-Z0-9\s]", "")) \
           .withColumn("text", F.trim(F.regexp_replace(F.col("text"), r"\s+", " ")))

    window_dedup = Window.partitionBy("user_id", "parent_asin", "timestamp_raw").orderBy(F.col("helpful_vote").desc_nulls_last())
    df = df.withColumn("rn", F.row_number().over(window_dedup)).filter(F.col("rn") == 1).drop("rn")

    df = df.withColumn("processed_at", F.current_timestamp())
    core_columns = ["user_id", "parent_asin", "rating", "text", "timestamp", "timestamp_raw", "verified_purchase", "helpful_vote", "source_category", "processed_at"]
    return df.select(*[c for c in core_columns if c in df.columns])


def process_meta_silver(df, cat_name):
    df = df.withColumn("source_category", F.lit(cat_name))

    df = clean_string_columns(df)

    meta_drop_cols = ["parent_asin"]

    if "average_rating" in df.columns:
        is_empty_rating = F.trim(F.col("average_rating").cast("string")).isin("", "null", "N/A")
        df = df.withColumn("average_rating",
                           F.when(is_empty_rating, F.lit(None)).otherwise(F.col("average_rating")).cast("float"))

    if "rating_number" in df.columns:
        is_empty_num = F.trim(F.col("rating_number").cast("string")).isin("", "null", "N/A")
        df = df.withColumn("rating_number",
                           F.when(is_empty_num, F.lit(None)).otherwise(F.col("rating_number")).cast("int"))

    if "price" in df.columns:
        str_price = F.col("price").cast("string")
        extracted_price = F.regexp_extract(str_price, r"(\d+\.\d+|\d+)", 1)
        df = df.withColumn("price",
                           F.when(extracted_price == "", F.lit(None)).otherwise(extracted_price).cast("float"))

    df = df.dropna(subset=meta_drop_cols)

    array_cols = ["categories", "features", "description"]
    for c in array_cols:
        if c in df.columns:
            df = df.withColumn(c, F.when(F.col(c).isNull(), F.array()).otherwise(F.col(c)))

    window_meta = Window.partitionBy("parent_asin").orderBy(F.col("parent_asin"))
    df = df.withColumn("rn", F.row_number().over(window_meta)).filter(F.col("rn") == 1).drop("rn")

    df = df.withColumn("processed_at", F.current_timestamp())
    return df


def execute_silver_pipeline_safe(categories, sub_folder, data_type, max_retry=1):
    prefix = f"[{sub_folder.upper()}]"
    print(f"\n==============================================================")
    print(f"🚀 ETL BẮT ĐẦU: {sub_folder}  ({len(categories)} danh mục)")
    print(f"==============================================================")

    result = {"success": 0, "skipped": 0, "failed": []}

    for idx, cat in enumerate(categories, 1):
        source_path = f"gs://{bronze_base}/{sub_folder}/{cat}/*.parquet"
        target_path = f"gs://{silver_base}/{sub_folder}/{cat}"

        # Bỏ qua nếu đã làm xong
        if fs.exists(f"{target_path}/_SUCCESS"):
            print(f"  ⏩ [{idx:02d}/{len(categories)}] {cat} — Bỏ qua (đã có _SUCCESS)")
            result["skipped"] += 1
            continue

        print(f"⏳ [{idx:02d}/{len(categories)}] {cat} — Đang xử lý...")
        attempt = 0

        while attempt <= max_retry:
            df_bronze = None
            df_silver = None

            try:
                df_bronze = spark.read.parquet(source_path)
                df_bronze = df_bronze.repartition(10)

                if data_type == "Review":
                    df_silver = process_review_silver(df_bronze, cat)
                else:
                    df_silver = process_meta_silver(df_bronze, cat)

                df_silver.write.mode("overwrite")\
                    .option("compression", "gzip") \
                    .parquet(target_path)
                count_out = spark.read.parquet(target_path).count()

                print(f"  ✅ Thành công: {cat} | Đầu ra: {count_out:,} hàng")
                result["success"] += 1
                break

            except BaseException as exc:
                last_err = str(exc).split('\n')[0][:250]

                if is_jvm_crash(exc) and attempt < max_retry:
                    attempt += 1
                    print(f"  💥 JVM crash tại {cat} (Thử lại {attempt}/{max_retry}) — Đang restart Spark...")
                    restart_spark(wait=12)
                    continue
                else:
                    print(f"  ❌ LỖI tại {cat}: {last_err}")
                    result["failed"].append(cat)
                    break

            finally:
                if df_bronze is not None:
                    try: df_bronze.unpersist()
                    except: pass
                if df_silver is not None:
                    try: df_silver.unpersist()
                    except: pass
                try: spark.catalog.clearCache()
                except: pass
                gc.collect()

    return result

if __name__ == "__main__":
    print('\n' + '#'*62)
    print('#  AMAZON REVIEWS — BRONZE → SILVER PIPELINE')
    print('#'*62)

    meta_result = execute_silver_pipeline_safe(
        meta_folders, 'meta-data', 'Meta', max_retry=1
    )

    review_result = execute_silver_pipeline_safe(
        review_folders, 'review-data', 'Review', max_retry=1
    )

    # Tổng hợp
    total_ok   = meta_result['success'] + review_result['success']
    total_skip = meta_result['skipped'] + review_result['skipped']
    total_fail = len(meta_result['failed']) + len(review_result['failed'])

    print('\n' + '#'*62)
    print('#  KẾT QUẢ TỔNG HỢP')
    print('#'*62)
    print(f' Tổng thành công : {total_ok}')
    print(f' Tổng bỏ qua    : {total_skip}')
    print(f' Tổng lỗi       : {total_fail}')

    if total_fail == 0:
        print('\n Pipeline hoàn thành KHÔNG lỗi!')
    else:
        all_failed = meta_result['failed'] + review_result['failed']
        print(f'\n  {total_fail} danh mục cần chạy lại:')
        for name in all_failed:
            print(f'   • {name}')