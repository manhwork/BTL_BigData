# NGHIỆP VỤ DỰ ÁN SO SÁNH GIÁ SẢN PHẨM GIỮA CÁC SÀN THƯƠNG MẠI ĐIỆN TỬ

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Mục tiêu dự án

Xây dựng hệ thống thu thập, phân tích và so sánh giá sản phẩm từ các sàn thương mại điện tử (TMĐT) phổ biến tại Việt Nam, đồng thời theo dõi biến động giá theo thời gian để hỗ trợ người dùng đưa ra quyết định mua hàng thông minh.

### 1.2. Phạm vi dự án

- **Các sàn TMĐT mục tiêu:**
    - Shopee
    - Lazada
    - Tiki
    - Sendo
    - TikTok Shop
    - Các sàn khác (mở rộng trong tương lai)

- **Chức năng chính:**
    - Thu thập dữ liệu sản phẩm và giá cả
    - So sánh giá giữa các sàn
    - Theo dõi lịch sử biến động giá
    - Phân tích xu hướng giá
    - Cảnh báo giá tốt
    - Báo cáo và thống kê

### 1.3. Đối tượng sử dụng

- Người tiêu dùng cá nhân
- Nhà bán hàng (nghiên cứu thị trường)
- Nhà phân tích thị trường
- Doanh nghiệp (định giá sản phẩm)

---

## 2. NGHIỆP VỤ CHI TIẾT

### 2.1. Thu thập dữ liệu sản phẩm (Data Crawling)

#### 2.1.1. Quy trình thu thập

```
[Định nghĩa sản phẩm cần crawl]
    ↓
[Xác định các sàn TMĐT nguồn]
    ↓
[Crawl dữ liệu từ các sàn]
    ↓
[Chuẩn hóa dữ liệu]
    ↓
[Lưu trữ vào database]
    ↓
[Lập lịch crawl định kỳ]
```

#### 2.1.2. Thông tin cần thu thập

**Thông tin cơ bản:**

- ID sản phẩm (trên từng sàn)
- Tên sản phẩm
- Mô tả sản phẩm
- Danh mục sản phẩm
- Thương hiệu
- Hình ảnh sản phẩm
- URL sản phẩm

**Thông tin giá cả:**

- Giá hiện tại
- Giá gốc (trước khuyến mãi)
- Phần trăm giảm giá
- Mã giảm giá (voucher/coupon)
- Giá sau khi áp dụng mã
- Phí vận chuyển
- Tổng giá cuối cùng

**Thông tin người bán:**

- Tên shop/người bán
- Địa chỉ shop
- Rating của shop
- Số lượng sản phẩm đã bán

**Thông tin đánh giá:**

- Số sao trung bình
- Số lượng đánh giá
- Số lượng đã bán
- Tỷ lệ đánh giá tích cực

**Metadata:**

- Thời gian thu thập
- Nguồn (sàn TMĐT)
- Trạng thái sản phẩm (còn hàng/hết hàng)
- Kho hàng còn lại

#### 2.1.3. Tần suất thu thập

- **Sản phẩm hot/trending:** Mỗi 1-2 giờ
- **Sản phẩm thông thường:** Mỗi 6-12 giờ
- **Sản phẩm ít biến động:** Mỗi 24 giờ
- **Đợt sale lớn (11/11, 12/12, Black Friday):** Mỗi 30 phút

#### 2.1.4. Xử lý dữ liệu

- **Chuẩn hóa tên sản phẩm:** Loại bỏ ký tự đặc biệt, viết hoa/thường
- **Mapping sản phẩm:** Nhận diện cùng một sản phẩm trên các sàn khác nhau
- **Làm sạch dữ liệu:** Loại bỏ dữ liệu trùng lặp, không hợp lệ
- **Phân loại:** Gán danh mục chuẩn cho sản phẩm

---

### 2.2. So sánh giá sản phẩm

#### 2.2.1. Quy trình so sánh

```
[Người dùng tìm kiếm sản phẩm]
    ↓
[Hệ thống tìm sản phẩm tương tự trên các sàn]
    ↓
[Chuẩn hóa và mapping sản phẩm]
    ↓
[Tính toán giá cuối cùng (bao gồm phí ship, giảm giá)]
    ↓
[Hiển thị bảng so sánh]
    ↓
[Đề xuất lựa chọn tốt nhất]
```

#### 2.2.2. Tiêu chí so sánh

**So sánh giá:**

- Giá gốc
- Giá sau giảm
- Phí vận chuyển
- Tổng giá cuối cùng
- Chênh lệch giá (%)

**So sánh chất lượng dịch vụ:**

- Rating sản phẩm
- Số lượng đánh giá
- Rating shop
- Số lượng đã bán
- Thời gian giao hàng dự kiến

**Điểm tổng hợp:**

- Tính điểm tổng hợp dựa trên: giá (50%), rating (25%), độ tin cậy shop (15%), số lượng bán (10%)
- Xếp hạng các lựa chọn

#### 2.2.3. Thuật toán matching sản phẩm

**Phương pháp nhận diện sản phẩm giống nhau:**

1. **Exact matching:** So sánh tên, mã sản phẩm chính xác
2. **Fuzzy matching:** Sử dụng thuật toán như:
    - Levenshtein distance
    - Cosine similarity
    - TF-IDF
3. **Image matching:** So sánh hình ảnh sản phẩm (Computer Vision)
4. **Attribute matching:** So sánh các thuộc tính (màu sắc, kích thước, thương hiệu)

**Ngưỡng matching:**

- Độ tương đồng >= 85%: Cùng sản phẩm
- Độ tương đồng 70-85%: Sản phẩm tương tự
- Độ tương đồng < 70%: Sản phẩm khác

#### 2.2.4. Giao diện so sánh

**Bảng so sánh hiển thị:**

- Hình ảnh sản phẩm
- Tên sản phẩm
- Tên sàn TMĐT
- Giá gốc (gạch ngang nếu có giảm)
- Giá hiện tại (highlight)
- % giảm giá
- Phí ship
- **Tổng giá cuối cùng (in đậm, màu nổi bật)**
- Rating (sao)
- Số đánh giá
- Số lượng đã bán
- Link đến sản phẩm
- Nút "Xem chi tiết" / "Mua ngay"

**Sắp xếp:**

- Theo giá thấp nhất
- Theo điểm tổng hợp cao nhất
- Theo rating cao nhất
- Theo số lượng bán nhiều nhất

---

### 2.3. Theo dõi biến động giá theo thời gian

#### 2.3.1. Quy trình lưu trữ lịch sử giá

```
[Thu thập giá định kỳ]
    ↓
[Kiểm tra thay đổi giá]
    ↓
[Nếu có thay đổi → Lưu vào bảng price_history]
    ↓
[Tính toán các chỉ số thống kê]
    ↓
[Cập nhật biểu đồ giá]
```

#### 2.3.2. Cấu trúc dữ liệu lịch sử giá

```
price_history:
  - product_id
  - platform (sàn TMĐT)
  - price (giá tại thời điểm)
  - original_price (giá gốc)
  - discount_percentage
  - shipping_fee
  - final_price (tổng giá cuối)
  - stock_status (còn hàng/hết hàng)
  - timestamp (thời gian ghi nhận)
  - event_tag (11/11, 12/12, Black Friday, v.v.)
```

#### 2.3.3. Phân tích biến động giá

**Các chỉ số thống kê:**

- Giá trung bình (7 ngày, 30 ngày, 90 ngày)
- Giá cao nhất trong khoảng thời gian
- Giá thấp nhất trong khoảng thời gian
- Độ lệch chuẩn (volatility)
- Xu hướng giá (tăng/giảm/ổn định)

**Phát hiện pattern:**

- **Flash sale:** Giá giảm mạnh trong thời gian ngắn
- **Seasonal pricing:** Giá thay đổi theo mùa
- **Event pricing:** Giá thay đổi trong các sự kiện lớn
- **Price manipulation:** Tăng giá gốc rồi giảm giá ảo

**Dự đoán giá:**

- Sử dụng Time Series Analysis (ARIMA, Prophet)
- Machine Learning (LSTM, Random Forest)
- Dự đoán giá trong 7-30 ngày tới

#### 2.3.4. Biểu đồ lịch sử giá

**Loại biểu đồ:**

- **Line chart:** Hiển thị xu hướng giá theo thời gian
- **Candlestick chart:** Hiển thị giá cao-thấp-mở-đóng theo ngày
- **Area chart:** So sánh giá giữa các sàn
- **Bar chart:** So sánh giá trung bình theo tháng

**Tính năng tương tác:**

- Zoom in/out theo khoảng thời gian
- Hover để xem chi tiết giá tại thời điểm
- Đánh dấu các sự kiện đặc biệt (sale, flash sale)
- So sánh nhiều sàn trên cùng biểu đồ
- Export biểu đồ (PNG, PDF)

**Khoảng thời gian:**

- 7 ngày gần nhất
- 30 ngày gần nhất
- 90 ngày gần nhất
- 6 tháng gần nhất
- 1 năm gần nhất
- Tùy chỉnh (custom range)

---

### 2.4. Cảnh báo giá tốt (Price Alert)

#### 2.4.1. Quy trình cảnh báo

```
[Người dùng đặt cảnh báo giá]
    ↓
[Hệ thống lưu điều kiện cảnh báo]
    ↓
[Kiểm tra giá định kỳ]
    ↓
[Nếu đạt điều kiện → Gửi thông báo]
    ↓
[Người dùng nhận thông báo]
```

#### 2.4.2. Loại cảnh báo

**Cảnh báo theo ngưỡng giá:**

- Giá giảm xuống dưới X VNĐ
- Giá giảm X% so với giá hiện tại
- Giá thấp hơn giá trung bình Y%

**Cảnh báo theo sự kiện:**

- Flash sale bắt đầu
- Voucher mới ra mắt
- Sản phẩm sắp hết hàng
- Giá tốt nhất trong 30 ngày

**Cảnh báo so sánh:**

- Giá trên sàn A rẻ hơn sàn B
- Chênh lệch giá giữa các sàn > X%

#### 2.4.3. Kênh thông báo

- **In-app notification:** Thông báo trong ứng dụng
- **Email:** Gửi email chi tiết
- **SMS:** Gửi tin nhắn (sản phẩm quan trọng)
- **Push notification:** Thông báo đẩy trên mobile
- **Telegram/Zalo bot:** Tích hợp bot

#### 2.4.4. Quản lý cảnh báo

- Tạo mới cảnh báo
- Chỉnh sửa điều kiện cảnh báo
- Tạm dừng/Kích hoạt cảnh báo
- Xóa cảnh báo
- Xem lịch sử cảnh báo đã nhận

---

### 2.5. Tìm kiếm và lọc sản phẩm

#### 2.5.1. Tìm kiếm

**Tìm kiếm cơ bản:**

- Tìm theo tên sản phẩm
- Tìm theo từ khóa
- Tìm theo mã sản phẩm

**Tìm kiếm nâng cao:**

- Tìm theo danh mục
- Tìm theo thương hiệu
- Tìm theo khoảng giá
- Tìm theo rating
- Tìm theo sàn TMĐT

**Tìm kiếm thông minh:**

- Auto-complete/Auto-suggest
- Gợi ý từ khóa liên quan
- Sửa lỗi chính tả
- Tìm kiếm bằng hình ảnh

#### 2.5.2. Bộ lọc (Filter)

**Lọc theo giá:**

- Dưới 100k
- 100k - 500k
- 500k - 1 triệu
- 1 triệu - 5 triệu
- Trên 5 triệu
- Tùy chỉnh khoảng giá

**Lọc theo sàn TMĐT:**

- Shopee
- Lazada
- Tiki
- Sendo
- TikTok Shop
- Chọn nhiều sàn

**Lọc theo đánh giá:**

- 5 sao
- 4 sao trở lên
- 3 sao trở lên

**Lọc theo trạng thái:**

- Đang giảm giá
- Miễn phí vận chuyển
- Còn hàng
- Flash sale
- Có voucher

**Lọc theo xu hướng giá:**

- Giá đang giảm
- Giá đang tăng
- Giá ổn định
- Giá tốt nhất trong 30 ngày

#### 2.5.3. Sắp xếp (Sort)

- Giá thấp đến cao
- Giá cao đến thấp
- Phổ biến nhất (số lượng bán)
- Đánh giá cao nhất
- Mới nhất
- Giảm giá nhiều nhất
- Điểm tổng hợp cao nhất

---

### 2.6. Báo cáo và Thống kê

#### 2.6.1. Báo cáo cho người dùng

**Dashboard cá nhân:**

- Sản phẩm đang theo dõi
- Lịch sử tìm kiếm
- Cảnh báo giá đã nhận
- Sản phẩm đã xem
- Xu hướng giá sản phẩm quan tâm

**Báo cáo tiết kiệm:**

- Tổng số tiền tiết kiệm được (nếu mua theo gợi ý)
- Số lần nhận cảnh báo giá tốt
- Sản phẩm tiết kiệm nhiều nhất

#### 2.6.2. Báo cáo thị trường

**Phân tích danh mục:**

- Top sản phẩm bán chạy theo danh mục
- Xu hướng giá theo danh mục
- Sàn TMĐT có giá tốt nhất theo danh mục

**Phân tích sàn TMĐT:**

- So sánh giá trung bình giữa các sàn
- Tần suất sale/khuyến mãi
- Độ tin cậy (rating trung bình)
- Thị phần theo danh mục

**Phân tích xu hướng:**

- Sản phẩm đang trending
- Danh mục đang hot
- Thời điểm sale tốt nhất
- Dự đoán xu hướng giá

#### 2.6.3. Báo cáo cho admin

**Thống kê hệ thống:**

- Số lượng sản phẩm đang theo dõi
- Số lượng người dùng
- Số lần tìm kiếm/ngày
- Số cảnh báo gửi đi/ngày
- Tỷ lệ thành công crawl data

**Hiệu suất:**

- Thời gian phản hồi trung bình
- Tỷ lệ uptime
- Số lỗi crawl
- Dung lượng database

---

## 3. KIẾN TRÚC HỆ THỐNG

### 3.1. Kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│  (Web App / Mobile App / Browser Extension)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   API GATEWAY                            │
│          (Authentication, Rate Limiting)                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────────┐
│   Search &   │ │  Price  │ │   Alert     │
│   Compare    │ │ History │ │   Service   │
│   Service    │ │ Service │ │             │
└───────┬──────┘ └──┬──────┘ └──┬──────────┘
        │           │            │
        └───────────┼────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│              DATA PROCESSING LAYER                       │
│  (Normalization, Matching, Analytics)                    │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                 DATA STORAGE                             │
│  (PostgreSQL/MongoDB + Redis Cache + S3/MinIO)          │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│              CRAWLING LAYER                              │
│  (Scrapy/Selenium + Proxy + Queue)                       │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────▼──────┐ ┌─▼──────┐ ┌─▼──────┐
│   Shopee     │ │ Lazada │ │  Tiki  │ ...
│   Crawler    │ │Crawler │ │Crawler │
└──────────────┘ └────────┘ └────────┘
```

### 3.2. Tech Stack đề xuất

#### 3.2.1. Backend

- **Framework:** Node.js (NestJS) hoặc Python (FastAPI/Django)
- **Database:**
    - PostgreSQL (dữ liệu quan hệ, lịch sử giá)
    - MongoDB (dữ liệu sản phẩm, metadata)
    - Redis (cache, session, queue)
- **Message Queue:** RabbitMQ hoặc Apache Kafka
- **Search Engine:** Elasticsearch
- **Storage:** MinIO hoặc AWS S3 (lưu hình ảnh)

#### 3.2.2. Crawling

- **Framework:** Scrapy, Selenium, Puppeteer
- **Proxy:** Rotating proxy để tránh bị block
- **Anti-bot:** Stealth plugins, user-agent rotation
- **Scheduler:** Apache Airflow hoặc Celery

#### 3.2.3. Frontend

- **Web:** React.js/Next.js hoặc Vue.js/Nuxt.js
- **Mobile:** React Native hoặc Flutter
- **Charting:** Chart.js, D3.js, ApexCharts
- **UI Framework:** Material-UI, Ant Design, Tailwind CSS

#### 3.2.4. Data Processing & Analytics

- **ETL:** Apache Spark, Pandas
- **Machine Learning:** TensorFlow, PyTorch, Scikit-learn
- **Time Series:** Prophet, ARIMA
- **Image Processing:** OpenCV, TensorFlow

#### 3.2.5. DevOps

- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes
- **CI/CD:** GitLab CI/CD, GitHub Actions
- **Monitoring:** Prometheus, Grafana, ELK Stack
- **Cloud:** AWS, GCP, hoặc Azure

---

## 4. LUỒNG DỮ LIỆU (DATA FLOW)

### 4.1. Luồng thu thập dữ liệu

```
1. Scheduler kích hoạt job crawl
2. Job được đưa vào queue (RabbitMQ/Kafka)
3. Worker lấy job từ queue
4. Worker crawl dữ liệu từ sàn TMĐT
5. Dữ liệu thô được lưu vào staging area
6. Data processing pipeline xử lý:
   - Làm sạch dữ liệu
   - Chuẩn hóa format
   - Matching sản phẩm
   - Extract features
7. Lưu vào database chính
8. Cập nhật search index (Elasticsearch)
9. Kiểm tra điều kiện cảnh báo
10. Gửi notification nếu cần
```

### 4.2. Luồng tìm kiếm và so sánh

```
1. User nhập từ khóa tìm kiếm
2. API Gateway nhận request
3. Kiểm tra cache (Redis)
4. Nếu không có cache:
   - Query Elasticsearch
   - Lấy dữ liệu từ database
   - Tính toán điểm so sánh
   - Lưu vào cache
5. Trả kết quả về frontend
6. Frontend render bảng so sánh
```

### 4.3. Luồng theo dõi giá

```
1. Mỗi lần crawl, so sánh giá mới với giá cũ
2. Nếu có thay đổi:
   - Insert record mới vào price_history
   - Tính toán các chỉ số thống kê
   - Cập nhật cache
   - Kiểm tra điều kiện alert
3. User xem lịch sử giá:
   - Query price_history theo product_id
   - Aggregate data theo khoảng thời gian
   - Generate chart data
   - Trả về frontend
```

---

## 5. CƠ SỞ DỮ LIỆU (DATABASE SCHEMA)

### 5.1. Bảng Products (Sản phẩm)

```sql
products:
  - id (PK)
  - name
  - normalized_name (tên đã chuẩn hóa)
  - description
  - category_id (FK)
  - brand
  - attributes (JSON: màu sắc, kích thước, v.v.)
  - image_urls (array)
  - created_at
  - updated_at
```

### 5.2. Bảng Product_Listings (Sản phẩm trên từng sàn)

```sql
product_listings:
  - id (PK)
  - product_id (FK) - liên kết đến products
  - platform (shopee, lazada, tiki, v.v.)
  - platform_product_id (ID trên sàn đó)
  - url
  - seller_name
  - seller_rating
  - current_price
  - original_price
  - discount_percentage
  - shipping_fee
  - stock_quantity
  - rating
  - review_count
  - sold_count
  - is_available
  - last_crawled_at
  - created_at
  - updated_at
```

### 5.3. Bảng Price_History (Lịch sử giá)

```sql
price_history:
  - id (PK)
  - product_listing_id (FK)
  - price
  - original_price
  - discount_percentage
  - shipping_fee
  - final_price
  - stock_status
  - event_tag (sale event nếu có)
  - recorded_at (timestamp)
```

### 5.4. Bảng Categories (Danh mục)

```sql
categories:
  - id (PK)
  - name
  - parent_id (FK, self-reference)
  - level
  - created_at
```

### 5.5. Bảng Users (Người dùng)

```sql
users:
  - id (PK)
  - email
  - password_hash
  - full_name
  - phone
  - preferences (JSON)
  - created_at
  - updated_at
```

### 5.6. Bảng Price_Alerts (Cảnh báo giá)

```sql
price_alerts:
  - id (PK)
  - user_id (FK)
  - product_id (FK)
  - alert_type (price_drop, percentage_drop, best_price, v.v.)
  - target_price (giá mục tiêu)
  - target_percentage (% giảm mục tiêu)
  - platforms (array: các sàn cần theo dõi)
  - is_active
  - notification_channels (email, sms, push, v.v.)
  - created_at
  - updated_at
```

### 5.7. Bảng Alert_History (Lịch sử cảnh báo)

```sql
alert_history:
  - id (PK)
  - alert_id (FK)
  - product_listing_id (FK)
  - triggered_price
  - message
  - sent_at
```

### 5.8. Bảng User_Watchlist (Danh sách theo dõi)

```sql
user_watchlist:
  - id (PK)
  - user_id (FK)
  - product_id (FK)
  - added_at
```

### 5.9. Bảng Search_History (Lịch sử tìm kiếm)

```sql
search_history:
  - id (PK)
  - user_id (FK, nullable)
  - search_query
  - filters (JSON)
  - result_count
  - searched_at
```

---

## 6. API ENDPOINTS

### 6.1. Product APIs

```
GET    /api/products                    - Lấy danh sách sản phẩm
GET    /api/products/:id                - Lấy chi tiết sản phẩm
GET    /api/products/search             - Tìm kiếm sản phẩm
GET    /api/products/:id/compare        - So sánh giá sản phẩm
GET    /api/products/:id/price-history  - Lịch sử giá sản phẩm
GET    /api/products/trending           - Sản phẩm trending
```

### 6.2. Price Alert APIs

```
POST   /api/alerts                      - Tạo cảnh báo giá
GET    /api/alerts                      - Lấy danh sách cảnh báo
GET    /api/alerts/:id                  - Chi tiết cảnh báo
PUT    /api/alerts/:id                  - Cập nhật cảnh báo
DELETE /api/alerts/:id                  - Xóa cảnh báo
GET    /api/alerts/:id/history          - Lịch sử cảnh báo
```

### 6.3. User APIs

```
POST   /api/auth/register               - Đăng ký
POST   /api/auth/login                  - Đăng nhập
POST   /api/auth/logout                 - Đăng xuất
GET    /api/users/profile               - Thông tin user
PUT    /api/users/profile               - Cập nhật profile
GET    /api/users/watchlist             - Danh sách theo dõi
POST   /api/users/watchlist             - Thêm vào watchlist
DELETE /api/users/watchlist/:id         - Xóa khỏi watchlist
```

### 6.4. Analytics APIs

```
GET    /api/analytics/price-trends      - Xu hướng giá
GET    /api/analytics/platform-compare  - So sánh các sàn
GET    /api/analytics/category-stats    - Thống kê theo danh mục
GET    /api/analytics/best-deals        - Deals tốt nhất
```

### 6.5. Category APIs

```
GET    /api/categories                  - Danh sách danh mục
GET    /api/categories/:id              - Chi tiết danh mục
GET    /api/categories/:id/products     - Sản phẩm theo danh mục
```

---

## 7. TÍNH NĂNG NÂNG CAO

### 7.1. Machine Learning & AI

**Recommendation System:**

- Gợi ý sản phẩm tương tự
- Gợi ý dựa trên lịch sử tìm kiếm
- Collaborative filtering

**Price Prediction:**

- Dự đoán giá trong tương lai
- Dự đoán thời điểm sale
- Phát hiện giá ảo

**Image Recognition:**

- Tìm kiếm bằng hình ảnh
- So sánh hình ảnh sản phẩm
- Phát hiện sản phẩm giả

### 7.2. Browser Extension

- Hiển thị lịch sử giá ngay trên trang sản phẩm
- So sánh giá với các sàn khác
- Cảnh báo giá tốt
- Tự động áp dụng mã giảm giá

### 7.3. Mobile App

- Push notification real-time
- Scan barcode để tìm kiếm
- Chụp ảnh để tìm sản phẩm
- Offline mode (cache dữ liệu)

### 7.4. Social Features

- Chia sẻ deals tốt
- Comment và đánh giá
- Follow người dùng khác
- Leaderboard (người tiết kiệm nhiều nhất)

### 7.5. Gamification

- Điểm thưởng khi tìm được deal tốt
- Badge và achievement
- Referral program
- Daily check-in

---

## 8. THÁCH THỨC VÀ GIẢI PHÁP

### 8.1. Thách thức kỹ thuật

#### 8.1.1. Anti-Crawling

**Vấn đề:**

- Các sàn TMĐT có cơ chế chống crawl (CAPTCHA, rate limiting, IP blocking)

**Giải pháp:**

- Sử dụng rotating proxy
- User-agent rotation
- Headless browser với stealth mode
- Distributed crawling
- Respect robots.txt và rate limiting
- Sử dụng API chính thức nếu có

#### 8.1.2. Data Matching

**Vấn đề:**

- Khó khăn trong việc nhận diện cùng một sản phẩm trên các sàn khác nhau

**Giải pháp:**

- Kết hợp nhiều phương pháp matching
- Machine Learning model cho matching
- Manual verification cho sản phẩm phổ biến
- Crowdsourcing (người dùng xác nhận)

#### 8.1.3. Scalability

**Vấn đề:**

- Lượng dữ liệu lớn (hàng triệu sản phẩm, hàng tỷ records giá)

**Giải pháp:**

- Database sharding
- Horizontal scaling
- Caching strategy (Redis)
- CDN cho static assets
- Async processing
- Data archiving (lưu trữ dữ liệu cũ)

#### 8.1.4. Real-time Processing

**Vấn đề:**

- Xử lý real-time cho flash sale, cảnh báo giá

**Giải pháp:**

- Message queue (Kafka/RabbitMQ)
- WebSocket cho real-time notification
- Stream processing (Apache Flink/Kafka Streams)
- Event-driven architecture

### 8.2. Thách thức pháp lý

#### 8.2.1. Bản quyền dữ liệu

**Vấn đề:**

- Crawl dữ liệu có thể vi phạm Terms of Service

**Giải pháp:**

- Sử dụng API chính thức khi có
- Chỉ crawl dữ liệu công khai
- Tuân thủ robots.txt
- Tham khảo luật pháp về web scraping
- Có disclaimer rõ ràng

#### 8.2.2. Bảo mật thông tin người dùng

**Vấn đề:**

- Lưu trữ thông tin cá nhân, lịch sử tìm kiếm

**Giải pháp:**

- Tuân thủ GDPR, PDPA
- Mã hóa dữ liệu nhạy cảm
- Cho phép user xóa dữ liệu
- Privacy policy rõ ràng
- Two-factor authentication

---

## 9. ROADMAP PHÁT TRIỂN

### Phase 1: MVP (2-3 tháng)

- [ ] Crawl dữ liệu từ 2-3 sàn chính (Shopee, Lazada, Tiki)
- [ ] Database schema cơ bản
- [ ] API cơ bản (search, compare)
- [ ] Web UI đơn giản
- [ ] Lưu lịch sử giá
- [ ] Hiển thị biểu đồ giá cơ bản

### Phase 2: Core Features (2-3 tháng)

- [ ] Mở rộng thêm sàn TMĐT
- [ ] Tính năng price alert
- [ ] Email notification
- [ ] User authentication
- [ ] Watchlist
- [ ] Cải thiện thuật toán matching
- [ ] Advanced search & filter

### Phase 3: Advanced Features (3-4 tháng)

- [ ] Mobile app (iOS/Android)
- [ ] Browser extension
- [ ] Push notification
- [ ] Price prediction
- [ ] Recommendation system
- [ ] Analytics dashboard
- [ ] Admin panel

### Phase 4: Scale & Optimize (2-3 tháng)

- [ ] Performance optimization
- [ ] Scalability improvements
- [ ] Machine Learning models
- [ ] Image search
- [ ] Social features
- [ ] Gamification

### Phase 5: Monetization (ongoing)

- [ ] Affiliate marketing
- [ ] Premium features
- [ ] API for businesses
- [ ] Advertisement
- [ ] White-label solution

---

## 10. MONETIZATION STRATEGY

### 10.1. Affiliate Marketing

- Tích hợp affiliate links từ các sàn TMĐT
- Hoa hồng khi user mua hàng qua link
- Ước tính: 2-5% giá trị đơn hàng

### 10.2. Premium Subscription

**Free tier:**

- Theo dõi tối đa 10 sản phẩm
- 5 price alerts
- Lịch sử giá 30 ngày
- Ads

**Premium tier (99k/tháng):**

- Theo dõi không giới hạn
- Unlimited alerts
- Lịch sử giá 1 năm
- No ads
- Priority notification
- Advanced analytics
- Export data

**Business tier (499k/tháng):**

- API access
- Bulk monitoring
- Custom reports
- Dedicated support

### 10.3. Advertisement

- Display ads (Google AdSense)
- Sponsored products
- Banner ads
- Native advertising

### 10.4. Data & Analytics

- Bán báo cáo thị trường
- API cho doanh nghiệp
- Market intelligence

### 10.5. White-label Solution

- Cung cấp giải pháp cho doanh nghiệp
- Customization
- On-premise deployment

---

## 11. KPIs (KEY PERFORMANCE INDICATORS)

### 11.1. Technical KPIs

- **Crawl Success Rate:** >= 95%
- **API Response Time:** < 500ms (p95)
- **System Uptime:** >= 99.5%
- **Data Freshness:** <= 6 hours
- **Matching Accuracy:** >= 90%

### 11.2. Business KPIs

- **Daily Active Users (DAU)**
- **Monthly Active Users (MAU)**
- **User Retention Rate:** >= 40% (30 days)
- **Conversion Rate:** >= 3% (click to purchase)
- **Revenue per User (ARPU)**
- **Customer Acquisition Cost (CAC)**
- **Lifetime Value (LTV)**

### 11.3. Product KPIs

- **Search Success Rate:** >= 80%
- **Alert Accuracy:** >= 95%
- **User Satisfaction Score:** >= 4.0/5.0
- **Average Savings per User:** >= 100k/tháng

---

## 12. RISK MANAGEMENT

### 12.1. Technical Risks

| Risk                               | Impact | Probability | Mitigation                                              |
| ---------------------------------- | ------ | ----------- | ------------------------------------------------------- |
| Sàn TMĐT thay đổi cấu trúc website | High   | High        | Monitoring, quick adaptation, multiple crawling methods |
| Bị block IP                        | High   | Medium      | Proxy rotation, rate limiting, distributed crawling     |
| Database overload                  | High   | Medium      | Sharding, caching, archiving                            |
| System downtime                    | High   | Low         | High availability, auto-scaling, monitoring             |

### 12.2. Business Risks

| Risk                           | Impact | Probability | Mitigation                              |
| ------------------------------ | ------ | ----------- | --------------------------------------- |
| Cạnh tranh từ các nền tảng lớn | High   | Medium      | Differentiation, niche focus, better UX |
| Thay đổi chính sách affiliate  | Medium | Medium      | Diversify revenue streams               |
| Vấn đề pháp lý                 | High   | Low         | Legal consultation, compliance          |
| Không đủ user                  | High   | Medium      | Marketing, SEO, partnerships            |

### 12.3. Legal Risks

| Risk                     | Impact | Probability | Mitigation                            |
| ------------------------ | ------ | ----------- | ------------------------------------- |
| Vi phạm ToS của sàn TMĐT | High   | Medium      | Use official APIs, legal review       |
| Vi phạm bảo mật dữ liệu  | High   | Low         | GDPR/PDPA compliance, security audit  |
| Tranh chấp bản quyền     | Medium | Low         | Clear disclaimers, proper attribution |

---

## 13. TEAM & RESOURCES

### 13.1. Team Structure

**Development Team:**

- 1 Tech Lead/Architect
- 2-3 Backend Developers
- 2 Frontend Developers
- 1 Mobile Developer
- 1 DevOps Engineer
- 1 Data Engineer
- 1 QA Engineer

**Data Team:**

- 1 Data Scientist
- 1 ML Engineer

**Product & Design:**

- 1 Product Manager
- 1 UI/UX Designer

**Business:**

- 1 Marketing Manager
- 1 Business Development

### 13.2. Infrastructure Cost (Monthly)

- **Cloud Hosting (AWS/GCP):** $500-1000
- **Database:** $200-500
- **Proxy Services:** $200-300
- **CDN:** $100-200
- **Monitoring & Logging:** $100
- **Email/SMS Services:** $50-100
- **Total:** ~$1,150-2,200/month

---

## 14. SUCCESS METRICS

### 14.1. Launch Goals (3 months)

- 10,000+ products tracked
- 1,000+ registered users
- 100+ daily active users
- 500+ price alerts set

### 14.2. Growth Goals (6 months)

- 50,000+ products tracked
- 10,000+ registered users
- 1,000+ daily active users
- 5,000+ price alerts set
- $1,000+ monthly revenue

### 14.3. Scale Goals (12 months)

- 200,000+ products tracked
- 50,000+ registered users
- 5,000+ daily active users
- 20,000+ price alerts set
- $10,000+ monthly revenue
- Mobile app launch
- Browser extension launch

---

## 15. CONCLUSION

Dự án so sánh giá sản phẩm và theo dõi biến động giá là một giải pháp có giá trị cao cho người tiêu dùng Việt Nam trong bối cảnh thương mại điện tử đang phát triển mạnh mẽ.

**Điểm mạnh:**

- Giải quyết pain point thực tế của người dùng
- Nhiều nguồn revenue tiềm năng
- Scalable và có thể mở rộng
- Technology stack hiện đại

**Thách thức:**

- Kỹ thuật crawling phức tạp
- Cạnh tranh từ các nền tảng lớn
- Vấn đề pháp lý cần lưu ý

**Khuyến nghị:**

- Bắt đầu với MVP, tập trung vào core features
- Ưu tiên UX/UI để differentiate
- Xây dựng community và trust
- Tuân thủ pháp luật và đạo đức
- Liên tục cải thiện thuật toán matching và prediction

Với roadmap rõ ràng và execution tốt, dự án có tiềm năng trở thành một nền tảng hữu ích và có lợi nhuận trong thị trường TMĐT Việt Nam.

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-23  
**Author:** Development Team  
**Status:** Draft
