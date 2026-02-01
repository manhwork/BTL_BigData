# BỔ SUNG: PHÂN LOẠI SHOP (SHOP CLASSIFICATION)

## Tổng quan

Đã bổ sung tính năng **Phân loại Shop** vào nghiệp vụ dự án so sánh giá sản phẩm. Tính năng này giúp người dùng đánh giá độ tin cậy của người bán trước khi mua hàng.

---

## 3 Loại Shop

### 🏢 Shop Mall (Official Store)

- **Màu sắc:** 🟢 Xanh lá - Tin cậy cao
- **Tiêu chí:**
    - Có badge "Mall" hoặc "Official"
    - Rating >= 4.7/5.0
    - Số đánh giá >= 1,000
    - Đã bán >= 10,000 sản phẩm
    - Tỷ lệ phản hồi >= 90%
    - Tỷ lệ thành công >= 95%

### ⭐ Shop Yêu thích (Preferred Shop)

- **Màu sắc:** 🟡 Vàng - Tin cậy trung bình
- **Tiêu chí:**
    - Rating >= 4.5/5.0
    - Số đánh giá >= 500
    - Đã bán >= 5,000 sản phẩm
    - Tỷ lệ phản hồi >= 80%
    - Tỷ lệ thành công >= 90%

### ⚠️ Shop Rủi ro (Risky Shop)

- **Màu sắc:** 🔴 Đỏ - Cần cẩn trọng
- **Tiêu chí:** Thỏa mãn ít nhất 2 điều kiện:
    - Rating < 4.5/5.0
    - Số đánh giá < 100
    - Đã bán < 1,000 sản phẩm
    - Tỷ lệ phản hồi < 70%
    - Tỷ lệ thành công < 85%
    - Thời gian tham gia < 1 tháng

---

## Thuật toán Scoring

```
Shop Score = (Rating_Score × 0.25) +
             (Review_Score × 0.15) +
             (Sales_Score × 0.20) +
             (Response_Score × 0.10) +
             (Success_Score × 0.15) +
             (Tenure_Score × 0.10) +
             (Badge_Score × 0.05)
```

**Phân loại:**

- Shop Mall: Score >= 80 VÀ có Official/Mall badge
- Shop Yêu thích: Score >= 60 VÀ < 80
- Shop Rủi ro: Score < 60

---

## Thay đổi Database

### Bảng mới: `sellers`

```sql
sellers:
  - id (PK)
  - platform
  - platform_seller_id
  - seller_name
  - seller_rating
  - response_rate
  - success_rate
  - positive_review_rate
  - return_rate
  - has_mall_badge
  - has_preferred_badge
  - shop_type (mall, preferred, risky)
  - shop_score (0-100)
  - last_score_updated_at
  ...
```

### Cập nhật bảng `product_listings`

- Thêm: `seller_id (FK)` - liên kết đến bảng sellers
- Xóa: `seller_name`, `seller_rating` (chuyển sang bảng sellers)

---

## API Endpoints mới

```
GET    /api/sellers                     - Danh sách shop
GET    /api/sellers/:id                 - Chi tiết shop
GET    /api/sellers/:id/products        - Sản phẩm của shop
GET    /api/sellers/:id/stats           - Thống kê shop
GET    /api/sellers/mall                - Danh sách Shop Mall
GET    /api/sellers/preferred           - Danh sách Shop Yêu thích
GET    /api/sellers/search              - Tìm kiếm shop
POST   /api/sellers/:id/recalculate     - Tính lại điểm shop (admin)
```

---

## Tính năng UI/UX

### 1. Hiển thị Badge

- 🏢 **MALL** - Nền xanh lá, chữ trắng
- ⭐ **YÊU THÍCH** - Nền vàng, chữ đen
- ⚠️ **RỦI RO** - Nền đỏ, chữ trắng

### 2. Cảnh báo tự động

Khi xem sản phẩm từ Shop Rủi ro:

```
⚠️ CẢNH BÁO
Shop này được đánh giá là "Rủi ro"

Khuyến nghị:
✓ Đọc kỹ đánh giá từ người mua
✓ Kiểm tra chính sách đổi trả
✓ Ưu tiên thanh toán COD
```

### 3. Gợi ý thay thế

Nếu sản phẩm có ở shop uy tín hơn:

```
💡 GỢI Ý TỐT HƠN
Sản phẩm này có sẵn tại shop uy tín hơn:

🏢 ABC Official Store (Shop Mall)
   Giá: 1,200,000đ (+250,000đ)
   [Xem ngay]
```

### 4. Bộ lọc

- ☑️ Chỉ hiển thị Shop Mall
- ☑️ Chỉ hiển thị Shop Yêu thích
- ☑️ Ẩn Shop Rủi ro
- ☑️ Hiển thị tất cả

### 5. Sắp xếp

- Ưu tiên Shop Mall trước
- Theo điểm tin cậy (cao → thấp)
- Theo loại shop (Mall → Yêu thích → Rủi ro)

---

## Cập nhật tự động

### Tần suất

- Shop Mall: Mỗi tuần
- Shop Yêu thích: Mỗi 3 ngày
- Shop Rủi ro: Mỗi ngày

### Nâng/Hạ hạng

- Shop Rủi ro → Shop Yêu thích: Khi đạt điểm >= 60
- Shop Yêu thích → Shop Mall: Khi đạt điểm >= 80 VÀ có badge
- Shop Mall → Shop Yêu thích: Khi mất badge hoặc điểm < 80
- Shop Yêu thích → Shop Rủi ro: Khi điểm < 60

### Thông báo

Người dùng nhận thông báo khi shop trong watchlist thay đổi hạng.

---

## Lợi ích

### Cho người dùng

✅ Đánh giá nhanh độ tin cậy của shop  
✅ Giảm rủi ro mua hàng kém chất lượng  
✅ Tìm được shop uy tín với giá tốt  
✅ Nhận cảnh báo kịp thời

### Cho hệ thống

✅ Tăng giá trị cho người dùng  
✅ Khác biệt hóa với đối thủ  
✅ Tăng độ tin cậy của nền tảng  
✅ Dữ liệu phong phú cho phân tích

---

## Vị trí trong tài liệu

Phần **2.2. Phân loại Shop** đã được thêm vào file `NGHIEP_VU_DU_AN.md`:

- Sau phần **2.1. Thu thập dữ liệu sản phẩm**
- Trước phần **2.3. So sánh giá sản phẩm**

Các phần khác đã được đánh số lại:

- 2.2 → 2.3: So sánh giá sản phẩm
- 2.3 → 2.4: Theo dõi biến động giá
- 2.4 → 2.5: Cảnh báo giá tốt
- 2.5 → 2.6: Tìm kiếm và lọc
- 2.6 → 2.7: Báo cáo và thống kê

---

**Ngày cập nhật:** 2026-01-23  
**Phiên bản:** 1.1
