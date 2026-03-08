import polars as pl
import time
import os


def run_senior_cleaning():
    print("🧹 Khởi động Pipeline Làm sạch dữ liệu (Chế độ Out-of-Core/Streaming)...")
    start_time = time.time()

    input_file = "amazon_appliances_100k.parquet"
    output_file = "amazon_appliances_cleaned.parquet"

    # 1. LAZY EVALUATION: Trì hoãn việc đọc dữ liệu vào RAM
    # Polars chỉ lập kế hoạch truy vấn chứ không tải toàn bộ file vào bộ nhớ
    q = pl.scan_parquet(input_file)

    # 2. XÂY DỰNG PIPELINE LÀM SẠCH TỐI ƯU CHO MÁY YẾU
    cleaned_q = (
        q
        # Bước 1: Loại bỏ rác cốt lõi
        # Không có user_id, parent_asin, hoặc rating thì không thể phân tích
        .drop_nulls(subset=["user_id", "parent_asin", "rating"])
        # Bước 2: Ép kiểu dữ liệu CỰC ĐOAN (Bí quyết tiết kiệm 70%+ RAM)
        .with_columns(
            [
                # Chuyển ID sang Categorical.
                # String chiếm rất nhiều RAM. Trong Big Data, user_id/item_id lặp lại liên tục.
                # Categorical sẽ lưu ID dạng số nguyên (integer) ngầm bên dưới.
                pl.col("user_id").cast(pl.Categorical),
                pl.col("parent_asin").cast(pl.Categorical),
                # Rating (1-5) chỉ cần Int8 (1 byte thay vì 8 bytes của Float64)
                pl.col("rating").cast(pl.Int8),
                # Chuẩn hoá timestamp (s hoặc ms tùy format, Amazon thường lưu ms)
                pl.from_epoch("timestamp", time_unit="ms").alias("datetime"),
                # Verified purchase đưa về Boolean chuẩn (1 bit)
                pl.col("verified_purchase").cast(pl.Boolean),
                # Xử lý Text: Dùng engine C++ native của Polars thay vì vòng lặp Python
                pl.col("text")
                .fill_null("")
                .str.to_lowercase()
                .str.replace_all(r"<[^>]*>", " ")  # Xóa HTML tags
                .str.replace_all(r"http\S+", ""),  # Xóa URLs
            ]
        )
        # Bước 3: Khử trùng lặp cực nhanh (Memory-efficient deduplication)
        # Tránh người dùng gửi 1 review 2 lần do lag mạng
        .unique(subset=["user_id", "parent_asin", "datetime"], keep="first")
        # Bước 4: Lọc bỏ review rác (quá ngắn < 3 ký tự như "ok", "a")
        .filter(pl.col("text").str.len_chars() >= 3)
    )

    # 3. THỰC THI CHẾ ĐỘ STREAMING XUỐNG ĐĨA (SINK_PARQUET)
    print("⚙️ Đang xử lý theo lô (Batches) và ghi thẳng xuống ổ cứng...")

    # Bắt buộc bật StringCache khi ép kiểu String sang Categorical trong Lazy API
    with pl.StringCache():
        # TỐI HẬU QUYẾT: Dùng sink_parquet() thay vì collect()
        # collect() sẽ nạp TẤT CẢ kết quả vào RAM rồi mới lưu. Máy yếu sẽ sập (OOM).
        # sink_parquet() sẽ xử lý và ghi xuống đĩa theo từng chunk nhỏ. RAM luôn ở mức thấp.
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
