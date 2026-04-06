import polars as pl
import time
import os


def run_senior_cleaning():
    print("🧹 Khởi động Pipeline Làm sạch dữ liệu (Chế độ Out-of-Core/Streaming)...")
    start_time = time.time()

    input_file = "amazon_appliances_100k.parquet"
    output_file = "amazon_appliances_cleaned.parquet"

    q = pl.scan_parquet(input_file)

    cleaned_q = (
        q
        .drop_nulls(subset=["user_id", "parent_asin", "rating"])
        .with_columns(
            [
                pl.col("user_id").cast(pl.Categorical),
                pl.col("parent_asin").cast(pl.Categorical),
                pl.col("rating").cast(pl.Int8),
                pl.from_epoch("timestamp", time_unit="ms").alias("datetime"),
                pl.col("verified_purchase").cast(pl.Boolean),
                pl.col("text")
                .fill_null("")
                .str.to_lowercase()
                .str.replace_all(r"<[^>]*>", " ")  # Xóa HTML tags
                .str.replace_all(r"http\S+", ""),  # Xóa URLs
            ]
        )
        .unique(subset=["user_id", "parent_asin", "datetime"], keep="first")
        .filter(pl.col("text").str.len_chars() >= 3)
    )

    print("⚙️ Đang xử lý theo lô (Batches) và ghi thẳng xuống ổ cứng...")

    with pl.StringCache():
        cleaned_q.sink_parquet(output_file)

    end_time = time.time()

    # Thống kê dung lượng
    in_size = os.path.getsize(input_file) / (1024 * 1024)
    out_size = os.path.getsize(output_file) / (1024 * 1024)

    print(f"✅ Hoàn tất làm sạch!")
    print(f"📊 Dung lượng file gốc: {in_size:.2f} MB")
    print(
        f"📊 Dung lượng file sạch: {out_size:.2f} MB (Tiết kiệm được {(1 - out_size / in_size) * 100:.1f}%)"
    )
    print(f"⏱️ Tổng thời gian: {round(end_time - start_time, 2)} giây.")


if __name__ == "__main__":
    run_senior_cleaning()
