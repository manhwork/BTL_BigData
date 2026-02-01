# 02. USE CASE SPECIFICATION (ĐẶC TẢ CHI TIẾT CHỨC NĂNG)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. TỔNG QUAN USE CASE

### 1.1. Use Case Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HỆ THỐNG SO SÁNH GIÁ TMĐT                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐                                               ┌─────────┐      │
│  │  Guest  │                                               │  Admin  │      │
│  └────┬────┘                                               └────┬────┘      │
│       │                                                         │           │
│       │    ┌─────────────────────────────────────────────────┐  │           │
│       │    │              USE CASES                          │  │           │
│       │    │                                                 │  │           │
│       ├────┼──▶ UC-01: Tìm kiếm sản phẩm                    │  │           │
│       ├────┼──▶ UC-02: Xem so sánh giá                       │  │           │
│       ├────┼──▶ UC-03: Xem lịch sử giá                       │  │           │
│       ├────┼──▶ UC-04: Đăng ký tài khoản                     │  │           │
│       │    │                                                 │  │           │
│  ┌────┴────┐   │                                            │  │           │
│  │  User   │───┼──▶ UC-05: Đăng nhập/Đăng xuất              │  │           │
│  └────┬────┘   │                                            │  │           │
│       ├────────┼──▶ UC-06: Quản lý Watchlist                │  │           │
│       ├────────┼──▶ UC-07: Quản lý Price Alert              │  │           │
│       ├────────┼──▶ UC-08: Xem Dashboard cá nhân            │  │           │
│       ├────────┼──▶ UC-09: Quản lý Profile                  │  │           │
│       │        │                                            │  │           │
│       │        │                                            │  │           │
│       │        │──▶ UC-10: Quản lý hệ thống crawl      ◀────┤           │
│       │        │──▶ UC-11: Quản lý người dùng          ◀────┤           │
│       │        │──▶ UC-12: Xem báo cáo thống kê        ◀────┤           │
│       │        │──▶ UC-13: Quản lý danh mục            ◀────┤           │
│       │        │──▶ UC-14: Tính lại điểm Shop          ◀────┤           │
│       │        │                                            │  │           │
│       │        └─────────────────────────────────────────────┘  │           │
│       │                                                         │           │
│  ┌────┴────┐                                               ┌────┴────┐     │
│  │ System  │                                               │ Crawler │     │
│  │ Timer   │                                               │ Worker  │     │
│  └────┬────┘                                               └────┬────┘     │
│       │    ┌─────────────────────────────────────────────────┐  │           │
│       │    │           SYSTEM USE CASES                      │  │           │
│       ├────┼──▶ UC-15: Crawl dữ liệu sản phẩm           ◀────┤           │
│       ├────┼──▶ UC-16: Xử lý và chuẩn hóa dữ liệu       ◀────┤           │
│       ├────┼──▶ UC-17: Phân loại Shop                   ◀────┤           │
│       ├────┼──▶ UC-18: Kiểm tra và gửi Alert            ◀────┤           │
│       │    └─────────────────────────────────────────────────┘  │           │
│       │                                                         │           │
└───────┴─────────────────────────────────────────────────────────┴───────────┘
```

### 1.2. Danh sách Use Case

| ID | Tên Use Case | Actor | Mức độ ưu tiên |
|----|--------------|-------|----------------|
| UC-01 | Tìm kiếm sản phẩm | Guest, User | High |
| UC-02 | Xem so sánh giá | Guest, User | High |
| UC-03 | Xem lịch sử giá | Guest, User | High |
| UC-04 | Đăng ký tài khoản | Guest | High |
| UC-05 | Đăng nhập/Đăng xuất | User | High |
| UC-06 | Quản lý Watchlist | User | High |
| UC-07 | Quản lý Price Alert | User | High |
| UC-08 | Xem Dashboard cá nhân | User | Medium |
| UC-09 | Quản lý Profile | User | Medium |
| UC-10 | Quản lý hệ thống crawl | Admin | High |
| UC-11 | Quản lý người dùng | Admin | Medium |
| UC-12 | Xem báo cáo thống kê | Admin | Medium |
| UC-13 | Quản lý danh mục | Admin | Low |
| UC-14 | Tính lại điểm Shop | Admin | Medium |
| UC-15 | Crawl dữ liệu sản phẩm | System | High |
| UC-16 | Xử lý và chuẩn hóa dữ liệu | System | High |
| UC-17 | Phân loại Shop | System | High |
| UC-18 | Kiểm tra và gửi Alert | System | High |

---

## 2. ĐẶC TẢ CHI TIẾT USE CASE

### 2.1. UC-01: TÌM KIẾM SẢN PHẨM

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-01 |
| **Tên Use Case** | Tìm kiếm sản phẩm |
| **Actor chính** | Guest, User |
| **Mô tả** | Cho phép người dùng tìm kiếm sản phẩm theo từ khóa, danh mục, hoặc bộ lọc |
| **Trigger** | Người dùng nhập từ khóa vào ô tìm kiếm |
| **Precondition** | Hệ thống hoạt động bình thường |
| **Postcondition** | Hiển thị danh sách sản phẩm phù hợp |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | User | Nhập từ khóa tìm kiếm | Hiển thị gợi ý auto-complete |
| 2 | User | Nhấn Enter hoặc click Search | Gửi request tìm kiếm |
| 3 | System | - | Kiểm tra cache |
| 4 | System | - | Query Elasticsearch |
| 5 | System | - | Matching sản phẩm |
| 6 | System | - | Trả về kết quả |
| 7 | User | Xem kết quả tìm kiếm | Hiển thị danh sách sản phẩm |

#### Luồng phụ (Alternative Flow)

| ID | Điều kiện | Hành động |
|----|-----------|-----------|
| AF-01 | Không tìm thấy kết quả | Hiển thị thông báo "Không tìm thấy sản phẩm" + Gợi ý từ khóa tương tự |
| AF-02 | Người dùng áp dụng bộ lọc | Lọc kết quả theo điều kiện (giá, sàn, rating, loại shop) |
| AF-03 | Người dùng sắp xếp kết quả | Sắp xếp theo tiêu chí (giá, rating, số lượng bán) |

#### Luồng ngoại lệ (Exception Flow)

| ID | Điều kiện | Hành động |
|----|-----------|-----------|
| EF-01 | Lỗi kết nối database | Hiển thị thông báo lỗi + Retry |
| EF-02 | Request timeout | Hiển thị thông báo "Hệ thống đang bận" |

#### Business Rules

- BR-01: Từ khóa tìm kiếm tối thiểu 2 ký tự
- BR-02: Kết quả tìm kiếm được cache trong 5 phút
- BR-03: Tối đa 100 kết quả mỗi trang
- BR-04: Auto-complete hiển thị tối đa 10 gợi ý

---

### 2.2. UC-02: XEM SO SÁNH GIÁ

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-02 |
| **Tên Use Case** | Xem so sánh giá |
| **Actor chính** | Guest, User |
| **Mô tả** | So sánh giá của cùng một sản phẩm trên các sàn TMĐT khác nhau |
| **Trigger** | Người dùng click vào sản phẩm từ kết quả tìm kiếm |
| **Precondition** | Sản phẩm đã được crawl và có dữ liệu |
| **Postcondition** | Hiển thị bảng so sánh giá chi tiết |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | User | Click xem chi tiết sản phẩm | Gửi request lấy thông tin |
| 2 | System | - | Lấy dữ liệu sản phẩm |
| 3 | System | - | Tìm sản phẩm tương tự trên các sàn |
| 4 | System | - | Tính toán điểm tổng hợp |
| 5 | System | - | Xếp hạng các lựa chọn |
| 6 | User | Xem bảng so sánh | Hiển thị bảng với các thông tin: |
| | | | - Hình ảnh sản phẩm |
| | | | - Tên sàn TMĐT |
| | | | - Giá gốc / Giá hiện tại |
| | | | - % giảm giá |
| | | | - Phí ship |
| | | | - Tổng giá cuối cùng |
| | | | - Rating / Số đánh giá |
| | | | - Loại Shop (Mall/Yêu thích/Rủi ro) |
| | | | - Link mua hàng |

#### Luồng phụ (Alternative Flow)

| ID | Điều kiện | Hành động |
|----|-----------|-----------|
| AF-01 | User click "Mua ngay" | Redirect đến trang sản phẩm trên sàn TMĐT (affiliate link) |
| AF-02 | User click "Thêm vào Watchlist" | Thêm sản phẩm vào danh sách theo dõi (yêu cầu đăng nhập) |
| AF-03 | User lọc theo loại Shop | Chỉ hiển thị shop theo loại đã chọn |

#### Display Format

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SO SÁNH GIÁ: iPhone 15 Pro Max 256GB                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ 🏢 SHOP MALL         │ Shopee Mall - Apple Official                │ │
│  │ Rating: ⭐ 4.9       │ Đã bán: 50,000+                              │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ Giá gốc:    ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶                                          │ │
│  │ Giá sale:   32,990,000đ   (-6%)                                   │ │
│  │ Phí ship:   Miễn phí                                              │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ TỔNG:       32,990,000đ   🏆 Giá tốt nhất                         │ │
│  │                            [Mua ngay]  [Theo dõi giá]             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ ⭐ SHOP YÊU THÍCH    │ Lazada - Di Động Việt                       │ │
│  │ Rating: ⭐ 4.7       │ Đã bán: 15,000+                              │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ Giá gốc:    ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶                                          │ │
│  │ Giá sale:   33,490,000đ   (-4%)                                   │ │
│  │ Phí ship:   30,000đ                                               │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ TỔNG:       33,520,000đ   (+530,000đ so với giá tốt nhất)         │ │
│  │                            [Mua ngay]  [Theo dõi giá]             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ ⚠️ SHOP RỦI RO       │ Tiki - New Seller                           │ │
│  │ Rating: ⭐ 4.2       │ Đã bán: 500+                                 │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ Giá gốc:    ̶3̶2̶,̶0̶0̶0̶,̶0̶0̶0̶đ̶                                          │ │
│  │ Giá sale:   31,500,000đ   (-2%)                                   │ │
│  │ Phí ship:   50,000đ                                               │ │
│  │ ──────────────────────────────────────────────────────────────────│ │
│  │ TỔNG:       31,550,000đ   ⚠️ Cần cẩn trọng khi mua                │ │
│  │                            [Mua ngay]  [Theo dõi giá]             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 2.3. UC-03: XEM LỊCH SỬ GIÁ

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-03 |
| **Tên Use Case** | Xem lịch sử giá |
| **Actor chính** | Guest, User |
| **Mô tả** | Xem biểu đồ lịch sử biến động giá của sản phẩm theo thời gian |
| **Trigger** | Người dùng click tab "Lịch sử giá" trong trang sản phẩm |
| **Precondition** | Sản phẩm có dữ liệu lịch sử giá |
| **Postcondition** | Hiển thị biểu đồ và thống kê giá |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | User | Click "Lịch sử giá" | Gửi request lấy price_history |
| 2 | System | - | Query price_history table |
| 3 | System | - | Aggregate data theo timeframe |
| 4 | System | - | Tính toán thống kê (min, max, avg) |
| 5 | User | Xem biểu đồ | Hiển thị line chart |
| 6 | User | Thay đổi timeframe | Cập nhật biểu đồ |

#### Timeframe Options

| Option | Mô tả |
|--------|-------|
| 7D | 7 ngày gần nhất |
| 30D | 30 ngày gần nhất |
| 90D | 90 ngày gần nhất |
| 6M | 6 tháng gần nhất |
| 1Y | 1 năm gần nhất |
| Custom | Tùy chỉnh khoảng thời gian |

#### Thống kê hiển thị

```
┌─────────────────────────────────────────────────────────────────┐
│                     THỐNG KÊ GIÁ (30 ngày)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Giá hiện tại:     32,990,000đ                                  │
│  Giá thấp nhất:    31,990,000đ  (15/01/2026 - Flash Sale)       │
│  Giá cao nhất:     34,990,000đ  (01/01/2026)                    │
│  Giá trung bình:   33,450,000đ                                  │
│  Xu hướng:         📉 Giảm 5% so với 30 ngày trước              │
│                                                                  │
│  [────────────────────────────────────────────────────────────] │
│  │                                                              │ │
│  │     ╭───╮                                                    │ │
│  │    ╱     ╲        ╭──╮                                       │ │
│  │   ╱       ╲──────╱    ╲────╮                                 │ │
│  │  ╱                         ╲───╮                             │ │
│  │ ╱                               ╲────────                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│    01/01    07/01    15/01    22/01    30/01                    │
│                                                                  │
│  📍 Sự kiện: [Flash Sale 15/01] [Tết Sale 22/01]                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.4. UC-04: ĐĂNG KÝ TÀI KHOẢN

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-04 |
| **Tên Use Case** | Đăng ký tài khoản |
| **Actor chính** | Guest |
| **Mô tả** | Tạo tài khoản mới để sử dụng đầy đủ tính năng |
| **Trigger** | Người dùng click "Đăng ký" |
| **Precondition** | Người dùng chưa có tài khoản |
| **Postcondition** | Tài khoản được tạo thành công |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | Guest | Click "Đăng ký" | Hiển thị form đăng ký |
| 2 | Guest | Nhập thông tin | Validate realtime |
| 3 | Guest | Click "Đăng ký" | Gửi request |
| 4 | System | - | Validate dữ liệu |
| 5 | System | - | Kiểm tra email tồn tại |
| 6 | System | - | Hash password |
| 7 | System | - | Tạo user record |
| 8 | System | - | Gửi email xác nhận |
| 9 | Guest | Xác nhận email | Kích hoạt tài khoản |

#### Validation Rules

| Field | Rule |
|-------|------|
| Email | Required, Valid email format, Unique |
| Password | Required, Min 8 chars, 1 uppercase, 1 number |
| Full Name | Required, 2-100 chars |
| Phone | Optional, Valid VN phone format |

---

### 2.5. UC-06: QUẢN LÝ WATCHLIST

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-06 |
| **Tên Use Case** | Quản lý Watchlist |
| **Actor chính** | User |
| **Mô tả** | Quản lý danh sách sản phẩm đang theo dõi |
| **Trigger** | User truy cập trang Watchlist |
| **Precondition** | User đã đăng nhập |
| **Postcondition** | Watchlist được cập nhật |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | User | Truy cập Watchlist | Lấy danh sách sản phẩm |
| 2 | System | - | Query watchlist + product info |
| 3 | User | Xem danh sách | Hiển thị sản phẩm với: |
| | | | - Hình ảnh |
| | | | - Tên sản phẩm |
| | | | - Giá hiện tại |
| | | | - Biến động giá |
| | | | - Alert status |

#### Sub Use Cases

| Action | Mô tả |
|--------|-------|
| Thêm sản phẩm | Từ trang so sánh giá |
| Xóa sản phẩm | Click nút "Bỏ theo dõi" |
| Tạo Alert | Click "Đặt cảnh báo giá" |
| Xem chi tiết | Click vào sản phẩm |

#### Giới hạn theo Tier

| User Tier | Max Products |
|-----------|--------------|
| Free | 10 |
| Premium | Unlimited |

---

### 2.6. UC-07: QUẢN LÝ PRICE ALERT

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-07 |
| **Tên Use Case** | Quản lý Price Alert |
| **Actor chính** | User |
| **Mô tả** | Tạo, sửa, xóa cảnh báo giá cho sản phẩm |
| **Trigger** | User click "Đặt cảnh báo" |
| **Precondition** | User đã đăng nhập, sản phẩm trong watchlist |
| **Postcondition** | Alert được tạo/cập nhật |

#### Luồng chính - Tạo Alert

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | User | Click "Đặt cảnh báo" | Hiển thị form tạo alert |
| 2 | User | Chọn loại alert | Hiển thị options tương ứng |
| 3 | User | Nhập điều kiện | Validate input |
| 4 | User | Chọn kênh thông báo | - |
| 5 | User | Click "Lưu" | Tạo alert record |
| 6 | System | - | Confirm thành công |

#### Alert Types

| Type | Mô tả | Điều kiện |
|------|-------|-----------|
| PRICE_DROP | Giá giảm xuống dưới ngưỡng | `current_price <= target_price` |
| PERCENTAGE_DROP | Giảm giá theo % | `discount >= target_pct%` |
| BEST_PRICE | Giá tốt nhất N ngày | `current_price <= min_price(N days)` |
| FLASH_SALE | Có flash sale | `event_tag = 'flash_sale'` |
| BACK_IN_STOCK | Có hàng trở lại | `is_available = true` |

#### Alert Form

```
┌─────────────────────────────────────────────────────────────────┐
│                    ĐẶT CẢNH BÁO GIÁ                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Sản phẩm: iPhone 15 Pro Max 256GB                              │
│  Giá hiện tại: 32,990,000đ                                      │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Loại cảnh báo:                                                 │
│  ○ Giá giảm xuống dưới: [___________]đ                          │
│  ○ Giảm giá ít nhất: [___]%                                     │
│  ● Giá tốt nhất trong [30] ngày                                 │
│  ○ Khi có Flash Sale                                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Theo dõi trên sàn:                                             │
│  ☑️ Shopee  ☑️ Lazada  ☑️ Tiki  ☐ Sendo  ☐ TikTok Shop         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Nhận thông báo qua:                                            │
│  ☑️ Email  ☑️ Push Notification  ☐ SMS                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│                    [Hủy]    [Lưu cảnh báo]                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Giới hạn theo Tier

| User Tier | Max Alerts |
|-----------|------------|
| Free | 5 |
| Premium | Unlimited |

---

### 2.7. UC-17: PHÂN LOẠI SHOP

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-17 |
| **Tên Use Case** | Phân loại Shop |
| **Actor chính** | System (Automated) |
| **Mô tả** | Tính điểm và phân loại shop theo độ tin cậy |
| **Trigger** | Sau khi crawl dữ liệu shop hoặc theo lịch |
| **Precondition** | Có dữ liệu shop từ crawl |
| **Postcondition** | Shop được phân loại (Mall/Preferred/Risky) |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | System | Trigger tính điểm | Lấy dữ liệu shop |
| 2 | System | - | Tính Rating_Score (25%) |
| 3 | System | - | Tính Review_Score (15%) |
| 4 | System | - | Tính Sales_Score (20%) |
| 5 | System | - | Tính Response_Score (10%) |
| 6 | System | - | Tính Success_Score (15%) |
| 7 | System | - | Tính Tenure_Score (10%) |
| 8 | System | - | Tính Badge_Score (5%) |
| 9 | System | - | Tổng hợp Shop Score |
| 10 | System | - | Phân loại theo ngưỡng |
| 11 | System | - | Cập nhật database |
| 12 | System | - | Gửi notification nếu thay đổi hạng |

#### Scoring Formula

```
Shop Score = (Rating_Score × 0.25) +
             (Review_Score × 0.15) +
             (Sales_Score × 0.20) +
             (Response_Score × 0.10) +
             (Success_Score × 0.15) +
             (Tenure_Score × 0.10) +
             (Badge_Score × 0.05)
```

#### Classification Rules

| Classification | Condition |
|----------------|-----------|
| 🏢 MALL | Score >= 80 AND has_mall_badge = true |
| ⭐ PREFERRED | Score >= 60 AND Score < 80 |
| ⚠️ RISKY | Score < 60 |

#### Tần suất cập nhật

| Shop Type | Frequency |
|-----------|-----------|
| MALL | Mỗi tuần |
| PREFERRED | Mỗi 3 ngày |
| RISKY | Mỗi ngày |

---

### 2.8. UC-18: KIỂM TRA VÀ GỬI ALERT

#### Thông tin chung

| Thuộc tính | Giá trị |
|------------|---------|
| **Use Case ID** | UC-18 |
| **Tên Use Case** | Kiểm tra và gửi Alert |
| **Actor chính** | System (Automated) |
| **Mô tả** | Kiểm tra điều kiện alert và gửi thông báo |
| **Trigger** | Sau khi cập nhật giá sản phẩm |
| **Precondition** | Có price update event |
| **Postcondition** | Alert được gửi nếu đạt điều kiện |

#### Luồng chính (Main Flow)

| Step | Actor | Hành động | System Response |
|------|-------|-----------|-----------------|
| 1 | System | Receive price update | Parse event |
| 2 | System | - | Query active alerts cho product |
| 3 | System | - | Loop: For each alert |
| 4 | System | - | Evaluate condition |
| 5 | System | - | If matched: Prepare notification |
| 6 | System | - | Send via configured channels |
| 7 | System | - | Log alert_history |
| 8 | System | - | Update last_triggered |

#### Notification Channels

| Channel | Implementation | Priority |
|---------|---------------|----------|
| Push Notification | Firebase FCM | Real-time |
| Email | SendGrid/SES | Within 5 mins |
| SMS | Twilio | Within 1 min |
| Telegram | Telegram Bot API | Real-time |

#### Notification Template

```
📢 CẢNH BÁO GIÁ TỐT!

Sản phẩm: iPhone 15 Pro Max 256GB
Sàn: Shopee Mall - Apple Official

💰 Giá giảm từ 34,990,000đ → 31,990,000đ
📉 Giảm 8.6% - Giá tốt nhất 30 ngày!

⏰ Flash Sale kết thúc sau 2 giờ

[Mua ngay] [Xem chi tiết]
```

---

## 3. TRACEABILITY MATRIX

### 3.1. Use Case - Business Process

| Use Case | Business Process |
|----------|-----------------|
| UC-01, UC-02 | BP-03: So sánh giá |
| UC-03 | BP-04: Theo dõi biến động giá |
| UC-04, UC-05, UC-09 | BP-06: Quản lý người dùng |
| UC-06 | BP-07: Quản lý Watchlist |
| UC-07 | BP-05: Cảnh báo giá |
| UC-15, UC-16 | BP-01: Thu thập dữ liệu |
| UC-17 | BP-02: Phân loại Shop |
| UC-18 | BP-05: Cảnh báo giá |

### 3.2. Use Case - API Endpoints

| Use Case | API Endpoints |
|----------|---------------|
| UC-01 | GET /api/products/search |
| UC-02 | GET /api/products/:id/compare |
| UC-03 | GET /api/products/:id/price-history |
| UC-04 | POST /api/auth/register |
| UC-05 | POST /api/auth/login, POST /api/auth/logout |
| UC-06 | GET/POST/DELETE /api/users/watchlist |
| UC-07 | GET/POST/PUT/DELETE /api/alerts |
| UC-17 | POST /api/sellers/:id/recalculate |

---

## 4. PHỤ LỤC

### 4.1. Actors Description

| Actor | Mô tả | Quyền hạn |
|-------|-------|-----------|
| Guest | Người dùng chưa đăng nhập | Tìm kiếm, xem so sánh, xem lịch sử giá |
| User | Người dùng đã đăng nhập | Tất cả quyền Guest + Watchlist, Alert, Profile |
| Admin | Quản trị viên | Quản lý hệ thống, người dùng, báo cáo |
| System | Hệ thống tự động | Crawl, xử lý dữ liệu, gửi alert |

### 4.2. Non-Functional Requirements

| NFR ID | Yêu cầu | Tiêu chí |
|--------|---------|----------|
| NFR-01 | Performance | API response < 500ms (p95) |
| NFR-02 | Availability | System uptime >= 99.5% |
| NFR-03 | Scalability | Support 10,000 concurrent users |
| NFR-04 | Data Freshness | Price data <= 6 hours old |
| NFR-05 | Security | Data encryption, HTTPS only |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
