# Tài liệu Kỹ thuật: Quy trình Data Engineering cho Big Data (Giai đoạn 1 & 2)

Tài liệu này giải thích chi tiết các quyết định kiến trúc, phương pháp và kỹ thuật được áp dụng trong Giai đoạn 1 (Thu thập dữ liệu) và Giai đoạn 2 (Tiền xử lý) của dự án phân tích bộ dữ liệu Amazon Reviews 2023. Các phương pháp này được thiết kế theo chuẩn công nghiệp (Production-ready) nhằm giải quyết bài toán cốt lõi: **Xử lý khối lượng dữ liệu khổng lồ (hàng trăm GB) trên các máy tính có cấu hình giới hạn (RAM yếu) mà không bị tràn bộ nhớ (Out-Of-Memory - OOM).**

---

## Giai đoạn 1: Thu thập & Thiết lập hạ tầng (Data Ingestion)

**Mục tiêu:** Rút trích dữ liệu từ Cloud (Hugging Face) về máy tính cá nhân một cách an toàn, không làm treo máy và tối ưu hóa dung lượng lưu trữ cục bộ.

### 1. Phương pháp Data Streaming (IterableDataset)
Thay vì tải toàn bộ file nén hàng trăm GB về ổ cứng rồi nạp vào RAM (cách làm phổ thông nhưng dễ gây sập hệ thống), chúng ta sử dụng kỹ thuật **Streaming**:
*   **Cách hoạt động:** Mở một "đường ống" kết nối trực tiếp đến máy chủ của Hugging Face (`streaming=True`). Dữ liệu được tải về bộ nhớ tạm theo từng gói nhỏ (chunk/batch).
*   **Lợi ích:** Tiêu thụ cực kỳ ít RAM (chỉ khoảng vài chục MB tại một thời điểm). Hệ thống đọc xong dòng nào, xử lý dòng đó rồi lập tức giải phóng bộ nhớ.

### 2. Kỹ thuật Schema Projection (Lọc cột ngay từ nguồn)
Dữ liệu thô của Amazon chứa rất nhiều trường thông tin nặng (ví dụ: `images`, `title`, biến thể sản phẩm). 
*   **Cách hoạt động:** Chỉ trích xuất đúng 7 cột mang "tín hiệu" phục vụ trực tiếp cho bài toán phân tích hành vi và độ tin cậy: `user_id`, `parent_asin`, `rating`, `text`, `timestamp`, `verified_purchase`, `helpful_vote`.
*   **Lợi ích:** Giảm thiểu 80% dung lượng băng thông mạng và dung lượng ổ cứng cần thiết.

### 3. Định dạng lưu trữ Parquet (Landing Zone)
*   **Lý do lựa chọn:** Không sử dụng định dạng `.csv` hay `.json`. Dữ liệu được ghi thẳng xuống ổ đĩa dưới định dạng `.parquet`.
*   **Ưu điểm:** Parquet là định dạng lưu trữ theo cột (columnar format) được nén rất chặt. Tốc độ đọc/ghi dữ liệu của Parquet nhanh hơn CSV gấp 10-20 lần và cực kỳ tối ưu cho các Engine xử lý phân tán như Polars hay Spark.

---

## Giai đoạn 2: Tiền xử lý & Làm sạch (Data Cleaning)

**Mục tiêu:** Làm sạch dữ liệu, loại bỏ nhiễu và chuẩn hóa định dạng với mục tiêu tối thượng là tiết kiệm RAM tối đa cho các bước chạy thuật toán Machine Learning ở giai đoạn sau. Công cụ được sử dụng là **Polars** (Engine viết bằng Rust) thay vì Pandas.

### 1. Kỹ thuật Out-of-Core Processing (Xử lý ngoài bộ nhớ)
Đây là kỹ thuật cốt lõi giúp máy tính RAM 8GB có thể xử lý mượt mà file dữ liệu 50GB.
*   **Lazy Evaluation (`scan_parquet`):** Thay vì nạp toàn bộ file vào RAM (`read_parquet`), Polars chỉ đọc cấu trúc siêu dữ liệu (metadata) và xây dựng một Kế hoạch thực thi (Execution Plan) tối ưu nhất (lọc trước, tính toán sau).
*   **Streaming xuống đĩa (`sink_parquet`):** Thay vì thu thập tất cả kết quả vào RAM rồi mới lưu file (`collect`), hệ thống sẽ thực thi quy trình làm sạch trên từng lô dữ liệu nhỏ (batch) và ghi đè trực tiếp kết quả xuống ổ cứng. RAM lúc nào cũng được giữ ở mức rất thấp.

### 2. Ép kiểu dữ liệu cực đoan (Aggressive Downcasting)
Việc sử dụng kiểu dữ liệu mặc định (`String` hoặc `Float64`) là nguyên nhân chính gây tràn RAM trong Big Data.
*   **Categorical Encoding cho Chuỗi (String):** Các cột ID (`user_id`, `parent_asin`) lặp lại hàng triệu lần. Nếu lưu dưới dạng String, nó sẽ chiếm bộ nhớ khổng lồ. Chúng ta ép sang kiểu `Categorical` (kết hợp `StringCache`). Polars sẽ ngầm tạo một cuốn từ điển (Dictionary) và lưu các ID này dưới dạng số nguyên (integer 32-bit), giúp tiết kiệm 50% - 70% bộ nhớ.
*   **Downcasting Số học:** Cột `rating` mặc định là `Float64` (8 bytes), chúng ta ép về `Int8` (1 byte) vì giá trị chỉ nằm từ 1 đến 5. Cột `verified_purchase` ép về `Boolean` (1 bit) thay vì chuỗi "True"/"False".

### 3. Native String Engine (Tối ưu hóa xử lý văn bản)
Khi làm sạch nội dung review (`text`), các Junior thường dùng hàm vòng lặp Python như `apply(lambda x: x.lower())`. Việc này gọi là tắc nghẽn GIL (Global Interpreter Lock), làm vô hiệu hóa tốc độ của thư viện đa luồng.
*   **Giải pháp:** Sử dụng hoàn toàn chuỗi hàm nội tại (Native methods) của Polars như `.str.replace_all()` và `.str.to_lowercase()`. Những hàm này gọi trực tiếp xuống các tập lệnh C++/Rust ở tầng thấp, chạy đa luồng trên tất cả các nhân CPU, mang lại tốc độ xử lý nhanh hơn hàng trăm lần.

### 4. Khử trùng lặp an toàn (Memory-efficient Deduplication)
*   Sử dụng hàm `.unique()` trên bộ ba khoá (Composite keys): `user_id`, `parent_asin`, và `datetime`. Nếu một người dùng gửi đánh giá 2 lần cho cùng một sản phẩm ở cùng một khoảnh khắc (do lag mạng), bản ghi thừa sẽ bị loại bỏ nhanh chóng thông qua thuật toán băm (hashing) ở cấp độ C++ mà không yêu cầu tải toàn bộ nhóm dữ liệu đó vào Python.

---
*Tài liệu này đóng vai trò nền tảng để giải thích tính "Production-ready" cho toàn bộ pipeline dữ liệu, sẵn sàng bảo vệ hướng tiếp cận trước bất kỳ hội đồng đánh giá (Senior/Architect) nào.*
