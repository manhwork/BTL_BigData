# QUY TẮC COMMIT (COMMIT CONVENTION)

## 📋 Mục đích

Tài liệu này định nghĩa quy tắc commit message cho dự án **So sánh giá sản phẩm TMĐT** nhằm:

- Duy trì lịch sử commit rõ ràng, dễ đọc
- Tự động tạo CHANGELOG
- Dễ dàng tìm kiếm và rollback
- Cải thiện collaboration trong team

---

## 🎯 Cấu trúc Commit Message

### Format cơ bản

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Ví dụ

```
feat(crawler): thêm crawler cho Shopee

- Implement Scrapy spider cho Shopee
- Xử lý pagination và anti-bot
- Lưu dữ liệu vào MongoDB

Closes #123
```

---

## 📌 1. TYPE (Loại commit)

### Các type chính

| Type         | Mô tả                                      | Ví dụ                                           |
| ------------ | ------------------------------------------ | ----------------------------------------------- |
| **feat**     | Tính năng mới                              | `feat(api): thêm endpoint so sánh giá`          |
| **fix**      | Sửa bug                                    | `fix(crawler): sửa lỗi parse giá Lazada`        |
| **docs**     | Cập nhật documentation                     | `docs(readme): cập nhật hướng dẫn cài đặt`      |
| **style**    | Format code (không ảnh hưởng logic)        | `style(api): format code theo ESLint`           |
| **refactor** | Refactor code (không thêm feature/fix bug) | `refactor(service): tối ưu hóa price matching`  |
| **perf**     | Cải thiện performance                      | `perf(db): thêm index cho bảng price_history`   |
| **test**     | Thêm/sửa test                              | `test(api): thêm unit test cho compare service` |
| **build**    | Thay đổi build system, dependencies        | `build(deps): update Scrapy to v2.11`           |
| **ci**       | Thay đổi CI/CD                             | `ci(gitlab): thêm auto deploy staging`          |
| **chore**    | Công việc maintenance                      | `chore(git): thêm .gitignore`                   |
| **revert**   | Revert commit trước đó                     | `revert: revert "feat(api): thêm endpoint"`     |

---

## 🎯 2. SCOPE (Phạm vi)

Scope xác định phần nào của dự án bị ảnh hưởng.

### Scopes cho dự án này

#### Backend

- `api` - API endpoints
- `service` - Business logic services
- `crawler` - Web crawling modules
- `db` - Database schema, migrations
- `queue` - Message queue (RabbitMQ/Kafka)
- `cache` - Redis caching
- `auth` - Authentication/Authorization
- `notification` - Email, SMS, Push notification

#### Frontend

- `ui` - UI components
- `page` - Pages/Views
- `store` - State management (Redux/Vuex)
- `router` - Routing
- `chart` - Charts và visualization

#### Data & Analytics

- `etl` - ETL pipelines
- `ml` - Machine Learning models
- `analytics` - Analytics và reporting

#### Infrastructure

- `docker` - Docker configuration
- `k8s` - Kubernetes
- `nginx` - Nginx configuration
- `monitoring` - Monitoring setup

#### General

- `config` - Configuration files
- `deps` - Dependencies
- `docs` - Documentation
- `test` - Testing

### Ví dụ với scope

```
feat(crawler): thêm crawler cho Tiki
fix(api): sửa lỗi pagination trong search endpoint
docs(readme): cập nhật hướng dẫn setup database
perf(cache): implement Redis caching cho product search
```

---

## ✍️ 3. SUBJECT (Tiêu đề)

### Quy tắc

- ✅ Viết bằng tiếng Việt có dấu (hoặc tiếng Anh nếu team quy định)
- ✅ Bắt đầu bằng động từ (thêm, sửa, xóa, cập nhật, tối ưu...)
- ✅ Không viết hoa chữ cái đầu
- ✅ Không kết thúc bằng dấu chấm
- ✅ Giới hạn 50-72 ký tự
- ✅ Mô tả ngắn gọn, súc tích

### ✅ Tốt

```
feat(api): thêm endpoint lấy lịch sử giá sản phẩm
fix(crawler): sửa lỗi timeout khi crawl Shopee
docs(api): cập nhật API documentation
```

### ❌ Không tốt

```
feat(api): Thêm endpoint.
fix: fix bug
update code
```

---

## 📝 4. BODY (Nội dung chi tiết)

### Quy tắc

- Tách biệt với subject bằng 1 dòng trống
- Giải thích **WHY** (tại sao) và **WHAT** (cái gì), không phải **HOW** (như thế nào)
- Sử dụng bullet points cho nhiều thay đổi
- Giới hạn 72 ký tự mỗi dòng

### Ví dụ

```
feat(crawler): thêm crawler cho TikTok Shop

- Implement Selenium crawler do TikTok Shop sử dụng heavy JavaScript
- Xử lý infinite scroll để lấy toàn bộ sản phẩm
- Thêm retry mechanism với exponential backoff
- Lưu dữ liệu vào staging area trước khi process

Crawler chạy mỗi 6 giờ và có thể handle tối đa 10k sản phẩm/lần.
```

---

## 🔗 5. FOOTER (Chân trang)

### Breaking Changes

Nếu commit có breaking changes (thay đổi không tương thích ngược):

```
feat(api): thay đổi format response của compare endpoint

BREAKING CHANGE: Response format đã thay đổi từ array sang object.
Trước: { "products": [...] }
Sau: { "data": { "products": [...] }, "meta": {...} }

Migration guide: https://docs.example.com/migration-v2
```

### Issue References

Liên kết với issue/ticket:

```
fix(crawler): sửa lỗi parse giá có ký tự đặc biệt

Closes #123
Refs #124, #125
```

**Keywords:**

- `Closes #123` - Đóng issue
- `Fixes #123` - Sửa issue
- `Refs #123` - Tham chiếu issue
- `Related to #123` - Liên quan đến issue

---

## 📚 Ví dụ đầy đủ

### Ví dụ 1: Feature mới

```
feat(api): thêm endpoint so sánh giá sản phẩm

- Implement GET /api/products/:id/compare
- Hỗ trợ filter theo platform (shopee, lazada, tiki)
- Tính toán điểm tổng hợp dựa trên giá, rating, trust score
- Cache kết quả trong 5 phút

Endpoint này cho phép user so sánh giá của cùng một sản phẩm
trên nhiều sàn TMĐT khác nhau.

Closes #45
```

### Ví dụ 2: Bug fix

```
fix(crawler): sửa lỗi parse giá khi có voucher

Trước đây crawler không xử lý được trường hợp giá có voucher
đi kèm, dẫn đến giá cuối cùng không chính xác.

- Thêm logic parse voucher discount
- Tính toán final_price = current_price - voucher_discount
- Thêm unit test cho edge cases

Fixes #67
```

### Ví dụ 3: Refactor

```
refactor(service): tối ưu hóa thuật toán matching sản phẩm

- Chuyển từ Levenshtein sang TF-IDF + Cosine similarity
- Giảm thời gian xử lý từ 2s xuống 200ms
- Tăng độ chính xác từ 85% lên 92%

Performance improvement đáng kể cho hệ thống.

Refs #89
```

### Ví dụ 4: Documentation

```
docs(readme): cập nhật hướng dẫn setup môi trường development

- Thêm hướng dẫn cài đặt Docker
- Cập nhật environment variables
- Thêm troubleshooting section
- Thêm link đến CONTRIBUTING.md
```

### Ví dụ 5: Performance

```
perf(db): thêm composite index cho bảng price_history

CREATE INDEX idx_product_platform_time
ON price_history(product_listing_id, recorded_at DESC);

Giảm query time từ 3s xuống 50ms cho endpoint lịch sử giá.

Closes #102
```

### Ví dụ 6: Breaking Change

```
feat(api): thay đổi cấu trúc response của search API

BREAKING CHANGE: Response format đã thay đổi để hỗ trợ pagination tốt hơn.

Trước:
{
  "products": [...],
  "total": 100
}

Sau:
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}

Migration: Cập nhật frontend để sử dụng response.data thay vì response.products

Closes #150
```

---

## 🚀 Best Practices

### 1. Commit thường xuyên

- ✅ Commit mỗi khi hoàn thành một đơn vị công việc nhỏ
- ✅ Mỗi commit nên tập trung vào một thay đổi duy nhất
- ❌ Tránh commit quá lớn với nhiều thay đổi không liên quan

### 2. Atomic Commits

Mỗi commit nên:

- Độc lập và hoàn chỉnh
- Có thể revert mà không ảnh hưởng logic khác
- Pass tests (nếu có)

### 3. Sử dụng Imperative Mood

```
✅ thêm feature X
✅ sửa bug Y
✅ cập nhật documentation

❌ đã thêm feature X
❌ đang sửa bug Y
❌ thêm feature X rồi
```

### 4. Tách biệt refactor và feature

```
❌ Không tốt:
feat(api): thêm endpoint mới và refactor code cũ

✅ Tốt:
refactor(api): tối ưu hóa code service
feat(api): thêm endpoint search sản phẩm
```

### 5. Test trước khi commit

```bash
# Chạy tests
npm test

# Chạy linter
npm run lint

# Commit
git add .
git commit -m "feat(api): thêm endpoint compare"
```

---

## 🛠️ Tools hỗ trợ

### 1. Commitizen

Giúp tạo commit message theo chuẩn:

```bash
# Cài đặt
npm install -g commitizen
npm install -g cz-conventional-changelog

# Sử dụng
git add .
git cz
```

### 2. Commitlint

Kiểm tra commit message:

```bash
# Cài đặt
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Tạo file commitlint.config.js
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Setup husky hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

### 3. Conventional Changelog

Tự động tạo CHANGELOG:

```bash
npm install -g conventional-changelog-cli
conventional-changelog -p angular -i CHANGELOG.md -s
```

---

## 📋 Checklist trước khi commit

- [ ] Code đã được test kỹ
- [ ] Đã chạy linter và fix warnings
- [ ] Commit message tuân thủ convention
- [ ] Đã xóa debug code, console.log
- [ ] Đã update documentation nếu cần
- [ ] Đã link issue/ticket nếu có
- [ ] Breaking changes đã được ghi chú rõ ràng

---

## 🎓 Tài liệu tham khảo

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

---

## 📞 Liên hệ

Nếu có thắc mắc về commit convention, liên hệ:

- Tech Lead: [email]
- Team Channel: [Slack/Discord]

---

**Version:** 1.0  
**Last Updated:** 2026-01-23  
**Maintainer:** Development Team
