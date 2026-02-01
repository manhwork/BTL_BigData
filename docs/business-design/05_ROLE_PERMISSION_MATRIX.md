# 05. ROLE & PERMISSION MATRIX (MA TRẬN PHÂN QUYỀN - RBAC)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. TỔNG QUAN HỆ THỐNG PHÂN QUYỀN

### 1.1. Mô hình RBAC (Role-Based Access Control)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RBAC MODEL                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌──────────────┐                               │
│                              │    USERS     │                               │
│                              └──────┬───────┘                               │
│                                     │                                       │
│                                     │ has                                   │
│                                     ▼                                       │
│                              ┌──────────────┐                               │
│                              │    ROLES     │                               │
│                              └──────┬───────┘                               │
│                                     │                                       │
│                                     │ contains                              │
│                                     ▼                                       │
│                           ┌──────────────────┐                              │
│                           │   PERMISSIONS    │                              │
│                           └──────────────────┘                              │
│                                     │                                       │
│              ┌──────────────────────┼──────────────────────┐                │
│              ▼                      ▼                      ▼                │
│      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│      │   RESOURCE   │      │    ACTION    │      │   SCOPE      │          │
│      │  (products,  │      │   (create,   │      │   (own,      │          │
│      │   alerts,    │      │    read,     │      │    all)      │          │
│      │   users)     │      │    update,   │      │              │          │
│      │              │      │    delete)   │      │              │          │
│      └──────────────┘      └──────────────┘      └──────────────┘          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2. Định nghĩa Roles

| Role ID | Tên Role | Mô tả | Mức độ |
|---------|----------|-------|--------|
| R001 | GUEST | Người dùng chưa đăng nhập | 0 |
| R002 | USER_FREE | Người dùng miễn phí | 1 |
| R003 | USER_PREMIUM | Người dùng trả phí | 2 |
| R004 | MODERATOR | Quản lý nội dung | 3 |
| R005 | ADMIN | Quản trị viên | 4 |
| R006 | SUPER_ADMIN | Quản trị cấp cao | 5 |
| R007 | SYSTEM | Hệ thống tự động | 99 |

---

## 2. MA TRẬN QUYỀN THEO CHỨC NĂNG

### 2.1. Module: Authentication & User Management

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| auth:register | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| auth:login | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| auth:logout | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| auth:refresh_token | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| auth:forgot_password | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| auth:reset_password | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| profile:read_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| profile:update_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| profile:delete_own | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| users:read_all | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| users:update_any | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| users:delete_any | ❌ | ❌ | ❌ | ❌ | 🔸 | ✅ |
| users:change_role | ❌ | ❌ | ❌ | ❌ | 🔸 | ✅ |
| users:ban | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |

**Chú thích:**
- ✅ Có quyền đầy đủ
- 🔸 Có quyền giới hạn
- ❌ Không có quyền

---

### 2.2. Module: Product & Search

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| products:search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| products:read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| products:compare | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| products:price_history_30d | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| products:price_history_90d | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| products:price_history_1y | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| products:export | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| products:create | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| products:update | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| products:delete | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| products:bulk_import | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.3. Module: Watchlist

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| watchlist:read_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| watchlist:create | ❌ | ✅ (max 10) | ✅ (∞) | ✅ | ✅ | ✅ |
| watchlist:delete_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| watchlist:read_any | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| watchlist:delete_any | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.4. Module: Price Alerts

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| alerts:read_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| alerts:create | ❌ | ✅ (max 5) | ✅ (∞) | ✅ | ✅ | ✅ |
| alerts:update_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| alerts:delete_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| alerts:read_any | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| alerts:delete_any | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| alerts:history_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| alerts:history_any | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.5. Module: Sellers/Shops

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| sellers:read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sellers:search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sellers:filter_by_type | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sellers:create | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| sellers:update | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| sellers:delete | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| sellers:recalculate_score | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| sellers:override_type | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.6. Module: Categories

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| categories:read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| categories:create | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| categories:update | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| categories:delete | ❌ | ❌ | ❌ | ❌ | 🔸 | ✅ |
| categories:reorder | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.7. Module: Analytics & Reports

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| analytics:personal_dashboard | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| analytics:price_trends | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| analytics:market_insights | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| analytics:advanced_reports | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| analytics:export_reports | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| analytics:system_stats | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |
| analytics:user_behavior | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| analytics:revenue | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

### 2.8. Module: Crawling & System

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| crawl:view_status | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| crawl:start_job | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| crawl:stop_job | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| crawl:config | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| crawl:view_logs | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| system:view_health | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| system:view_metrics | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| system:manage_cache | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| system:config | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| system:backup | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

### 2.9. Module: Notifications

| Permission | GUEST | USER_FREE | USER_PREMIUM | MODERATOR | ADMIN | SUPER_ADMIN |
|------------|:-----:|:---------:|:------------:|:---------:|:-----:|:-----------:|
| notifications:read_own | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| notifications:mark_read | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| notifications:preferences | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| notifications:send_global | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| notifications:send_targeted | ❌ | ❌ | ❌ | 🔸 | ✅ | ✅ |

---

## 3. GIỚI HẠN THEO TIER

### 3.1. Feature Limits

| Feature | GUEST | USER_FREE | USER_PREMIUM |
|---------|:-----:|:---------:|:------------:|
| Số sản phẩm Watchlist | 0 | 10 | ∞ |
| Số Price Alerts | 0 | 5 | ∞ |
| Lịch sử giá | 30 ngày | 30 ngày | 1 năm |
| Export dữ liệu | ❌ | ❌ | ✅ |
| Advanced Analytics | ❌ | ❌ | ✅ |
| Priority Notifications | ❌ | ❌ | ✅ |
| No Ads | ❌ | ❌ | ✅ |
| API Access | ❌ | ❌ | ✅ |

### 3.2. API Rate Limits

| User Type | Requests/Minute | Requests/Hour | Requests/Day |
|-----------|:---------------:|:-------------:|:------------:|
| GUEST | 30 | 300 | 500 |
| USER_FREE | 60 | 600 | 2,000 |
| USER_PREMIUM | 120 | 1,200 | 10,000 |
| ADMIN | 300 | 6,000 | ∞ |
| SYSTEM | ∞ | ∞ | ∞ |

---

## 4. PERMISSION INHERITANCE

### 4.1. Role Hierarchy

```
SUPER_ADMIN (Level 5)
    │
    └── inherits all from ↓
        │
        ADMIN (Level 4)
            │
            └── inherits all from ↓
                │
                MODERATOR (Level 3)
                    │
                    └── inherits all from ↓
                        │
                        USER_PREMIUM (Level 2)
                            │
                            └── inherits all from ↓
                                │
                                USER_FREE (Level 1)
                                    │
                                    └── inherits all from ↓
                                        │
                                        GUEST (Level 0)
```

### 4.2. Special Permissions

| Role | Special Permissions |
|------|---------------------|
| SUPER_ADMIN | - Có thể thay đổi role của bất kỳ user<br>- Có thể xóa bất kỳ dữ liệu<br>- Có thể truy cập system config |
| ADMIN | - Có thể thay đổi role (trừ SUPER_ADMIN)<br>- Có thể quản lý crawl jobs<br>- Có thể xem tất cả analytics |
| MODERATOR | - Có thể chỉnh sửa product/seller info<br>- Có thể ban user<br>- Có thể gửi notification |
| USER_PREMIUM | - Không giới hạn watchlist/alerts<br>- Truy cập advanced features<br>- Priority support |

---

## 5. PERMISSION IMPLEMENTATION

### 5.1. Database Schema

```sql
-- Roles table
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) NOT NULL UNIQUE,
  level INTEGER NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Permissions table
CREATE TABLE permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(100) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  resource VARCHAR(50) NOT NULL,
  action VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Role-Permission mapping
CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
  scope VARCHAR(20) DEFAULT 'OWN', -- OWN, ALL
  conditions JSONB, -- Additional conditions
  PRIMARY KEY (role_id, permission_id)
);

-- User-Role mapping
CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMP DEFAULT NOW(),
  assigned_by UUID REFERENCES users(id),
  PRIMARY KEY (user_id, role_id)
);
```

### 5.2. Permission Check Logic (Pseudocode)

```javascript
function hasPermission(user, permission, resource = null) {
  // 1. Get user's roles
  const roles = getUserRoles(user.id);
  
  // 2. Get all permissions for these roles (including inherited)
  const permissions = [];
  for (const role of roles) {
    permissions.push(...getRolePermissions(role.id));
    permissions.push(...getInheritedPermissions(role.level));
  }
  
  // 3. Check if requested permission exists
  const permissionEntry = permissions.find(p => p.code === permission);
  if (!permissionEntry) {
    return false;
  }
  
  // 4. Check scope
  if (permissionEntry.scope === 'ALL') {
    return true;
  }
  
  if (permissionEntry.scope === 'OWN' && resource) {
    return resource.owner_id === user.id;
  }
  
  // 5. Check additional conditions
  if (permissionEntry.conditions) {
    return evaluateConditions(permissionEntry.conditions, user, resource);
  }
  
  return true;
}

function checkFeatureLimit(user, feature) {
  const tier = user.tier; // FREE or PREMIUM
  const limits = FEATURE_LIMITS[tier];
  
  const currentUsage = getCurrentUsage(user.id, feature);
  const maxAllowed = limits[feature];
  
  if (maxAllowed === Infinity) {
    return { allowed: true };
  }
  
  if (currentUsage >= maxAllowed) {
    return {
      allowed: false,
      reason: `Đã đạt giới hạn ${maxAllowed} ${feature}. Nâng cấp Premium để sử dụng không giới hạn.`
    };
  }
  
  return { allowed: true, remaining: maxAllowed - currentUsage };
}
```

### 5.3. Middleware Example (NestJS)

```typescript
// permission.decorator.ts
export const RequirePermission = (permission: string) => {
  return SetMetadata('permission', permission);
};

// permission.guard.ts
@Injectable()
export class PermissionGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private permissionService: PermissionService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const permission = this.reflector.get<string>('permission', context.getHandler());
    
    if (!permission) {
      return true;
    }
    
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    
    if (!user) {
      throw new UnauthorizedException('Yêu cầu đăng nhập');
    }
    
    const hasPermission = await this.permissionService.hasPermission(
      user.id,
      permission,
      request.params.id // resource id if any
    );
    
    if (!hasPermission) {
      throw new ForbiddenException('Không có quyền thực hiện hành động này');
    }
    
    return true;
  }
}

// Usage in controller
@Controller('alerts')
export class AlertsController {
  @Post()
  @RequirePermission('alerts:create')
  async createAlert(@Body() dto: CreateAlertDto, @User() user: UserEntity) {
    // Check feature limit
    const limitCheck = await this.featureLimitService.check(user.id, 'alerts');
    if (!limitCheck.allowed) {
      throw new ForbiddenException(limitCheck.reason);
    }
    
    return this.alertsService.create(dto, user.id);
  }
  
  @Delete(':id')
  @RequirePermission('alerts:delete_own')
  async deleteAlert(@Param('id') id: string, @User() user: UserEntity) {
    // Guard will check if user owns this alert
    return this.alertsService.delete(id);
  }
}
```

---

## 6. AUDIT LOG

### 6.1. Permission Change Audit

```sql
CREATE TABLE permission_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL, -- ROLE_ASSIGNED, ROLE_REMOVED, PERMISSION_GRANTED, etc.
  target_user_id UUID,
  target_role_id UUID,
  old_value JSONB,
  new_value JSONB,
  ip_address INET,
  user_agent TEXT,
  performed_at TIMESTAMP DEFAULT NOW()
);
```

### 6.2. Access Audit

```sql
CREATE TABLE access_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  permission_code VARCHAR(100),
  resource_type VARCHAR(50),
  resource_id UUID,
  action VARCHAR(20), -- GRANTED, DENIED
  reason TEXT,
  ip_address INET,
  performed_at TIMESTAMP DEFAULT NOW()
);
```

---

## 7. ERROR MESSAGES

| Error Code | HTTP Status | Message (VI) | Message (EN) |
|------------|-------------|--------------|--------------|
| AUTH_001 | 401 | Vui lòng đăng nhập để tiếp tục | Please login to continue |
| AUTH_002 | 401 | Phiên đăng nhập đã hết hạn | Session expired |
| PERM_001 | 403 | Không có quyền thực hiện hành động này | Permission denied |
| PERM_002 | 403 | Đã đạt giới hạn. Nâng cấp Premium để tiếp tục | Limit reached. Upgrade to Premium |
| PERM_003 | 403 | Chức năng chỉ dành cho Premium | Premium feature only |
| PERM_004 | 403 | Không thể thao tác với tài nguyên của người khác | Cannot modify others' resources |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
