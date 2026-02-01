# 06. STATE TRANSITION DIAGRAM (VÒNG ĐỜI THỰC THỂ - STATE MACHINE)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. TỔNG QUAN

### 1.1. Danh sách State Machines

| Entity | Số States | Mô tả |
|--------|-----------|-------|
| User Account | 5 | Vòng đời tài khoản người dùng |
| Shop Classification | 3 | Phân loại độ tin cậy shop |
| Product Listing | 4 | Trạng thái sản phẩm trên sàn |
| Price Alert | 5 | Vòng đời cảnh báo giá |
| Crawl Job | 6 | Trạng thái job crawl dữ liệu |
| Notification | 4 | Vòng đời thông báo |

---

## 2. USER ACCOUNT STATE MACHINE

### 2.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER ACCOUNT STATE MACHINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ register                               │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │   PENDING     │                                 │
│                           │ (Chờ xác thực)│                                 │
│                           └───────┬───────┘                                 │
│                                   │                                         │
│                    ┌──────────────┼──────────────┐                          │
│                    │              │              │                          │
│           verify_email    resend_email   verification_expired               │
│                    │              │              │                          │
│                    ▼              │              ▼                          │
│           ┌───────────────┐      │      ┌───────────────┐                  │
│           │    ACTIVE     │◀─────┘      │   EXPIRED     │                  │
│           │  (Hoạt động)  │             │(Hết hạn xác thực)│                │
│           └───────┬───────┘             └───────┬───────┘                  │
│                   │                             │                          │
│        ┌──────────┼──────────┐                  │ re_register              │
│        │          │          │                  │                          │
│    upgrade   deactivate   ban                   │                          │
│    downgrade     │          │                   │                          │
│        │         ▼          │                   │                          │
│        │  ┌───────────────┐ │                   │                          │
│        │  │   INACTIVE    │ │                   │                          │
│        │  │ (Tạm ngưng)   │ │                   │                          │
│        │  └───────┬───────┘ │                   │                          │
│        │          │         │                   │                          │
│        │    reactivate      │                   │                          │
│        │          │         ▼                   │                          │
│        │          │  ┌───────────────┐          │                          │
│        │          │  │    BANNED     │          │                          │
│        │          │  │   (Bị cấm)    │          │                          │
│        │          │  └───────┬───────┘          │                          │
│        │          │          │                  │                          │
│        │          │     unban│                  │                          │
│        │          │          │                  │                          │
│        └──────────┴──────────┴──────────────────┘                          │
│                              │                                              │
│                              ▼                                              │
│                       ┌───────────┐                                         │
│                       │  DELETED  │                                         │
│                       │  (Đã xóa) │                                         │
│                       └───────────┘                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2. State Definitions

| State | Code | Mô tả | Allowed Actions |
|-------|------|-------|-----------------|
| PENDING | PEN | Đã đăng ký, chờ xác thực email | verify_email, resend_email |
| ACTIVE | ACT | Tài khoản đang hoạt động | login, use_features, upgrade, deactivate |
| INACTIVE | INA | Tạm ngưng bởi user | reactivate |
| BANNED | BAN | Bị admin cấm | appeal (qua support) |
| EXPIRED | EXP | Hết hạn xác thực email (72h) | re_register |
| DELETED | DEL | Đã xóa vĩnh viễn | N/A |

### 2.3. Transitions

| From | To | Trigger | Guard Condition | Action |
|------|-----|---------|-----------------|--------|
| - | PENDING | register | email unique | Tạo user, gửi email xác thực |
| PENDING | ACTIVE | verify_email | token valid & not expired | Cập nhật email_verified = true |
| PENDING | EXPIRED | auto (72h) | created_at + 72h < now | Mark as expired |
| ACTIVE | INACTIVE | deactivate | user request | Set is_active = false |
| ACTIVE | BANNED | ban | admin action | Set status = BANNED, log reason |
| INACTIVE | ACTIVE | reactivate | user request + login | Set is_active = true |
| BANNED | ACTIVE | unban | admin action | Remove ban, log action |
| EXPIRED | PENDING | re_register | same email | Reset verification token |
| * | DELETED | delete | admin or GDPR request | Soft delete, anonymize data |

---

## 3. SHOP CLASSIFICATION STATE MACHINE

### 3.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SHOP CLASSIFICATION STATE MACHINE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ create_shop                            │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │    RISKY      │                                 │
│                           │   (Rủi ro)    │                                 │
│                           │   🔴 Red      │                                 │
│                           │ Score < 60    │                                 │
│                           └───────┬───────┘                                 │
│                                   │                                         │
│                                   │ score >= 60                             │
│                                   ▼                                         │
│                           ┌───────────────┐                                 │
│         score < 60        │   PREFERRED   │    score >= 80                  │
│       ┌──────────────────▶│  (Yêu thích)  │◀──────────────┐                │
│       │                   │   🟡 Yellow   │    + no badge │                │
│       │                   │ 60 <= Score   │               │                │
│       │                   │    < 80       │               │                │
│       │                   └───────┬───────┘               │                │
│       │                           │                       │                │
│       │                           │ score >= 80           │                │
│       │                           │ + has_mall_badge      │                │
│       │                           ▼                       │                │
│       │                   ┌───────────────┐               │                │
│       │                   │     MALL      │───────────────┘                │
│       │                   │  (Chính hãng) │  lost_badge                    │
│       │                   │   🟢 Green    │  OR score < 80                 │
│       │                   │ Score >= 80   │                                │
│       │                   │ + Mall Badge  │                                │
│       │                   └───────────────┘                                │
│       │                           │                                        │
│       └───────────────────────────┘                                        │
│                          score < 60                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2. State Definitions

| State | Code | Color | Điều kiện | Trust Level |
|-------|------|-------|-----------|-------------|
| RISKY | RSK | 🔴 Red | Score < 60 | Low |
| PREFERRED | PRF | 🟡 Yellow | 60 <= Score < 80 | Medium |
| MALL | MAL | 🟢 Green | Score >= 80 AND has_mall_badge | High |

### 3.3. Transitions

| From | To | Trigger | Guard Condition | Frequency |
|------|-----|---------|-----------------|-----------|
| - | RISKY | create | New shop (default) | On create |
| RISKY | PREFERRED | score_update | score >= 60 | Daily |
| PREFERRED | MALL | score_update | score >= 80 AND has_mall_badge | Every 3 days |
| MALL | PREFERRED | score_update | score < 80 OR lost_badge | Weekly |
| PREFERRED | RISKY | score_update | score < 60 | Every 3 days |
| MALL | RISKY | score_update | score < 60 | Weekly |

### 3.4. Score Calculation Trigger Events

| Event | Action |
|-------|--------|
| New review received | Recalculate review_score, rating_score |
| Sale completed | Recalculate sales_score, success_rate |
| Badge status changed | Recalculate badge_score, trigger reclassification |
| Monthly anniversary | Recalculate tenure_score |
| Response rate updated | Recalculate response_score |

---

## 4. PRODUCT LISTING STATE MACHINE

### 4.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PRODUCT LISTING STATE MACHINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ crawl_new_product                      │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │   AVAILABLE   │                                 │
│                           │  (Còn hàng)   │◀─────────────────────┐         │
│                           └───────┬───────┘                      │         │
│                                   │                              │         │
│              ┌────────────────────┼────────────────────┐         │         │
│              │                    │                    │         │         │
│         stock = 0          price_changed         stock > 0       │         │
│              │                    │              (restock)       │         │
│              ▼                    ▼                    │         │         │
│      ┌───────────────┐    ┌───────────────┐           │         │         │
│      │ OUT_OF_STOCK  │    │   AVAILABLE   │           │         │         │
│      │  (Hết hàng)   │    │ (Price Alert  │           │         │         │
│      │               │    │   Triggered)  │           │         │         │
│      └───────┬───────┘    └───────────────┘           │         │         │
│              │                                        │         │         │
│              │                                        │         │         │
│              └────────────────────┬───────────────────┘         │         │
│                                   │                             │         │
│                                   │ crawl_not_found             │         │
│                                   │ OR seller_removed           │         │
│                                   ▼                             │         │
│                           ┌───────────────┐                     │         │
│                           │   INACTIVE    │                     │         │
│                           │(Không hoạt động)                    │         │
│                           └───────┬───────┘                     │         │
│                                   │                             │         │
│                    ┌──────────────┼──────────────┐              │         │
│                    │              │              │              │         │
│              30_days_inactive   re_crawl_found  admin_remove    │         │
│                    │              │              │              │         │
│                    ▼              └──────────────┼──────────────┘         │
│            ┌───────────────┐                     │                        │
│            │   ARCHIVED    │                     │                        │
│            │   (Lưu trữ)   │◀────────────────────┘                        │
│            └───────────────┘                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2. State Definitions

| State | Code | Mô tả | Visible to User |
|-------|------|-------|-----------------|
| AVAILABLE | AVL | Còn hàng, có thể mua | ✅ Yes |
| OUT_OF_STOCK | OOS | Hết hàng tạm thời | ✅ Yes (với label) |
| INACTIVE | INA | Không tìm thấy khi crawl | ❌ No |
| ARCHIVED | ARC | Đã lưu trữ (>30 ngày inactive) | ❌ No |

### 4.3. Transitions

| From | To | Trigger | Guard Condition | Action |
|------|-----|---------|-----------------|--------|
| - | AVAILABLE | crawl_success | is_available = true | Create listing record |
| AVAILABLE | OUT_OF_STOCK | crawl_update | stock_quantity = 0 | Update, trigger "back_in_stock" alert listeners |
| OUT_OF_STOCK | AVAILABLE | crawl_update | stock_quantity > 0 | Trigger BACK_IN_STOCK alerts |
| AVAILABLE | INACTIVE | crawl_fail | 3 consecutive failures | Mark inactive |
| OUT_OF_STOCK | INACTIVE | crawl_fail | 3 consecutive failures | Mark inactive |
| INACTIVE | AVAILABLE | crawl_success | Product found again | Reactivate |
| INACTIVE | ARCHIVED | auto (30 days) | inactive_since + 30d < now | Archive old data |
| * | ARCHIVED | admin_action | Manual removal | Archive with reason |

---

## 5. PRICE ALERT STATE MACHINE

### 5.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRICE ALERT STATE MACHINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ create_alert                           │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │    ACTIVE     │◀───────────────┐               │
│                           │ (Đang theo dõi)│                │               │
│                           └───────┬───────┘                │               │
│                                   │                        │               │
│              ┌────────────────────┼────────────────────┐   │               │
│              │                    │                    │   │               │
│         user_pause        condition_met          user_resume               │
│              │                    │                    │   │               │
│              ▼                    ▼                    │   │               │
│      ┌───────────────┐    ┌───────────────┐           │   │               │
│      │    PAUSED     │    │  TRIGGERED    │───────────┘   │               │
│      │  (Tạm dừng)   │    │ (Đã kích hoạt)│               │               │
│      └───────┬───────┘    └───────┬───────┘               │               │
│              │                    │                       │               │
│              │                    │ send_notification     │               │
│              │                    ▼                       │               │
│              │            ┌───────────────┐               │               │
│              │            │     SENT      │               │               │
│              │            │  (Đã gửi)     │               │               │
│              │            └───────┬───────┘               │               │
│              │                    │                       │               │
│              │         ┌──────────┼──────────┐            │               │
│              │         │          │          │            │               │
│              │    one_time    recurring   cooldown_end    │               │
│              │         │          │          │            │               │
│              │         ▼          │          └────────────┘               │
│              │  ┌───────────────┐ │                                       │
│              │  │   COMPLETED   │ │                                       │
│              │  │  (Hoàn thành) │◀┴──────────────────────────────────────┐│
│              │  └───────────────┘                                        ││
│              │                                                           ││
│              └──────────────────────────────────────────────────────────▶││
│                              user_delete                                 ││
│                                                                          ││
│                                                                          ▼│
│                                                                  ┌───────────┐
│                                                                  │  DELETED  │
│                                                                  │  (Đã xóa) │
│                                                                  └───────────┘
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2. State Definitions

| State | Code | Mô tả | Checking Active |
|-------|------|-------|-----------------|
| ACTIVE | ACT | Đang theo dõi giá | ✅ Yes |
| PAUSED | PAU | Tạm dừng bởi user | ❌ No |
| TRIGGERED | TRG | Điều kiện đã đạt, đang gửi | ❌ No |
| SENT | SNT | Đã gửi thông báo | Depends |
| COMPLETED | CMP | Đã hoàn thành (one-time) | ❌ No |
| DELETED | DEL | Đã xóa | ❌ No |

### 5.3. Transitions

| From | To | Trigger | Guard Condition | Action |
|------|-----|---------|-----------------|--------|
| - | ACTIVE | create | User has permission | Create alert record |
| ACTIVE | PAUSED | user_pause | User action | Set is_active = false |
| PAUSED | ACTIVE | user_resume | User action | Set is_active = true |
| ACTIVE | TRIGGERED | condition_met | Alert condition = true | Prepare notification |
| TRIGGERED | SENT | send_notification | Notification sent | Log to alert_history |
| SENT | COMPLETED | - | alert_type = one_time | Mark completed |
| SENT | ACTIVE | cooldown_end | alert_type = recurring | Reset for next trigger |
| * | DELETED | user_delete | User/Admin action | Soft delete |

### 5.4. Alert Type Behavior

| Alert Type | After Trigger | Cooldown |
|------------|---------------|----------|
| PRICE_DROP | Return to ACTIVE | 6 hours |
| PERCENTAGE_DROP | Return to ACTIVE | 6 hours |
| BEST_PRICE | Return to ACTIVE | 24 hours |
| FLASH_SALE | COMPLETED (one-time) | N/A |
| BACK_IN_STOCK | COMPLETED (one-time) | N/A |

---

## 6. CRAWL JOB STATE MACHINE

### 6.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CRAWL JOB STATE MACHINE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ schedule_job                           │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │    PENDING    │                                 │
│                           │  (Đang chờ)   │                                 │
│                           └───────┬───────┘                                 │
│                                   │                                         │
│                                   │ worker_pickup                           │
│                                   ▼                                         │
│                           ┌───────────────┐                                 │
│                           │   RUNNING     │◀─────────────────┐             │
│                           │ (Đang chạy)   │                  │             │
│                           └───────┬───────┘                  │             │
│                                   │                          │             │
│              ┌────────────────────┼────────────────────┐     │             │
│              │                    │                    │     │             │
│           success             failure              timeout   │             │
│              │                    │                    │     │             │
│              ▼                    ▼                    ▼     │             │
│      ┌───────────────┐    ┌───────────────┐    ┌───────────────┐          │
│      │   COMPLETED   │    │    FAILED     │    │   TIMEOUT     │          │
│      │  (Hoàn thành) │    │  (Thất bại)   │    │ (Quá thời gian)│         │
│      └───────────────┘    └───────┬───────┘    └───────┬───────┘          │
│                                   │                    │                  │
│                                   │ retry_count < 3    │                  │
│                                   │                    │                  │
│                                   └────────────────────┴──────────────────┘
│                                              │                             │
│                                              │ retry_count >= 3            │
│                                              ▼                             │
│                                      ┌───────────────┐                     │
│                                      │    DEAD       │                     │
│                                      │(Không thể xử lý)│                   │
│                                      └───────────────┘                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2. State Definitions

| State | Code | Mô tả | Auto Retry |
|-------|------|-------|------------|
| PENDING | PEN | Đang chờ trong queue | N/A |
| RUNNING | RUN | Worker đang xử lý | N/A |
| COMPLETED | CMP | Hoàn thành thành công | N/A |
| FAILED | FAI | Thất bại (có thể retry) | ✅ Yes |
| TIMEOUT | TIM | Quá thời gian cho phép | ✅ Yes |
| DEAD | DED | Không thể xử lý sau nhiều lần retry | ❌ No |

### 6.3. Transitions

| From | To | Trigger | Guard Condition | Action |
|------|-----|---------|-----------------|--------|
| - | PENDING | schedule | Job created | Add to queue |
| PENDING | RUNNING | worker_pickup | Worker available | Start processing |
| RUNNING | COMPLETED | success | Data valid | Save data, update indexes |
| RUNNING | FAILED | error | Exception caught | Log error, increment retry |
| RUNNING | TIMEOUT | timeout | duration > max_duration | Kill job, retry |
| FAILED | RUNNING | retry | retry_count < 3 | Re-queue with backoff |
| TIMEOUT | RUNNING | retry | retry_count < 3 | Re-queue with backoff |
| FAILED | DEAD | - | retry_count >= 3 | Alert admin, log |
| TIMEOUT | DEAD | - | retry_count >= 3 | Alert admin, log |

### 6.4. Retry Policy

```javascript
const RETRY_CONFIG = {
  maxRetries: 3,
  backoffMultiplier: 2,
  initialDelay: 1000, // 1 second
  maxDelay: 60000, // 1 minute
};

function calculateDelay(retryCount) {
  const delay = RETRY_CONFIG.initialDelay * 
                Math.pow(RETRY_CONFIG.backoffMultiplier, retryCount);
  return Math.min(delay, RETRY_CONFIG.maxDelay);
}

// Retry delays: 1s, 2s, 4s
```

---

## 7. NOTIFICATION STATE MACHINE

### 7.1. State Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      NOTIFICATION STATE MACHINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                  │
│                              │  [START]  │                                  │
│                              └─────┬─────┘                                  │
│                                    │ create                                 │
│                                    ▼                                        │
│                           ┌───────────────┐                                 │
│                           │    PENDING    │                                 │
│                           │ (Chờ gửi)     │                                 │
│                           └───────┬───────┘                                 │
│                                   │                                         │
│                                   │ send                                    │
│                                   ▼                                         │
│                           ┌───────────────┐                                 │
│                           │     SENT      │                                 │
│                           │   (Đã gửi)    │                                 │
│                           └───────┬───────┘                                 │
│                                   │                                         │
│                    ┌──────────────┼──────────────┐                          │
│                    │              │              │                          │
│              user_read      auto_expire(30d)   delivery_failed              │
│                    │              │              │                          │
│                    ▼              ▼              ▼                          │
│           ┌───────────────┐                ┌───────────────┐                │
│           │     READ      │                │    FAILED     │                │
│           │   (Đã đọc)    │                │  (Gửi thất bại)│               │
│           └───────────────┘                └───────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2. State Definitions

| State | Code | Mô tả |
|-------|------|-------|
| PENDING | PEN | Đang chờ gửi |
| SENT | SNT | Đã gửi thành công |
| READ | RD | User đã đọc |
| FAILED | FAI | Gửi thất bại |

---

## 8. STATE MACHINE IMPLEMENTATION

### 8.1. Database Schema for State Tracking

```sql
-- Generic state history table
CREATE TABLE entity_state_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type VARCHAR(50) NOT NULL, -- 'user', 'shop', 'alert', etc.
  entity_id UUID NOT NULL,
  from_state VARCHAR(50),
  to_state VARCHAR(50) NOT NULL,
  trigger_event VARCHAR(100) NOT NULL,
  trigger_data JSONB,
  performed_by UUID, -- user_id or NULL for system
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_state_history_entity ON entity_state_history(entity_type, entity_id);
CREATE INDEX idx_state_history_time ON entity_state_history(created_at DESC);
```

### 8.2. State Machine Service (TypeScript)

```typescript
interface StateTransition<T extends string> {
  from: T | T[];
  to: T;
  event: string;
  guard?: (context: any) => boolean;
  action?: (context: any) => Promise<void>;
}

class StateMachine<T extends string> {
  constructor(
    private entityType: string,
    private initialState: T,
    private transitions: StateTransition<T>[],
  ) {}

  async transition(
    entityId: string,
    currentState: T,
    event: string,
    context: any = {},
  ): Promise<T> {
    const transition = this.transitions.find(
      t => (Array.isArray(t.from) ? t.from.includes(currentState) : t.from === currentState) 
           && t.event === event
    );

    if (!transition) {
      throw new Error(`Invalid transition: ${currentState} -> ${event}`);
    }

    if (transition.guard && !transition.guard(context)) {
      throw new Error(`Guard condition failed for: ${event}`);
    }

    if (transition.action) {
      await transition.action(context);
    }

    // Log state change
    await this.logStateChange(entityId, currentState, transition.to, event, context);

    return transition.to;
  }

  private async logStateChange(
    entityId: string,
    fromState: T,
    toState: T,
    event: string,
    context: any,
  ) {
    // Insert into entity_state_history
  }
}

// Usage
const shopStateMachine = new StateMachine<ShopType>(
  'shop',
  'RISKY',
  [
    {
      from: 'RISKY',
      to: 'PREFERRED',
      event: 'score_update',
      guard: (ctx) => ctx.newScore >= 60,
      action: async (ctx) => {
        await notifyWatchers(ctx.shopId, 'Shop upgraded to Preferred');
      },
    },
    {
      from: 'PREFERRED',
      to: 'MALL',
      event: 'score_update',
      guard: (ctx) => ctx.newScore >= 80 && ctx.hasMallBadge,
    },
    // ... more transitions
  ],
);
```

---

## 9. SUMMARY - BẢNG TÓM TẮT STATES

| Entity | States | Initial | Terminal |
|--------|--------|---------|----------|
| User Account | PENDING, ACTIVE, INACTIVE, BANNED, EXPIRED, DELETED | PENDING | DELETED |
| Shop Classification | RISKY, PREFERRED, MALL | RISKY | - (循环) |
| Product Listing | AVAILABLE, OUT_OF_STOCK, INACTIVE, ARCHIVED | AVAILABLE | ARCHIVED |
| Price Alert | ACTIVE, PAUSED, TRIGGERED, SENT, COMPLETED, DELETED | ACTIVE | COMPLETED, DELETED |
| Crawl Job | PENDING, RUNNING, COMPLETED, FAILED, TIMEOUT, DEAD | PENDING | COMPLETED, DEAD |
| Notification | PENDING, SENT, READ, FAILED | PENDING | READ, FAILED |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
