import polars as pl
from datasets import load_dataset
import time

def run_ingestion():
    print("⏳ Bắt đầu kết nối tới Hugging Face...")
    start_time = time.time()
    
    dataset = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023", 
        "raw_review_Appliances", 
        split="full", 
        streaming=True,
        trust_remote_code=True
    )
    
    target_sample_size = 100000  # Lấy 100.000 dòng để test
    extracted_data = []
    
    print(f"📥 Đang stream và lọc {target_sample_size} dòng dữ liệu...")
    
    for i, row in enumerate(dataset):
        if i >= target_sample_size:
            break
            
        extracted_data.append({
            "user_id": row.get("user_id"),
            "parent_asin": row.get("parent_asin"),
            "rating": row.get("rating"),
            "text": row.get("text"),
            "timestamp": row.get("timestamp"),
            "verified_purchase": row.get("verified_purchase"),
            "helpful_vote": row.get("helpful_vote")
        })
        
        if (i + 1) % 20000 == 0:
            print(f"   Đã tải: {i + 1} / {target_sample_size} reviews...")

    print("⚙️ Đang chuyển đổi dữ liệu sang Polars DataFrame...")
    df = pl.DataFrame(extracted_data)
    
    output_filename = "amazon_appliances_100k.parquet"
    df.write_parquet(output_filename)
    
    end_time = time.time()
    print(f"✅ Hoàn tất! Đã lưu file '{output_filename}'.")
    print(f"⏱️ Tổng thời gian thực thi: {round(end_time - start_time, 2)} giây.")

if __name__ == "__main__":
    run_ingestion()