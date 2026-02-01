# 03. BUSINESS RULES CATALOG (DANH MỤC LUẬT NGHIỆP VỤ & CÔNG THỨC)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. TỔNG QUAN

### 1.1. Phân loại Business Rules

| Loại | Ký hiệu | Mô tả |
|------|---------|-------|
| Computation | BR-COMP | Công thức tính toán |
| Constraint | BR-CONS | Ràng buộc dữ liệu |
| Inference | BR-INF | Suy luận logic |
| Action | BR-ACT | Hành động tự động |
| Validation | BR-VAL | Kiểm tra dữ liệu |

### 1.2. Mức độ ưu tiên

| Priority | Mô tả |
|----------|-------|
| P1 - Critical | Bắt buộc, ảnh hưởng core business |
| P2 - High | Quan trọng, ảnh hưởng trải nghiệm |
| P3 - Medium | Cần thiết, có thể điều chỉnh |
| P4 - Low | Tùy chọn, có thể bỏ qua |

---

## 2. BUSINESS RULES - PHÂN LOẠI SHOP

### 2.1. Shop Score Calculation

#### BR-COMP-001: Công thức tính Shop Score

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-001 |
| **Tên** | Shop Score Calculation |
| **Loại** | Computation |
| **Priority** | P1 - Critical |
| **Mô tả** | Tính điểm tin cậy của shop dựa trên nhiều tiêu chí |

**Công thức:**

```
Shop_Score = (Rating_Score × 0.25) +
             (Review_Score × 0.15) +
             (Sales_Score × 0.20) +
             (Response_Score × 0.10) +
             (Success_Score × 0.15) +
             (Tenure_Score × 0.10) +
             (Badge_Score × 0.05)
```

**Trọng số chi tiết:**

| Thành phần | Trọng số | Mô tả |
|------------|----------|-------|
| Rating_Score | 25% | Điểm đánh giá trung bình |
| Review_Score | 15% | Số lượng đánh giá |
| Sales_Score | 20% | Số lượng sản phẩm đã bán |
| Response_Score | 10% | Tỷ lệ phản hồi chat |
| Success_Score | 15% | Tỷ lệ đơn hàng thành công |
| Tenure_Score | 10% | Thời gian tham gia |
| Badge_Score | 5% | Badge từ sàn TMĐT |

---

#### BR-COMP-002: Rating Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-002 |
| **Tên** | Rating Score |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Bảng quy đổi:**

| Rating | Score |
|--------|-------|
| 5.0 | 100 |
| 4.8 - 4.9 | 90 |
| 4.5 - 4.7 | 75 |
| 4.0 - 4.4 | 50 |
| < 4.0 | 25 |

**Pseudocode:**

```javascript
function calculateRatingScore(rating) {
  if (rating === 5.0) return 100;
  if (rating >= 4.8) return 90;
  if (rating >= 4.5) return 75;
  if (rating >= 4.0) return 50;
  return 25;
}
```

---

#### BR-COMP-003: Review Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-003 |
| **Tên** | Review Score |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Bảng quy đổi:**

| Số lượng đánh giá | Score |
|-------------------|-------|
| >= 10,000 | 100 |
| 5,000 - 9,999 | 80 |
| 1,000 - 4,999 | 60 |
| 500 - 999 | 40 |
| 100 - 499 | 20 |
| < 100 | 10 |

---

#### BR-COMP-004: Sales Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-004 |
| **Tên** | Sales Score |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Bảng quy đổi:**

| Số sản phẩm đã bán | Score |
|--------------------|-------|
| >= 100,000 | 100 |
| 50,000 - 99,999 | 85 |
| 10,000 - 49,999 | 70 |
| 5,000 - 9,999 | 50 |
| 1,000 - 4,999 | 30 |
| < 1,000 | 15 |

---

#### BR-COMP-005: Response Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-005 |
| **Tên** | Response Score |
| **Loại** | Computation |
| **Priority** | P2 - High |

**Bảng quy đổi:**

| Tỷ lệ phản hồi | Score |
|----------------|-------|
| >= 95% | 100 |
| 90% - 94% | 80 |
| 80% - 89% | 60 |
| 70% - 79% | 40 |
| < 70% | 20 |

---

#### BR-COMP-006: Success Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-006 |
| **Tên** | Success Score |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Bảng quy đổi:**

| Tỷ lệ đơn thành công | Score |
|----------------------|-------|
| >= 98% | 100 |
| 95% - 97% | 85 |
| 90% - 94% | 70 |
| 85% - 89% | 50 |
| < 85% | 25 |

---

#### BR-COMP-007: Tenure Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-007 |
| **Tên** | Tenure Score |
| **Loại** | Computation |
| **Priority** | P2 - High |

**Bảng quy đổi:**

| Thời gian tham gia | Score |
|--------------------|-------|
| >= 3 năm | 100 |
| 1 - 3 năm | 75 |
| 6 - 12 tháng | 50 |
| 3 - 6 tháng | 30 |
| < 3 tháng | 10 |

---

#### BR-COMP-008: Badge Score Calculation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-008 |
| **Tên** | Badge Score |
| **Loại** | Computation |
| **Priority** | P2 - High |

**Bảng quy đổi:**

| Badge | Score |
|-------|-------|
| Official/Mall | 100 |
| Preferred/Yêu thích | 70 |
| No badge | 30 |

---

### 2.2. Shop Classification Rules

#### BR-INF-001: Phân loại Shop Mall

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-001 |
| **Tên** | Shop Mall Classification |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF Shop_Score >= 80 AND has_mall_badge = TRUE
THEN shop_type = 'MALL'
```

**Tiêu chí bắt buộc:**
- Có badge "Mall" hoặc "Official" từ sàn TMĐT
- Rating >= 4.7/5.0
- Số lượng đánh giá >= 1,000
- Số sản phẩm đã bán >= 10,000
- Tỷ lệ phản hồi >= 90%
- Tỷ lệ đơn thành công >= 95%
- Thời gian tham gia >= 6 tháng

---

#### BR-INF-002: Phân loại Shop Yêu thích

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-002 |
| **Tên** | Shop Preferred Classification |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF Shop_Score >= 60 AND Shop_Score < 80
THEN shop_type = 'PREFERRED'
```

**Tiêu chí:**
- Rating >= 4.5/5.0
- Số lượng đánh giá >= 500
- Số sản phẩm đã bán >= 5,000
- Tỷ lệ phản hồi >= 80%
- Tỷ lệ đơn thành công >= 90%
- Thời gian tham gia >= 3 tháng

---

#### BR-INF-003: Phân loại Shop Rủi ro

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-003 |
| **Tên** | Shop Risky Classification |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF Shop_Score < 60
THEN shop_type = 'RISKY'
```

**Dấu hiệu nhận diện (ít nhất 2 điều kiện):**
- Rating < 4.5/5.0
- Số lượng đánh giá < 100
- Số sản phẩm đã bán < 1,000
- Tỷ lệ phản hồi < 70%
- Tỷ lệ đơn thành công < 85%
- Thời gian tham gia < 1 tháng
- Đánh giá 1-2 sao > 15%
- Tỷ lệ hoàn tiền/khiếu nại > 10%

---

#### BR-ACT-001: Tự động nâng/hạ hạng Shop

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-ACT-001 |
| **Tên** | Shop Rank Transition |
| **Loại** | Action |
| **Priority** | P2 - High |

**Quy tắc chuyển đổi:**

| Từ | Sang | Điều kiện |
|----|------|-----------|
| RISKY | PREFERRED | Score >= 60 |
| PREFERRED | MALL | Score >= 80 AND has_badge |
| MALL | PREFERRED | Score < 80 OR lost_badge |
| PREFERRED | RISKY | Score < 60 |

**Hành động kèm theo:**
- Cập nhật shop_type trong database
- Ghi log thay đổi
- Gửi notification cho user theo dõi shop

---

## 3. BUSINESS RULES - PRICE COMPARISON

### 3.1. Price Calculation

#### BR-COMP-010: Tính tổng giá cuối cùng

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-010 |
| **Tên** | Final Price Calculation |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Công thức:**

```
Final_Price = Current_Price - Voucher_Discount + Shipping_Fee
```

**Các thành phần:**
- `Current_Price`: Giá sản phẩm sau khuyến mãi
- `Voucher_Discount`: Giảm giá từ voucher/coupon
- `Shipping_Fee`: Phí vận chuyển

---

#### BR-COMP-011: Tính % giảm giá

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-011 |
| **Tên** | Discount Percentage |
| **Loại** | Computation |
| **Priority** | P1 - Critical |

**Công thức:**

```
Discount_Percentage = ((Original_Price - Current_Price) / Original_Price) × 100
```

---

#### BR-COMP-012: Tính điểm tổng hợp sản phẩm

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-COMP-012 |
| **Tên** | Product Composite Score |
| **Loại** | Computation |
| **Priority** | P2 - High |

**Công thức:**

```
Composite_Score = (Price_Score × 0.50) +
                  (Rating_Score × 0.25) +
                  (Shop_Trust_Score × 0.15) +
                  (Sales_Score × 0.10)
```

**Giải thích:**
- `Price_Score`: Điểm giá (giá thấp = điểm cao)
- `Rating_Score`: Điểm đánh giá sản phẩm
- `Shop_Trust_Score`: Điểm tin cậy shop (từ BR-COMP-001)
- `Sales_Score`: Điểm dựa trên số lượng bán

---

### 3.2. Product Matching

#### BR-INF-010: Exact Product Matching

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-010 |
| **Tên** | Exact Product Matching |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF (product_name_A === product_name_B) OR
   (sku_A === sku_B) OR
   (barcode_A === barcode_B)
THEN similarity = 100%
     match_type = 'EXACT'
```

---

#### BR-INF-011: Fuzzy Product Matching

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-011 |
| **Tên** | Fuzzy Product Matching |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
similarity = max(
  levenshtein_similarity(name_A, name_B),
  cosine_similarity(tfidf(name_A), tfidf(name_B)),
  jaccard_similarity(tokens(name_A), tokens(name_B))
)

IF similarity >= 85%
THEN match_type = 'SAME_PRODUCT'
ELSE IF similarity >= 70%
THEN match_type = 'SIMILAR_PRODUCT'
ELSE match_type = 'DIFFERENT_PRODUCT'
```

---

#### BR-CONS-010: Ngưỡng matching sản phẩm

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-CONS-010 |
| **Tên** | Matching Threshold |
| **Loại** | Constraint |
| **Priority** | P1 - Critical |

**Ngưỡng:**

| Độ tương đồng | Kết luận |
|---------------|----------|
| >= 95% | Exact match |
| 85% - 94% | Same product |
| 70% - 84% | Similar product |
| < 70% | Different product |

---

## 4. BUSINESS RULES - PRICE ALERT

### 4.1. Alert Conditions

#### BR-INF-020: Price Drop Alert

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-020 |
| **Tên** | Price Drop Alert |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF current_price <= target_price
THEN trigger_alert = TRUE
     alert_type = 'PRICE_DROP'
     message = "Giá đã giảm xuống {current_price}"
```

---

#### BR-INF-021: Percentage Drop Alert

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-021 |
| **Tên** | Percentage Drop Alert |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
IF discount_percentage >= target_percentage
THEN trigger_alert = TRUE
     alert_type = 'PERCENTAGE_DROP'
     message = "Giảm giá {discount_percentage}%"
```

---

#### BR-INF-022: Best Price Alert

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-022 |
| **Tên** | Best Price Alert |
| **Loại** | Inference |
| **Priority** | P1 - Critical |

**Điều kiện:**

```
min_price_N_days = MIN(price) FROM price_history WHERE recorded_at >= NOW() - N_DAYS

IF current_price <= min_price_N_days
THEN trigger_alert = TRUE
     alert_type = 'BEST_PRICE'
     message = "Giá tốt nhất trong {N} ngày"
```

---

#### BR-INF-023: Flash Sale Alert

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-023 |
| **Tên** | Flash Sale Alert |
| **Loại** | Inference |
| **Priority** | P2 - High |

**Điều kiện:**

```
IF event_tag = 'FLASH_SALE' AND product IN user_watchlist
THEN trigger_alert = TRUE
     alert_type = 'FLASH_SALE'
     message = "Flash Sale bắt đầu!"
```

---

#### BR-INF-024: Cross Platform Price Alert

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-INF-024 |
| **Tên** | Cross Platform Alert |
| **Loại** | Inference |
| **Priority** | P2 - High |

**Điều kiện:**

```
IF price_platform_A < (price_platform_B × (1 - threshold))
THEN trigger_alert = TRUE
     alert_type = 'CROSS_PLATFORM'
     message = "{Platform_A} rẻ hơn {Platform_B} {difference}đ"
```

---

### 4.2. Alert Rate Limiting

#### BR-CONS-020: Alert Cooldown

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-CONS-020 |
| **Tên** | Alert Cooldown Period |
| **Loại** | Constraint |
| **Priority** | P2 - High |

**Quy tắc:**

```
Không gửi alert trùng lặp trong khoảng thời gian cooldown.

Cooldown period:
- PRICE_DROP: 6 giờ
- PERCENTAGE_DROP: 6 giờ
- BEST_PRICE: 24 giờ
- FLASH_SALE: Không cooldown
```

---

#### BR-CONS-021: Daily Alert Limit

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-CONS-021 |
| **Tên** | Daily Alert Limit |
| **Loại** | Constraint |
| **Priority** | P3 - Medium |

**Quy tắc:**

| User Tier | Max Alerts/Day |
|-----------|----------------|
| Free | 10 |
| Premium | Unlimited |

---

## 5. BUSINESS RULES - DATA CRAWLING

### 5.1. Crawl Scheduling

#### BR-ACT-030: Crawl Frequency by Product Type

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-ACT-030 |
| **Tên** | Crawl Frequency Rules |
| **Loại** | Action |
| **Priority** | P1 - Critical |

**Quy tắc:**

| Loại sản phẩm | Tần suất | Cron Expression |
|---------------|----------|-----------------|
| Hot/Trending | 1-2 giờ | `0 */1 * * *` |
| Thông thường | 6-12 giờ | `0 */6 * * *` |
| Ít biến động | 24 giờ | `0 0 * * *` |
| Flash Sale Event | 30 phút | `*/30 * * * *` |

---

#### BR-ACT-031: Shop Score Update Frequency

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-ACT-031 |
| **Tên** | Shop Score Update Frequency |
| **Loại** | Action |
| **Priority** | P2 - High |

**Quy tắc:**

| Shop Type | Update Frequency |
|-----------|------------------|
| MALL | Mỗi tuần |
| PREFERRED | Mỗi 3 ngày |
| RISKY | Mỗi ngày |

---

### 5.2. Data Validation

#### BR-VAL-030: Price Validation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-VAL-030 |
| **Tên** | Price Validation |
| **Loại** | Validation |
| **Priority** | P1 - Critical |

**Quy tắc:**

```
1. price > 0
2. price <= 1,000,000,000 (1 tỷ VNĐ)
3. current_price <= original_price
4. discount_percentage >= 0 AND <= 100
5. shipping_fee >= 0
```

---

#### BR-VAL-031: Shop Data Validation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-VAL-031 |
| **Tên** | Shop Data Validation |
| **Loại** | Validation |
| **Priority** | P1 - Critical |

**Quy tắc:**

```
1. rating >= 0 AND rating <= 5.0
2. response_rate >= 0 AND response_rate <= 100
3. success_rate >= 0 AND success_rate <= 100
4. total_sold >= 0
5. review_count >= 0
6. follower_count >= 0
```

---

#### BR-VAL-032: Anomaly Detection

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-VAL-032 |
| **Tên** | Price Anomaly Detection |
| **Loại** | Validation |
| **Priority** | P2 - High |

**Quy tắc:**

```
avg_price = AVG(price) FROM price_history WHERE recorded_at >= NOW() - 7 DAYS
std_dev = STDDEV(price) FROM price_history WHERE recorded_at >= NOW() - 7 DAYS

IF ABS(new_price - avg_price) > (3 × std_dev)
THEN flag_as_anomaly = TRUE
     require_manual_review = TRUE
```

---

## 6. BUSINESS RULES - USER MANAGEMENT

### 6.1. User Tier Limits

#### BR-CONS-040: Free User Limits

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-CONS-040 |
| **Tên** | Free User Limits |
| **Loại** | Constraint |
| **Priority** | P1 - Critical |

**Giới hạn:**

| Feature | Free Tier | Premium Tier |
|---------|-----------|--------------|
| Watchlist products | 10 | Unlimited |
| Price alerts | 5 | Unlimited |
| Price history | 30 ngày | 1 năm |
| Export data | Không | Có |
| Ads | Có | Không |

---

#### BR-CONS-041: API Rate Limiting

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-CONS-041 |
| **Tên** | API Rate Limiting |
| **Loại** | Constraint |
| **Priority** | P1 - Critical |

**Giới hạn:**

| User Type | Requests/Minute | Requests/Day |
|-----------|-----------------|--------------|
| Guest | 30 | 500 |
| Free User | 60 | 2,000 |
| Premium User | 120 | 10,000 |
| Admin | Unlimited | Unlimited |

---

### 6.2. Authentication Rules

#### BR-VAL-040: Password Requirements

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-VAL-040 |
| **Tên** | Password Requirements |
| **Loại** | Validation |
| **Priority** | P1 - Critical |

**Quy tắc:**

```
1. Độ dài tối thiểu: 8 ký tự
2. Chứa ít nhất 1 chữ hoa
3. Chứa ít nhất 1 chữ thường
4. Chứa ít nhất 1 số
5. Không chứa email hoặc tên người dùng
```

**Regex:**

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$
```

---

#### BR-VAL-041: Email Validation

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-VAL-041 |
| **Tên** | Email Validation |
| **Loại** | Validation |
| **Priority** | P1 - Critical |

**Quy tắc:**

```
1. Email format hợp lệ (RFC 5322)
2. Domain tồn tại (MX record check)
3. Không trùng lặp trong hệ thống
4. Không phải disposable email
```

---

## 7. BUSINESS RULES - CACHING

#### BR-ACT-050: Cache TTL Rules

| Thuộc tính | Giá trị |
|------------|---------|
| **Rule ID** | BR-ACT-050 |
| **Tên** | Cache Time-To-Live |
| **Loại** | Action |
| **Priority** | P2 - High |

**Quy tắc:**

| Data Type | Cache TTL |
|-----------|-----------|
| Search results | 5 phút |
| Product details | 15 phút |
| Price comparison | 10 phút |
| Price history chart | 30 phút |
| Shop info | 1 giờ |
| Category list | 24 giờ |

---

## 8. SUMMARY - BẢNG TÓM TẮT

### 8.1. Danh sách Business Rules

| Rule ID | Tên | Loại | Priority |
|---------|-----|------|----------|
| BR-COMP-001 | Shop Score Calculation | Computation | P1 |
| BR-COMP-002 | Rating Score | Computation | P1 |
| BR-COMP-003 | Review Score | Computation | P1 |
| BR-COMP-004 | Sales Score | Computation | P1 |
| BR-COMP-005 | Response Score | Computation | P2 |
| BR-COMP-006 | Success Score | Computation | P1 |
| BR-COMP-007 | Tenure Score | Computation | P2 |
| BR-COMP-008 | Badge Score | Computation | P2 |
| BR-COMP-010 | Final Price Calculation | Computation | P1 |
| BR-COMP-011 | Discount Percentage | Computation | P1 |
| BR-COMP-012 | Product Composite Score | Computation | P2 |
| BR-INF-001 | Shop Mall Classification | Inference | P1 |
| BR-INF-002 | Shop Preferred Classification | Inference | P1 |
| BR-INF-003 | Shop Risky Classification | Inference | P1 |
| BR-INF-010 | Exact Product Matching | Inference | P1 |
| BR-INF-011 | Fuzzy Product Matching | Inference | P1 |
| BR-INF-020 | Price Drop Alert | Inference | P1 |
| BR-INF-021 | Percentage Drop Alert | Inference | P1 |
| BR-INF-022 | Best Price Alert | Inference | P1 |
| BR-INF-023 | Flash Sale Alert | Inference | P2 |
| BR-INF-024 | Cross Platform Alert | Inference | P2 |
| BR-ACT-001 | Shop Rank Transition | Action | P2 |
| BR-ACT-030 | Crawl Frequency Rules | Action | P1 |
| BR-ACT-031 | Shop Score Update Frequency | Action | P2 |
| BR-ACT-050 | Cache TTL Rules | Action | P2 |
| BR-CONS-010 | Matching Threshold | Constraint | P1 |
| BR-CONS-020 | Alert Cooldown | Constraint | P2 |
| BR-CONS-021 | Daily Alert Limit | Constraint | P3 |
| BR-CONS-040 | Free User Limits | Constraint | P1 |
| BR-CONS-041 | API Rate Limiting | Constraint | P1 |
| BR-VAL-030 | Price Validation | Validation | P1 |
| BR-VAL-031 | Shop Data Validation | Validation | P1 |
| BR-VAL-032 | Anomaly Detection | Validation | P2 |
| BR-VAL-040 | Password Requirements | Validation | P1 |
| BR-VAL-041 | Email Validation | Validation | P1 |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
