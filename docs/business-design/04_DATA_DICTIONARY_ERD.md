# 04. DATA DICTIONARY & ERD (MÔ HÌNH DỮ LIỆU & TỪ ĐIỂN)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. ENTITY RELATIONSHIP DIAGRAM (ERD)

### 1.1. ERD Tổng quan

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIP DIAGRAM                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         │
│  │   USERS      │         │  CATEGORIES  │         │   PLATFORMS  │         │
│  │──────────────│         │──────────────│         │──────────────│         │
│  │ id (PK)      │         │ id (PK)      │         │ id (PK)      │         │
│  │ email        │         │ name         │         │ name         │         │
│  │ password_hash│         │ parent_id(FK)│◀────┐   │ logo_url     │         │
│  │ full_name    │         │ level        │     │   │ base_url     │         │
│  │ phone        │         └──────┬───────┘     │   └──────┬───────┘         │
│  │ tier         │                │             │          │                 │
│  │ preferences  │                │             │          │                 │
│  └──────┬───────┘                │             │          │                 │
│         │                        │             │          │                 │
│         │ 1                      │ 1           │          │ 1               │
│         │                        │             │          │                 │
│         │                        ▼             │          ▼                 │
│         │              ┌──────────────┐        │  ┌──────────────┐          │
│         │              │   PRODUCTS   │        │  │   SELLERS    │          │
│         │              │──────────────│        │  │──────────────│          │
│         │              │ id (PK)      │        │  │ id (PK)      │          │
│         │              │ name         │        │  │ platform(FK) │──────────┤
│         │              │ normalized   │        │  │ seller_name  │          │
│         │              │ description  │        │  │ seller_rating│          │
│         │              │ category_id  │────────┘  │ shop_type    │          │
│         │              │ brand        │           │ shop_score   │          │
│         │              │ attributes   │           │ response_rate│          │
│         │              │ image_urls   │           │ success_rate │          │
│         │              └──────┬───────┘           │ has_mall_badge│         │
│         │                     │                   └──────┬───────┘          │
│         │                     │ 1                        │ 1                │
│         │                     │                          │                  │
│         │                     ▼                          ▼                  │
│         │            ┌────────────────────────────────────────┐             │
│         │            │         PRODUCT_LISTINGS               │             │
│         │            │────────────────────────────────────────│             │
│         │            │ id (PK)                                │             │
│         │            │ product_id (FK) ───────────────────────┤             │
│         │            │ seller_id (FK) ────────────────────────┤             │
│         │            │ platform (FK) ─────────────────────────┤             │
│         │            │ platform_product_id                    │             │
│         │            │ url                                    │             │
│         │            │ current_price                          │             │
│         │            │ original_price                         │             │
│         │            │ discount_percentage                    │             │
│         │            │ shipping_fee                           │             │
│         │            │ rating, review_count, sold_count       │             │
│         │            │ is_available, stock_quantity           │             │
│         │            │ last_crawled_at                        │             │
│         │            └──────────────┬─────────────────────────┘             │
│         │                           │ 1                                     │
│         │                           │                                       │
│         │                           ▼                                       │
│         │                  ┌──────────────┐                                 │
│         │                  │PRICE_HISTORY │                                 │
│         │                  │──────────────│                                 │
│         │                  │ id (PK)      │                                 │
│         │                  │ listing_id(FK)│                                │
│         │                  │ price        │                                 │
│         │                  │ original_price│                                │
│         │                  │ discount_pct │                                 │
│         │                  │ shipping_fee │                                 │
│         │                  │ final_price  │                                 │
│         │                  │ event_tag    │                                 │
│         │                  │ recorded_at  │                                 │
│         │                  └──────────────┘                                 │
│         │                                                                   │
│         │ 1                                                                 │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │ WATCHLIST    │    │PRICE_ALERTS  │    │ALERT_HISTORY │                  │
│  │──────────────│    │──────────────│    │──────────────│                  │
│  │ id (PK)      │    │ id (PK)      │    │ id (PK)      │                  │
│  │ user_id (FK) │    │ user_id (FK) │    │ alert_id(FK) │                  │
│  │ product_id(FK)    │ product_id(FK)    │ listing_id(FK)                  │
│  │ added_at     │    │ alert_type   │    │ triggered_price                 │
│  └──────────────┘    │ target_price │    │ message      │                  │
│                      │ target_pct   │    │ sent_at      │                  │
│                      │ platforms    │    └──────────────┘                  │
│                      │ channels     │                                       │
│                      │ is_active    │                                       │
│                      └──────────────┘                                       │
│                                                                              │
│  ┌──────────────┐                                                           │
│  │SEARCH_HISTORY│                                                           │
│  │──────────────│                                                           │
│  │ id (PK)      │                                                           │
│  │ user_id (FK) │                                                           │
│  │ search_query │                                                           │
│  │ filters      │                                                           │
│  │ result_count │                                                           │
│  │ searched_at  │                                                           │
│  └──────────────┘                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2. Quan hệ giữa các Entity

| Relation | Entity A | Entity B | Cardinality | Mô tả |
|----------|----------|----------|-------------|-------|
| R1 | Users | Watchlist | 1:N | User có nhiều sản phẩm theo dõi |
| R2 | Users | Price_Alerts | 1:N | User có nhiều cảnh báo giá |
| R3 | Users | Search_History | 1:N | User có nhiều lịch sử tìm kiếm |
| R4 | Products | Product_Listings | 1:N | Sản phẩm có nhiều listings trên các sàn |
| R5 | Products | Watchlist | 1:N | Sản phẩm được nhiều user theo dõi |
| R6 | Products | Price_Alerts | 1:N | Sản phẩm có nhiều cảnh báo |
| R7 | Products | Categories | N:1 | Nhiều sản phẩm thuộc 1 danh mục |
| R8 | Sellers | Product_Listings | 1:N | Shop có nhiều listings |
| R9 | Sellers | Platforms | N:1 | Shop thuộc về 1 platform |
| R10 | Product_Listings | Price_History | 1:N | Listing có nhiều lịch sử giá |
| R11 | Price_Alerts | Alert_History | 1:N | Alert có nhiều lịch sử trigger |
| R12 | Categories | Categories | 1:N | Danh mục cha-con (self-reference) |

---

## 2. DATA DICTIONARY (TỪ ĐIỂN DỮ LIỆU)

### 2.1. Bảng USERS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | email | VARCHAR(255) | NOT NULL | - | Email đăng nhập (unique) |
| 3 | password_hash | VARCHAR(255) | NOT NULL | - | Mật khẩu đã hash |
| 4 | full_name | VARCHAR(100) | NOT NULL | - | Họ tên đầy đủ |
| 5 | phone | VARCHAR(15) | NULL | NULL | Số điện thoại |
| 6 | tier | ENUM | NOT NULL | 'FREE' | Gói dịch vụ (FREE, PREMIUM) |
| 7 | preferences | JSONB | NULL | '{}' | Cài đặt cá nhân |
| 8 | email_verified | BOOLEAN | NOT NULL | FALSE | Email đã xác thực |
| 9 | is_active | BOOLEAN | NOT NULL | TRUE | Tài khoản đang hoạt động |
| 10 | last_login_at | TIMESTAMP | NULL | NULL | Thời gian đăng nhập cuối |
| 11 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |
| 12 | updated_at | TIMESTAMP | NOT NULL | NOW() | Thời gian cập nhật |

**Indexes:**
- `idx_users_email` (UNIQUE) ON email
- `idx_users_tier` ON tier

**Constraints:**
- `chk_users_email` CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
- `chk_users_tier` CHECK (tier IN ('FREE', 'PREMIUM'))

---

### 2.2. Bảng CATEGORIES

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | name | VARCHAR(100) | NOT NULL | - | Tên danh mục |
| 3 | slug | VARCHAR(100) | NOT NULL | - | Slug cho URL |
| 4 | parent_id | UUID | NULL | NULL | FK đến danh mục cha |
| 5 | level | INTEGER | NOT NULL | 1 | Cấp độ danh mục |
| 6 | icon_url | VARCHAR(500) | NULL | NULL | URL icon |
| 7 | is_active | BOOLEAN | NOT NULL | TRUE | Đang hoạt động |
| 8 | sort_order | INTEGER | NOT NULL | 0 | Thứ tự hiển thị |
| 9 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |

**Indexes:**
- `idx_categories_slug` (UNIQUE) ON slug
- `idx_categories_parent` ON parent_id
- `idx_categories_level` ON level

**Constraints:**
- `fk_categories_parent` FOREIGN KEY (parent_id) REFERENCES categories(id)
- `chk_categories_level` CHECK (level >= 1 AND level <= 5)

---

### 2.3. Bảng PLATFORMS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | name | VARCHAR(50) | NOT NULL | - | Tên sàn TMĐT |
| 3 | code | VARCHAR(20) | NOT NULL | - | Mã sàn (SHOPEE, LAZADA...) |
| 4 | logo_url | VARCHAR(500) | NULL | NULL | URL logo |
| 5 | base_url | VARCHAR(255) | NOT NULL | - | URL gốc |
| 6 | affiliate_url | VARCHAR(500) | NULL | NULL | URL affiliate |
| 7 | is_active | BOOLEAN | NOT NULL | TRUE | Đang hoạt động |
| 8 | crawl_config | JSONB | NULL | '{}' | Cấu hình crawl |
| 9 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |

**Indexes:**
- `idx_platforms_code` (UNIQUE) ON code

**Enum Values (code):**
- SHOPEE, LAZADA, TIKI, SENDO, TIKTOK_SHOP

---

### 2.4. Bảng PRODUCTS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | name | VARCHAR(500) | NOT NULL | - | Tên sản phẩm gốc |
| 3 | normalized_name | VARCHAR(500) | NOT NULL | - | Tên đã chuẩn hóa |
| 4 | description | TEXT | NULL | NULL | Mô tả sản phẩm |
| 5 | category_id | UUID | NOT NULL | - | FK đến categories |
| 6 | brand | VARCHAR(100) | NULL | NULL | Thương hiệu |
| 7 | attributes | JSONB | NULL | '{}' | Thuộc tính (màu, size...) |
| 8 | image_urls | TEXT[] | NULL | '{}' | Mảng URL hình ảnh |
| 9 | tags | VARCHAR(50)[] | NULL | '{}' | Tags/keywords |
| 10 | is_active | BOOLEAN | NOT NULL | TRUE | Đang hoạt động |
| 11 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |
| 12 | updated_at | TIMESTAMP | NOT NULL | NOW() | Thời gian cập nhật |

**Indexes:**
- `idx_products_category` ON category_id
- `idx_products_brand` ON brand
- `idx_products_normalized_name` ON normalized_name (GIN trigram)
- `idx_products_tags` ON tags (GIN)

**Full-text Search Index:**
- `idx_products_search` ON to_tsvector('vietnamese', name || ' ' || COALESCE(description, ''))

---

### 2.5. Bảng SELLERS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | platform_id | UUID | NOT NULL | - | FK đến platforms |
| 3 | platform_seller_id | VARCHAR(100) | NOT NULL | - | ID shop trên sàn |
| 4 | seller_name | VARCHAR(255) | NOT NULL | - | Tên shop |
| 5 | seller_url | VARCHAR(500) | NULL | NULL | URL shop |
| 6 | seller_rating | DECIMAL(2,1) | NULL | NULL | Rating (0.0-5.0) |
| 7 | total_products | INTEGER | NOT NULL | 0 | Tổng số sản phẩm |
| 8 | total_sold | BIGINT | NOT NULL | 0 | Tổng đã bán |
| 9 | review_count | INTEGER | NOT NULL | 0 | Số lượng đánh giá |
| 10 | follower_count | INTEGER | NOT NULL | 0 | Số người theo dõi |
| 11 | join_date | DATE | NULL | NULL | Ngày tham gia |
| 12 | response_rate | DECIMAL(5,2) | NULL | NULL | Tỷ lệ phản hồi (%) |
| 13 | success_rate | DECIMAL(5,2) | NULL | NULL | Tỷ lệ thành công (%) |
| 14 | positive_review_rate | DECIMAL(5,2) | NULL | NULL | Tỷ lệ đánh giá tích cực (%) |
| 15 | return_rate | DECIMAL(5,2) | NULL | NULL | Tỷ lệ hoàn/khiếu nại (%) |
| 16 | has_mall_badge | BOOLEAN | NOT NULL | FALSE | Có badge Mall |
| 17 | has_preferred_badge | BOOLEAN | NOT NULL | FALSE | Có badge Yêu thích |
| 18 | **shop_type** | ENUM | NOT NULL | 'RISKY' | Loại shop |
| 19 | **shop_score** | DECIMAL(5,2) | NOT NULL | 0 | Điểm tin cậy (0-100) |
| 20 | last_score_updated_at | TIMESTAMP | NULL | NULL | Thời gian cập nhật điểm |
| 21 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |
| 22 | updated_at | TIMESTAMP | NOT NULL | NOW() | Thời gian cập nhật |

**Indexes:**
- `idx_sellers_platform` ON platform_id
- `idx_sellers_platform_id` (UNIQUE) ON (platform_id, platform_seller_id)
- `idx_sellers_shop_type` ON shop_type
- `idx_sellers_shop_score` ON shop_score DESC

**Constraints:**
- `fk_sellers_platform` FOREIGN KEY (platform_id) REFERENCES platforms(id)
- `chk_sellers_rating` CHECK (seller_rating >= 0 AND seller_rating <= 5.0)
- `chk_sellers_shop_type` CHECK (shop_type IN ('MALL', 'PREFERRED', 'RISKY'))
- `chk_sellers_shop_score` CHECK (shop_score >= 0 AND shop_score <= 100)
- `chk_sellers_rates` CHECK (response_rate BETWEEN 0 AND 100 AND success_rate BETWEEN 0 AND 100)

---

### 2.6. Bảng PRODUCT_LISTINGS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | product_id | UUID | NOT NULL | - | FK đến products |
| 3 | seller_id | UUID | NOT NULL | - | FK đến sellers |
| 4 | platform_id | UUID | NOT NULL | - | FK đến platforms |
| 5 | platform_product_id | VARCHAR(100) | NOT NULL | - | ID sản phẩm trên sàn |
| 6 | url | VARCHAR(1000) | NOT NULL | - | URL sản phẩm |
| 7 | **current_price** | DECIMAL(15,2) | NOT NULL | - | Giá hiện tại |
| 8 | **original_price** | DECIMAL(15,2) | NULL | NULL | Giá gốc |
| 9 | **discount_percentage** | DECIMAL(5,2) | NULL | 0 | % giảm giá |
| 10 | **shipping_fee** | DECIMAL(15,2) | NULL | 0 | Phí vận chuyển |
| 11 | rating | DECIMAL(2,1) | NULL | NULL | Rating sản phẩm |
| 12 | review_count | INTEGER | NOT NULL | 0 | Số đánh giá |
| 13 | sold_count | BIGINT | NOT NULL | 0 | Số đã bán |
| 14 | stock_quantity | INTEGER | NULL | NULL | Số lượng tồn kho |
| 15 | is_available | BOOLEAN | NOT NULL | TRUE | Còn hàng |
| 16 | is_flash_sale | BOOLEAN | NOT NULL | FALSE | Đang flash sale |
| 17 | flash_sale_end | TIMESTAMP | NULL | NULL | Thời gian kết thúc flash sale |
| 18 | voucher_codes | JSONB | NULL | '[]' | Mã giảm giá |
| 19 | last_crawled_at | TIMESTAMP | NOT NULL | NOW() | Lần crawl cuối |
| 20 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |
| 21 | updated_at | TIMESTAMP | NOT NULL | NOW() | Thời gian cập nhật |

**Indexes:**
- `idx_listings_product` ON product_id
- `idx_listings_seller` ON seller_id
- `idx_listings_platform` ON platform_id
- `idx_listings_platform_product` (UNIQUE) ON (platform_id, platform_product_id)
- `idx_listings_price` ON current_price
- `idx_listings_crawled` ON last_crawled_at
- `idx_listings_available` ON is_available WHERE is_available = TRUE

**Constraints:**
- `fk_listings_product` FOREIGN KEY (product_id) REFERENCES products(id)
- `fk_listings_seller` FOREIGN KEY (seller_id) REFERENCES sellers(id)
- `fk_listings_platform` FOREIGN KEY (platform_id) REFERENCES platforms(id)
- `chk_listings_price` CHECK (current_price > 0 AND current_price <= 1000000000)
- `chk_listings_discount` CHECK (discount_percentage BETWEEN 0 AND 100)

---

### 2.7. Bảng PRICE_HISTORY

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | listing_id | UUID | NOT NULL | - | FK đến product_listings |
| 3 | **price** | DECIMAL(15,2) | NOT NULL | - | Giá tại thời điểm |
| 4 | **original_price** | DECIMAL(15,2) | NULL | NULL | Giá gốc |
| 5 | **discount_percentage** | DECIMAL(5,2) | NULL | 0 | % giảm giá |
| 6 | **shipping_fee** | DECIMAL(15,2) | NULL | 0 | Phí ship |
| 7 | **final_price** | DECIMAL(15,2) | NOT NULL | - | Tổng giá cuối |
| 8 | stock_status | BOOLEAN | NOT NULL | TRUE | Còn hàng |
| 9 | stock_quantity | INTEGER | NULL | NULL | Số lượng tồn |
| 10 | event_tag | VARCHAR(50) | NULL | NULL | Tag sự kiện |
| 11 | **recorded_at** | TIMESTAMP | NOT NULL | NOW() | Thời gian ghi nhận |

**Indexes:**
- `idx_price_history_listing` ON listing_id
- `idx_price_history_recorded` ON recorded_at DESC
- `idx_price_history_listing_time` ON (listing_id, recorded_at DESC)
- `idx_price_history_event` ON event_tag WHERE event_tag IS NOT NULL

**Constraints:**
- `fk_price_history_listing` FOREIGN KEY (listing_id) REFERENCES product_listings(id) ON DELETE CASCADE
- `chk_price_history_price` CHECK (price > 0 AND final_price > 0)

**Partitioning:** Partition by RANGE (recorded_at) - Monthly partitions

**Event Tags:**
- REGULAR, FLASH_SALE, 11_11, 12_12, BLACK_FRIDAY, TET_SALE, MEGA_SALE

---

### 2.8. Bảng USER_WATCHLIST

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | user_id | UUID | NOT NULL | - | FK đến users |
| 3 | product_id | UUID | NOT NULL | - | FK đến products |
| 4 | notes | TEXT | NULL | NULL | Ghi chú |
| 5 | notify_on_price_drop | BOOLEAN | NOT NULL | TRUE | Thông báo khi giảm giá |
| 6 | added_at | TIMESTAMP | NOT NULL | NOW() | Thời gian thêm |

**Indexes:**
- `idx_watchlist_user` ON user_id
- `idx_watchlist_product` ON product_id
- `idx_watchlist_user_product` (UNIQUE) ON (user_id, product_id)

**Constraints:**
- `fk_watchlist_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `fk_watchlist_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE

---

### 2.9. Bảng PRICE_ALERTS

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | user_id | UUID | NOT NULL | - | FK đến users |
| 3 | product_id | UUID | NOT NULL | - | FK đến products |
| 4 | **alert_type** | ENUM | NOT NULL | - | Loại cảnh báo |
| 5 | target_price | DECIMAL(15,2) | NULL | NULL | Giá mục tiêu |
| 6 | target_percentage | DECIMAL(5,2) | NULL | NULL | % giảm mục tiêu |
| 7 | target_days | INTEGER | NULL | 30 | Số ngày (cho best price) |
| 8 | platforms | UUID[] | NULL | NULL | Các sàn cần theo dõi |
| 9 | notification_channels | VARCHAR(20)[] | NOT NULL | '{EMAIL}' | Kênh thông báo |
| 10 | is_active | BOOLEAN | NOT NULL | TRUE | Đang hoạt động |
| 11 | last_triggered_at | TIMESTAMP | NULL | NULL | Lần trigger cuối |
| 12 | trigger_count | INTEGER | NOT NULL | 0 | Số lần trigger |
| 13 | created_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tạo |
| 14 | updated_at | TIMESTAMP | NOT NULL | NOW() | Thời gian cập nhật |

**Indexes:**
- `idx_alerts_user` ON user_id
- `idx_alerts_product` ON product_id
- `idx_alerts_active` ON is_active WHERE is_active = TRUE
- `idx_alerts_type` ON alert_type

**Constraints:**
- `fk_alerts_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- `fk_alerts_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
- `chk_alerts_type` CHECK (alert_type IN ('PRICE_DROP', 'PERCENTAGE_DROP', 'BEST_PRICE', 'FLASH_SALE', 'BACK_IN_STOCK', 'CROSS_PLATFORM'))
- `chk_alerts_channels` CHECK (notification_channels <@ ARRAY['EMAIL', 'PUSH', 'SMS', 'TELEGRAM']::VARCHAR[])

---

### 2.10. Bảng ALERT_HISTORY

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | alert_id | UUID | NOT NULL | - | FK đến price_alerts |
| 3 | listing_id | UUID | NOT NULL | - | FK đến product_listings |
| 4 | triggered_price | DECIMAL(15,2) | NOT NULL | - | Giá khi trigger |
| 5 | previous_price | DECIMAL(15,2) | NULL | NULL | Giá trước đó |
| 6 | message | TEXT | NOT NULL | - | Nội dung thông báo |
| 7 | channels_sent | VARCHAR(20)[] | NOT NULL | - | Các kênh đã gửi |
| 8 | sent_at | TIMESTAMP | NOT NULL | NOW() | Thời gian gửi |

**Indexes:**
- `idx_alert_history_alert` ON alert_id
- `idx_alert_history_listing` ON listing_id
- `idx_alert_history_sent` ON sent_at DESC

**Constraints:**
- `fk_alert_history_alert` FOREIGN KEY (alert_id) REFERENCES price_alerts(id) ON DELETE CASCADE
- `fk_alert_history_listing` FOREIGN KEY (listing_id) REFERENCES product_listings(id)

---

### 2.11. Bảng SEARCH_HISTORY

| # | Tên cột | Kiểu dữ liệu | Null | Default | Mô tả |
|---|---------|--------------|------|---------|-------|
| 1 | id | UUID | NOT NULL | gen_random_uuid() | Khóa chính |
| 2 | user_id | UUID | NULL | NULL | FK đến users (null nếu guest) |
| 3 | session_id | VARCHAR(100) | NULL | NULL | Session ID |
| 4 | search_query | VARCHAR(500) | NOT NULL | - | Từ khóa tìm kiếm |
| 5 | filters | JSONB | NULL | '{}' | Bộ lọc đã áp dụng |
| 6 | result_count | INTEGER | NOT NULL | 0 | Số kết quả |
| 7 | clicked_product_id | UUID | NULL | NULL | Sản phẩm đã click |
| 8 | ip_address | INET | NULL | NULL | Địa chỉ IP |
| 9 | user_agent | TEXT | NULL | NULL | User agent |
| 10 | searched_at | TIMESTAMP | NOT NULL | NOW() | Thời gian tìm kiếm |

**Indexes:**
- `idx_search_history_user` ON user_id
- `idx_search_history_query` ON search_query
- `idx_search_history_time` ON searched_at DESC

---

## 3. ENUM TYPES

### 3.1. User Tier

```sql
CREATE TYPE user_tier AS ENUM ('FREE', 'PREMIUM');
```

### 3.2. Shop Type

```sql
CREATE TYPE shop_type AS ENUM ('MALL', 'PREFERRED', 'RISKY');
```

### 3.3. Alert Type

```sql
CREATE TYPE alert_type AS ENUM (
  'PRICE_DROP',
  'PERCENTAGE_DROP',
  'BEST_PRICE',
  'FLASH_SALE',
  'BACK_IN_STOCK',
  'CROSS_PLATFORM'
);
```

### 3.4. Notification Channel

```sql
CREATE TYPE notification_channel AS ENUM ('EMAIL', 'PUSH', 'SMS', 'TELEGRAM');
```

---

## 4. VIEWS

### 4.1. v_product_comparison

```sql
CREATE VIEW v_product_comparison AS
SELECT 
  p.id AS product_id,
  p.name AS product_name,
  p.brand,
  pl.id AS listing_id,
  plt.name AS platform_name,
  s.seller_name,
  s.shop_type,
  s.shop_score,
  pl.current_price,
  pl.original_price,
  pl.discount_percentage,
  pl.shipping_fee,
  (pl.current_price + COALESCE(pl.shipping_fee, 0)) AS final_price,
  pl.rating AS product_rating,
  pl.review_count,
  pl.sold_count,
  pl.is_available,
  pl.url AS product_url,
  pl.last_crawled_at
FROM products p
JOIN product_listings pl ON p.id = pl.product_id
JOIN platforms plt ON pl.platform_id = plt.id
JOIN sellers s ON pl.seller_id = s.id
WHERE p.is_active = TRUE AND pl.is_available = TRUE;
```

### 4.2. v_price_statistics

```sql
CREATE VIEW v_price_statistics AS
SELECT 
  listing_id,
  DATE_TRUNC('day', recorded_at) AS date,
  MIN(price) AS min_price,
  MAX(price) AS max_price,
  AVG(price) AS avg_price,
  COUNT(*) AS record_count
FROM price_history
GROUP BY listing_id, DATE_TRUNC('day', recorded_at);
```

### 4.3. v_shop_ranking

```sql
CREATE VIEW v_shop_ranking AS
SELECT 
  s.*,
  plt.name AS platform_name,
  RANK() OVER (PARTITION BY s.platform_id ORDER BY s.shop_score DESC) AS rank_in_platform,
  COUNT(pl.id) AS listing_count
FROM sellers s
JOIN platforms plt ON s.platform_id = plt.id
LEFT JOIN product_listings pl ON s.id = pl.seller_id
GROUP BY s.id, plt.name;
```

---

## 5. FUNCTIONS & TRIGGERS

### 5.1. Function: Calculate Shop Score

```sql
CREATE OR REPLACE FUNCTION calculate_shop_score(seller_id UUID)
RETURNS DECIMAL(5,2) AS $$
DECLARE
  v_rating_score DECIMAL;
  v_review_score DECIMAL;
  v_sales_score DECIMAL;
  v_response_score DECIMAL;
  v_success_score DECIMAL;
  v_tenure_score DECIMAL;
  v_badge_score DECIMAL;
  v_total_score DECIMAL;
  v_seller RECORD;
BEGIN
  SELECT * INTO v_seller FROM sellers WHERE id = seller_id;
  
  -- Rating Score (25%)
  v_rating_score := CASE
    WHEN v_seller.seller_rating = 5.0 THEN 100
    WHEN v_seller.seller_rating >= 4.8 THEN 90
    WHEN v_seller.seller_rating >= 4.5 THEN 75
    WHEN v_seller.seller_rating >= 4.0 THEN 50
    ELSE 25
  END;
  
  -- Review Score (15%)
  v_review_score := CASE
    WHEN v_seller.review_count >= 10000 THEN 100
    WHEN v_seller.review_count >= 5000 THEN 80
    WHEN v_seller.review_count >= 1000 THEN 60
    WHEN v_seller.review_count >= 500 THEN 40
    WHEN v_seller.review_count >= 100 THEN 20
    ELSE 10
  END;
  
  -- Sales Score (20%)
  v_sales_score := CASE
    WHEN v_seller.total_sold >= 100000 THEN 100
    WHEN v_seller.total_sold >= 50000 THEN 85
    WHEN v_seller.total_sold >= 10000 THEN 70
    WHEN v_seller.total_sold >= 5000 THEN 50
    WHEN v_seller.total_sold >= 1000 THEN 30
    ELSE 15
  END;
  
  -- Response Score (10%)
  v_response_score := CASE
    WHEN v_seller.response_rate >= 95 THEN 100
    WHEN v_seller.response_rate >= 90 THEN 80
    WHEN v_seller.response_rate >= 80 THEN 60
    WHEN v_seller.response_rate >= 70 THEN 40
    ELSE 20
  END;
  
  -- Success Score (15%)
  v_success_score := CASE
    WHEN v_seller.success_rate >= 98 THEN 100
    WHEN v_seller.success_rate >= 95 THEN 85
    WHEN v_seller.success_rate >= 90 THEN 70
    WHEN v_seller.success_rate >= 85 THEN 50
    ELSE 25
  END;
  
  -- Tenure Score (10%)
  v_tenure_score := CASE
    WHEN v_seller.join_date <= CURRENT_DATE - INTERVAL '3 years' THEN 100
    WHEN v_seller.join_date <= CURRENT_DATE - INTERVAL '1 year' THEN 75
    WHEN v_seller.join_date <= CURRENT_DATE - INTERVAL '6 months' THEN 50
    WHEN v_seller.join_date <= CURRENT_DATE - INTERVAL '3 months' THEN 30
    ELSE 10
  END;
  
  -- Badge Score (5%)
  v_badge_score := CASE
    WHEN v_seller.has_mall_badge THEN 100
    WHEN v_seller.has_preferred_badge THEN 70
    ELSE 30
  END;
  
  -- Total Score
  v_total_score := (v_rating_score * 0.25) +
                   (v_review_score * 0.15) +
                   (v_sales_score * 0.20) +
                   (v_response_score * 0.10) +
                   (v_success_score * 0.15) +
                   (v_tenure_score * 0.10) +
                   (v_badge_score * 0.05);
  
  RETURN ROUND(v_total_score, 2);
END;
$$ LANGUAGE plpgsql;
```

### 5.2. Function: Classify Shop Type

```sql
CREATE OR REPLACE FUNCTION classify_shop_type(score DECIMAL, has_mall BOOLEAN)
RETURNS shop_type AS $$
BEGIN
  IF score >= 80 AND has_mall THEN
    RETURN 'MALL';
  ELSIF score >= 60 THEN
    RETURN 'PREFERRED';
  ELSE
    RETURN 'RISKY';
  END IF;
END;
$$ LANGUAGE plpgsql;
```

### 5.3. Trigger: Update Shop Score

```sql
CREATE OR REPLACE FUNCTION trigger_update_shop_score()
RETURNS TRIGGER AS $$
DECLARE
  v_new_score DECIMAL;
  v_new_type shop_type;
BEGIN
  v_new_score := calculate_shop_score(NEW.id);
  v_new_type := classify_shop_type(v_new_score, NEW.has_mall_badge);
  
  NEW.shop_score := v_new_score;
  NEW.shop_type := v_new_type;
  NEW.last_score_updated_at := NOW();
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_shop_score
BEFORE INSERT OR UPDATE OF seller_rating, review_count, total_sold, 
                          response_rate, success_rate, join_date, 
                          has_mall_badge, has_preferred_badge
ON sellers
FOR EACH ROW
EXECUTE FUNCTION trigger_update_shop_score();
```

### 5.4. Trigger: Record Price History

```sql
CREATE OR REPLACE FUNCTION trigger_record_price_history()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.current_price IS DISTINCT FROM NEW.current_price THEN
    INSERT INTO price_history (
      listing_id, price, original_price, discount_percentage,
      shipping_fee, final_price, stock_status, stock_quantity, recorded_at
    ) VALUES (
      NEW.id, NEW.current_price, NEW.original_price, NEW.discount_percentage,
      NEW.shipping_fee, NEW.current_price + COALESCE(NEW.shipping_fee, 0),
      NEW.is_available, NEW.stock_quantity, NOW()
    );
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_record_price_history
AFTER UPDATE OF current_price
ON product_listings
FOR EACH ROW
EXECUTE FUNCTION trigger_record_price_history();
```

---

## 6. DATABASE INDEXES SUMMARY

| Table | Index Name | Columns | Type | Purpose |
|-------|------------|---------|------|---------|
| users | idx_users_email | email | UNIQUE | Login lookup |
| categories | idx_categories_slug | slug | UNIQUE | URL routing |
| platforms | idx_platforms_code | code | UNIQUE | Platform lookup |
| products | idx_products_search | name, description | GIN (FTS) | Full-text search |
| sellers | idx_sellers_shop_score | shop_score DESC | BTREE | Ranking |
| product_listings | idx_listings_price | current_price | BTREE | Price filtering |
| price_history | idx_price_history_listing_time | listing_id, recorded_at | BTREE | History query |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
