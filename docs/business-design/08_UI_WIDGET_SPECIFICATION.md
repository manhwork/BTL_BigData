# 08. UI WIDGET SPECIFICATION (LOGIC CỦA TỪNG THÀNH PHẦN GIAO DIỆN)

> **Dự án:** Hệ thống So sánh Giá Sản phẩm Thương mại Điện tử  
> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 2026-02-01

---

## 1. TỔNG QUAN

### 1.1. Danh sách Widget Components

| # | Widget | Mô tả | Sử dụng tại |
|---|--------|-------|-------------|
| 1 | SearchBar | Thanh tìm kiếm với auto-complete | Header, Home |
| 2 | ProductCard | Thẻ sản phẩm | Search results, Category |
| 3 | PriceComparisonTable | Bảng so sánh giá | Product Detail |
| 4 | ShopBadge | Badge loại shop | Product, Comparison |
| 5 | PriceHistoryChart | Biểu đồ lịch sử giá | Product Detail |
| 6 | AlertForm | Form tạo cảnh báo giá | Modal, Alert page |
| 7 | WatchlistItem | Item trong danh sách theo dõi | Watchlist page |
| 8 | NotificationDropdown | Dropdown thông báo | Header |
| 9 | FilterPanel | Panel bộ lọc | Search, Category |
| 10 | PriceTag | Tag hiển thị giá | Product cards |
| 11 | RatingStars | Hiển thị rating | Product, Shop |
| 12 | ShopWarningModal | Modal cảnh báo shop rủi ro | Product Detail |

### 1.2. Design Tokens

```css
/* Colors */
--color-primary: #1890ff;
--color-success: #52c41a;    /* Shop Mall */
--color-warning: #faad14;    /* Shop Preferred */
--color-error: #ff4d4f;      /* Shop Risky */

/* Typography */
--font-size-xs: 12px;
--font-size-sm: 14px;
--font-size-md: 16px;
--font-size-lg: 20px;
--font-size-xl: 24px;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;

/* Border Radius */
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 16px;
```

---

## 2. WIDGET SPECIFICATIONS

### 2.1. SearchBar Component

#### 2.1.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SEARCHBAR WIDGET                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Default State:                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ 🔍 │ Tìm kiếm sản phẩm...                                     │ [🎤] │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  Focus State (with auto-complete):                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ 🔍 │ iphone 15                                                │ [✕]  │ │
│  ├───────────────────────────────────────────────────────────────────────┤ │
│  │ 🕐 Tìm kiếm gần đây:                                                  │ │
│  │    iphone 15 pro max                                                  │ │
│  │    iphone 15 case                                                     │ │
│  │ ──────────────────────────────────────────────────────────────────── │ │
│  │ 💡 Gợi ý:                                                             │ │
│  │    📱 iPhone 15 Pro Max 256GB - 32,990,000đ                          │ │
│  │    📱 iPhone 15 Plus 128GB - 24,990,000đ                             │ │
│  │    📱 iPhone 15 128GB - 22,990,000đ                                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.1.2. Props & Configuration

| Prop | Type | Default | Mô tả |
|------|------|---------|-------|
| placeholder | string | "Tìm kiếm sản phẩm..." | Placeholder text |
| showVoiceSearch | boolean | true | Hiện nút voice search |
| showHistory | boolean | true | Hiện lịch sử tìm kiếm |
| maxSuggestions | number | 10 | Số gợi ý tối đa |
| debounceMs | number | 300 | Debounce time (ms) |
| minChars | number | 2 | Số ký tự tối thiểu |
| onSearch | function | - | Callback khi search |

#### 2.1.3. States

| State | Trigger | Visual Change |
|-------|---------|---------------|
| Default | Initial | Placeholder visible |
| Focused | Click/Tab | Border highlight, show dropdown |
| Loading | Typing | Show spinner |
| Has Results | API response | Show suggestions |
| No Results | API empty | Show "Không tìm thấy" |
| Error | API error | Show error message |

#### 2.1.4. Events

```typescript
interface SearchBarEvents {
  onFocus: () => void;
  onBlur: () => void;
  onChange: (value: string) => void;
  onSearch: (query: string) => void;
  onSuggestionClick: (product: Product) => void;
  onHistoryClick: (query: string) => void;
  onClear: () => void;
}
```

---

### 2.2. ProductCard Component

#### 2.2.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRODUCTCARD WIDGET                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Grid View (Default):                                                       │
│  ┌─────────────────────────┐                                                │
│  │ ┌─────────────────────┐ │                                                │
│  │ │                     │ │                                                │
│  │ │      [IMAGE]        │ │  ← 1:1 ratio                                  │
│  │ │                     │ │                                                │
│  │ │  ❤️ (wishlist)      │ │  ← Top right corner                           │
│  │ └─────────────────────┘ │                                                │
│  │                         │                                                │
│  │ 🏢 Shop Mall            │  ← Shop badge                                  │
│  │                         │                                                │
│  │ iPhone 15 Pro Max 256GB │  ← Product name (2 lines max)                 │
│  │ Natural Titanium        │                                                │
│  │                         │                                                │
│  │ ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶            │  ← Original price (strikethrough)           │
│  │ 32,990,000đ      -6%   │  ← Current price + discount badge             │
│  │                         │                                                │
│  │ ⭐ 4.8 (12,345)         │  ← Rating                                      │
│  │ Đã bán: 50k+            │  ← Sold count                                  │
│  │                         │                                                │
│  │ 📍 Shopee               │  ← Platform icon                               │
│  └─────────────────────────┘                                                │
│                                                                              │
│  List View:                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ┌───────┐                                                           │   │
│  │ │[IMAGE]│ 🏢 iPhone 15 Pro Max 256GB        ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶           │   │
│  │ │       │    Natural Titanium               32,990,000đ  -6%      │   │
│  │ │  ❤️   │    ⭐ 4.8 (12,345) | Đã bán: 50k+  Shopee Mall  [So sánh]│   │
│  │ └───────┘                                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.2.2. Props

| Prop | Type | Required | Mô tả |
|------|------|----------|-------|
| product | Product | Yes | Dữ liệu sản phẩm |
| variant | 'grid' \| 'list' | No | Kiểu hiển thị |
| showShopBadge | boolean | Yes | Hiện badge shop |
| showWishlist | boolean | Yes | Hiện nút wishlist |
| showCompare | boolean | No | Hiện nút so sánh |
| onClick | function | No | Click handler |
| onWishlistClick | function | No | Wishlist handler |

#### 2.2.3. Computed Values

```typescript
interface ProductCardComputed {
  discountPercentage: number; // ((original - current) / original) * 100
  formattedPrice: string;     // "32,990,000đ"
  formattedOriginal: string;  // "34,990,000đ" (strikethrough)
  soldCountDisplay: string;   // "50k+" or "1.2k"
  shopBadgeType: 'mall' | 'preferred' | 'risky';
}
```

---

### 2.3. PriceComparisonTable Component

#### 2.3.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PRICE COMPARISON TABLE WIDGET                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ SO SÁNH GIÁ - iPhone 15 Pro Max 256GB                    [Lọc] [Sắp xếp]│
│  ├───────────────────────────────────────────────────────────────────────┤ │
│  │                                                                       │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │                        BEST DEAL 🏆                             │   │ │
│  │ │ ┌─────┐                                                         │   │ │
│  │ │ │LOGO │  🏢 SHOP MALL - Apple Official Store                   │   │ │
│  │ │ │Shopee│     ⭐ 4.9 (12,345) | Đã bán: 50,000+                  │   │ │
│  │ │ └─────┘                                                         │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ Giá gốc:      ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶                                     │   │ │
│  │ │ Giá sale:     32,990,000đ                        [-6%]         │   │ │
│  │ │ Phí ship:     Miễn phí 🚚                                      │   │ │
│  │ │ Voucher:      -200,000đ (SALE200K)                             │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ TỔNG:         32,790,000đ                                      │   │ │
│  │ │                                                                 │   │ │
│  │ │ ✓ Chính hãng  ✓ Hoàn tiền 100%  ✓ Bảo hành 12 tháng           │   │ │
│  │ │                                                                 │   │ │
│  │ │            [Mua ngay]        [❤️ Theo dõi giá]                 │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                       │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │ ┌─────┐  ⭐ SHOP YÊU THÍCH - Di Động Việt                      │   │ │
│  │ │ │LOGO │     ⭐ 4.7 (3,456) | Đã bán: 15,000+                    │   │ │
│  │ │ │Lazada│                                                        │   │ │
│  │ │ └─────┘                                                         │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ Giá gốc:      ̶3̶4̶,̶9̶9̶0̶,̶0̶0̶0̶đ̶                                     │   │ │
│  │ │ Giá sale:     33,490,000đ                        [-4%]         │   │ │
│  │ │ Phí ship:     30,000đ                                          │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ TỔNG:         33,520,000đ              (+730,000đ)             │   │ │
│  │ │                                                                 │   │ │
│  │ │            [Mua ngay]        [❤️ Theo dõi giá]                 │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                       │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │ ┌─────┐  ⚠️ SHOP RỦI RO - New Seller                           │   │ │
│  │ │ │LOGO │     ⭐ 4.2 (89) | Đã bán: 500+                          │   │ │
│  │ │ │Tiki │     ⚠️ Shop mới - Cần cẩn trọng                        │   │ │
│  │ │ └─────┘                                                         │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ Giá:          31,500,000đ                                      │   │ │
│  │ │ Phí ship:     50,000đ                                          │   │ │
│  │ │ ────────────────────────────────────────────────────────────── │   │ │
│  │ │ TỔNG:         31,550,000đ              (-1,240,000đ)           │   │ │
│  │ │                                                                 │   │ │
│  │ │            [Mua ngay ⚠️]     [❤️ Theo dõi giá]                 │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.3.2. Props

| Prop | Type | Required | Mô tả |
|------|------|----------|-------|
| listings | ProductListing[] | Yes | Danh sách listings |
| sortBy | 'price' \| 'rating' \| 'sold' \| 'trust' | No | Sắp xếp |
| filterShopType | ShopType[] | No | Lọc loại shop |
| showVouchers | boolean | No | Hiện voucher |
| onBuyClick | (listing) => void | Yes | Handler mua |
| onWatchClick | (listing) => void | Yes | Handler theo dõi |

#### 2.3.3. Computed Values

```typescript
interface ComparisonComputed {
  bestDeal: ProductListing;           // Lowest final_price with good trust
  priceDifference: number;            // Difference from best deal
  savingsPercent: number;             // Savings compared to highest price
  sortedListings: ProductListing[];   // Sorted by selected criteria
  filteredListings: ProductListing[]; // After shop type filter
}
```

---

### 2.4. ShopBadge Component

#### 2.4.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SHOPBADGE WIDGET                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Variants:                                                                  │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │ 🏢 SHOP MALL    │  │ ⭐ YÊU THÍCH    │  │ ⚠️ RỦI RO      │            │
│  │ (Green bg)      │  │ (Yellow bg)     │  │ (Red bg)        │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                              │
│  Size variants:                                                             │
│                                                                              │
│  Small (inline):  [🏢 Mall]  [⭐ Yêu thích]  [⚠️ Rủi ro]                   │
│                                                                              │
│  Medium (card):   ┌───────────────────────────┐                            │
│                   │ 🏢 SHOP MALL              │                            │
│                   │ Tin cậy cao               │                            │
│                   └───────────────────────────┘                            │
│                                                                              │
│  Large (detail):  ┌───────────────────────────────────────────┐            │
│                   │ 🏢 SHOP MALL - Chính hãng                 │            │
│                   │ ✓ Sản phẩm chính hãng                     │            │
│                   │ ✓ Bảo hành chính hãng                     │            │
│                   │ ✓ Hoàn tiền 100%                          │            │
│                   └───────────────────────────────────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.4.2. Props

| Prop | Type | Default | Mô tả |
|------|------|---------|-------|
| type | 'mall' \| 'preferred' \| 'risky' | Required | Loại badge |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Kích thước |
| showTooltip | boolean | true | Hiện tooltip chi tiết |
| showScore | boolean | false | Hiện điểm tin cậy |
| score | number | - | Điểm shop (0-100) |

#### 2.4.3. Style Mapping

```typescript
const BADGE_STYLES = {
  mall: {
    bg: '#52c41a',       // Green
    text: '#ffffff',
    icon: '🏢',
    label: 'SHOP MALL',
    tooltip: 'Shop chính hãng, được sàn TMĐT xác thực'
  },
  preferred: {
    bg: '#faad14',       // Yellow
    text: '#000000',
    icon: '⭐',
    label: 'YÊU THÍCH',
    tooltip: 'Shop uy tín, được nhiều người tin tưởng'
  },
  risky: {
    bg: '#ff4d4f',       // Red
    text: '#ffffff',
    icon: '⚠️',
    label: 'RỦI RO',
    tooltip: 'Cần cẩn trọng khi mua hàng từ shop này'
  }
};
```

---

### 2.5. PriceHistoryChart Component

#### 2.5.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PRICE HISTORY CHART WIDGET                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ LỊCH SỬ GIÁ                                                           │ │
│  │                                                                       │ │
│  │ Timeframe: [7D] [30D] [90D🔒] [6M🔒] [1Y🔒] [Custom🔒]                │ │
│  │                                                                       │ │
│  │ Platform:  [All] [Shopee] [Lazada] [Tiki]                            │ │
│  │                                                                       │ │
│  │  35,000,000 ┤                                                         │ │
│  │             │     ╭─╮                                                 │ │
│  │  34,000,000 ┤    ╱   ╲                                                │ │
│  │             │   ╱     ╲        ╭──╮                                   │ │
│  │  33,000,000 ┤  ╱       ╲──────╱    ╲────╮                             │ │
│  │             │ ╱                         ╲───╮                         │ │
│  │  32,000,000 ┤╱                               ╲────── ●                │ │
│  │             │                                        │ 32,990,000     │ │
│  │  31,000,000 ┤                    ●                                    │ │
│  │             │                    │ Flash Sale                         │ │
│  │             └─────────────────────────────────────────────────────── │ │
│  │               01/01    07/01    15/01    22/01    30/01              │ │
│  │                                                                       │ │
│  │  Legend: ──── Shopee  ──── Lazada  ──── Tiki                        │ │
│  │                                                                       │ │
│  │ ┌───────────────────────────────────────────────────────────────────┐│ │
│  │ │ 📊 THỐNG KÊ (30 ngày):                                            ││ │
│  │ │                                                                   ││ │
│  │ │ Giá hiện tại:     32,990,000đ                                     ││ │
│  │ │ Giá thấp nhất:    31,990,000đ  (15/01 - Flash Sale)              ││ │
│  │ │ Giá cao nhất:     34,990,000đ  (01/01)                           ││ │
│  │ │ Giá trung bình:   33,450,000đ                                     ││ │
│  │ │ Xu hướng:         📉 Giảm 5% so với 30 ngày trước                ││ │
│  │ └───────────────────────────────────────────────────────────────────┘│ │
│  │                                                                       │ │
│  │ 📍 Sự kiện: [●Flash Sale 15/01] [●Tết Sale 22/01]                   │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.5.2. Props

| Prop | Type | Default | Mô tả |
|------|------|---------|-------|
| productId | string | Required | ID sản phẩm |
| defaultTimeframe | '7d' \| '30d' \| '90d' \| '6m' \| '1y' | '30d' | Timeframe mặc định |
| platforms | string[] | all | Platforms hiển thị |
| showEvents | boolean | true | Hiện event markers |
| showStatistics | boolean | true | Hiện thống kê |
| isPremium | boolean | false | User premium |
| onTimeframeChange | function | - | Handler |

#### 2.5.3. Chart Configuration

```typescript
interface ChartConfig {
  type: 'line';
  responsive: true;
  maintainAspectRatio: false;
  
  scales: {
    x: {
      type: 'time';
      time: {
        unit: 'day' | 'week' | 'month';
      };
    };
    y: {
      ticks: {
        callback: (value) => formatPrice(value);
      };
    };
  };
  
  plugins: {
    tooltip: {
      callbacks: {
        label: (context) => {
          return `${context.dataset.label}: ${formatPrice(context.raw)}`;
        };
      };
    };
    annotation: {
      annotations: eventMarkers; // Flash sale, etc.
    };
  };
}
```

#### 2.5.4. Statistics Calculation

```typescript
interface PriceStatistics {
  currentPrice: number;
  minPrice: number;
  minPriceDate: Date;
  minPriceEvent: string | null;
  maxPrice: number;
  maxPriceDate: Date;
  avgPrice: number;
  priceChange: number;        // Current vs first day
  priceChangePercent: number;
  trend: 'up' | 'down' | 'stable';
}
```

---

### 2.6. AlertForm Component

#### 2.6.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ALERT FORM WIDGET                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    ĐẶT CẢNH BÁO GIÁ                                   │ │
│  │                                                                       │ │
│  │  Sản phẩm: iPhone 15 Pro Max 256GB                                   │ │
│  │  Giá hiện tại: 32,990,000đ                                           │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  Loại cảnh báo: *                                                    │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ○ Giá giảm xuống dưới:                                          │ │ │
│  │  │   ┌────────────────────────────────────┐                        │ │ │
│  │  │   │ 30,000,000                    │ đ  │                        │ │ │
│  │  │   └────────────────────────────────────┘                        │ │ │
│  │  │   Slider: [═══════○═══════════════] 30M / 35M                   │ │ │
│  │  │                                                                 │ │ │
│  │  │ ○ Giảm giá ít nhất:                                             │ │ │
│  │  │   ┌──────────┐                                                  │ │ │
│  │  │   │ 10       │ %                                                │ │ │
│  │  │   └──────────┘                                                  │ │ │
│  │  │                                                                 │ │ │
│  │  │ ● Giá tốt nhất trong:                                           │ │ │
│  │  │   ┌──────────────────────┐                                      │ │ │
│  │  │   │ 30 ngày          ▼  │                                      │ │ │
│  │  │   └──────────────────────┘                                      │ │ │
│  │  │                                                                 │ │ │
│  │  │ ○ Khi có Flash Sale                                             │ │ │
│  │  │                                                                 │ │ │
│  │  │ ○ Khi có hàng trở lại (đang hết hàng)                          │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  Theo dõi trên sàn:                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ☑️ Shopee    ☑️ Lazada    ☑️ Tiki    ☐ Sendo    ☐ TikTok Shop │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  Nhận thông báo qua: *                                               │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ☑️ Email (user@email.com)                                       │ │ │
│  │  │ ☑️ Push Notification                                            │ │ │
│  │  │ ☐ SMS (+84 xxx xxx xxx) 🔒 Premium                             │ │ │
│  │  │ ☐ Telegram 🔒 Premium                                          │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  📊 Dự đoán: Dựa trên lịch sử, giá có thể giảm xuống 31,500,000đ   │ │
│  │             vào khoảng ngày 15/02 (Flash Sale 2.2)                  │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │                        [Hủy]        [Lưu cảnh báo]                   │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.6.2. Props

| Prop | Type | Required | Mô tả |
|------|------|----------|-------|
| productId | string | Yes | ID sản phẩm |
| currentPrice | number | Yes | Giá hiện tại |
| existingAlert | Alert | No | Alert đang chỉnh sửa |
| userTier | 'free' \| 'premium' | Yes | Tier user |
| onSubmit | (alert) => void | Yes | Submit handler |
| onCancel | () => void | Yes | Cancel handler |

#### 2.6.3. Form Validation

```typescript
interface AlertFormValidation {
  alertType: {
    required: true;
    message: 'Vui lòng chọn loại cảnh báo';
  };
  targetPrice: {
    required: (type) => type === 'PRICE_DROP';
    min: 1000;
    max: (currentPrice) => currentPrice * 0.99;
    message: 'Giá mục tiêu phải thấp hơn giá hiện tại';
  };
  targetPercentage: {
    required: (type) => type === 'PERCENTAGE_DROP';
    min: 1;
    max: 99;
    message: 'Phần trăm phải từ 1-99%';
  };
  platforms: {
    required: true;
    minLength: 1;
    message: 'Chọn ít nhất 1 sàn TMĐT';
  };
  channels: {
    required: true;
    minLength: 1;
    message: 'Chọn ít nhất 1 kênh thông báo';
  };
}
```

---

### 2.7. ShopWarningModal Component

#### 2.7.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SHOP WARNING MODAL WIDGET                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                               [✕]    │ │
│  │                                                                       │ │
│  │                          ⚠️ CẢNH BÁO                                  │ │
│  │                                                                       │ │
│  │  Shop "New Seller" được đánh giá là "Rủi ro"                         │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  Lý do:                                                              │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ • Shop mới tham gia (< 1 tháng)                                 │ │ │
│  │  │ • Số lượng đánh giá thấp (89 reviews)                           │ │ │
│  │  │ • Rating chưa cao (4.2/5.0)                                     │ │ │
│  │  │ • Tỷ lệ phản hồi thấp (65%)                                     │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  Khuyến nghị:                                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ✓ Đọc kỹ đánh giá từ người mua                                  │ │ │
│  │  │ ✓ Kiểm tra chính sách đổi trả                                   │ │ │
│  │  │ ✓ Ưu tiên thanh toán COD                                        │ │ │
│  │  │ ✓ Chụp ảnh/video khi nhận hàng                                  │ │ │
│  │  │ ✓ Cân nhắc mua từ shop uy tín hơn                               │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │  💡 Sản phẩm này có ở shop uy tín hơn:                              │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ 🏢 Apple Official Store (Shop Mall)                             │ │ │
│  │  │    Giá: 32,990,000đ (+1,490,000đ)                              │ │ │
│  │  │    ✓ Chính hãng ✓ Bảo hành 12 tháng                            │ │ │
│  │  │                                              [Xem ngay →]       │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ ⭐ Di Động Việt (Shop Yêu thích)                                │ │ │
│  │  │    Giá: 33,100,000đ (+1,600,000đ)                              │ │ │
│  │  │    ✓ Uy tín tốt ✓ Đã bán 15,000+                               │ │ │
│  │  │                                              [Xem ngay →]       │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ─────────────────────────────────────────────────────────────────── │ │
│  │                                                                       │ │
│  │       [Tiếp tục mua từ shop này]      [Xem tất cả shop uy tín]      │ │
│  │                                                                       │ │
│  │  ☐ Không hiện lại cảnh báo này cho shop "New Seller"                │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.7.2. Props

| Prop | Type | Required | Mô tả |
|------|------|----------|-------|
| isOpen | boolean | Yes | Modal đang mở |
| shop | Seller | Yes | Thông tin shop |
| product | Product | Yes | Sản phẩm đang xem |
| alternatives | ProductListing[] | No | Shop thay thế |
| onContinue | () => void | Yes | Tiếp tục mua |
| onViewAlternatives | () => void | Yes | Xem shop khác |
| onClose | () => void | Yes | Đóng modal |
| onDontShowAgain | (shopId) => void | No | Không hiện lại |

#### 2.7.3. Warning Reasons Logic

```typescript
function getWarningReasons(shop: Seller): string[] {
  const reasons: string[] = [];
  
  if (shop.tenure_months < 1) {
    reasons.push(`Shop mới tham gia (< 1 tháng)`);
  }
  if (shop.review_count < 100) {
    reasons.push(`Số lượng đánh giá thấp (${shop.review_count} reviews)`);
  }
  if (shop.seller_rating < 4.5) {
    reasons.push(`Rating chưa cao (${shop.seller_rating}/5.0)`);
  }
  if (shop.response_rate < 70) {
    reasons.push(`Tỷ lệ phản hồi thấp (${shop.response_rate}%)`);
  }
  if (shop.success_rate < 85) {
    reasons.push(`Tỷ lệ đơn thành công thấp (${shop.success_rate}%)`);
  }
  
  return reasons;
}
```

---

### 2.8. FilterPanel Component

#### 2.8.1. Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FILTER PANEL WIDGET                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────┐                                            │
│  │ BỘ LỌC                [Xóa tất cả]                                      │
│  │                                                                         │
│  │ ▼ Khoảng giá                                                            │
│  │ ┌───────────────────────────┐                                           │
│  │ │ [═══════○═══○═══════════] │                                           │
│  │ │   1M        10M       50M │                                           │
│  │ │                           │                                           │
│  │ │ Từ: [5,000,000  ] đ       │                                           │
│  │ │ Đến: [20,000,000] đ       │                                           │
│  │ └───────────────────────────┘                                           │
│  │                                                                         │
│  │ ▼ Sàn thương mại điện tử                                                │
│  │ ┌───────────────────────────┐                                           │
│  │ │ ☑️ Shopee     (12,345)    │                                           │
│  │ │ ☑️ Lazada     (8,234)     │                                           │
│  │ │ ☑️ Tiki       (5,678)     │                                           │
│  │ │ ☐ Sendo      (2,345)     │                                           │
│  │ │ ☐ TikTok Shop (1,234)    │                                           │
│  │ └───────────────────────────┘                                           │
│  │                                                                         │
│  │ ▼ Loại Shop                                                             │
│  │ ┌───────────────────────────┐                                           │
│  │ │ ☑️ 🏢 Shop Mall     (5,678)│                                          │
│  │ │ ☑️ ⭐ Shop Yêu thích (8,234)│                                          │
│  │ │ ☐ ⚠️ Shop Rủi ro   (2,345)│                                          │
│  │ └───────────────────────────┘                                           │
│  │                                                                         │
│  │ ▼ Đánh giá                                                              │
│  │ ┌───────────────────────────┐                                           │
│  │ │ ○ Tất cả                  │                                           │
│  │ │ ○ 5 sao ⭐⭐⭐⭐⭐        │                                           │
│  │ │ ● 4 sao trở lên ⭐⭐⭐⭐   │                                           │
│  │ │ ○ 3 sao trở lên ⭐⭐⭐     │                                           │
│  │ └───────────────────────────┘                                           │
│  │                                                                         │
│  │ ▼ Trạng thái                                                            │
│  │ ┌───────────────────────────┐                                           │
│  │ │ ☑️ Đang giảm giá          │                                           │
│  │ │ ☐ Miễn phí vận chuyển     │                                           │
│  │ │ ☐ Flash Sale              │                                           │
│  │ │ ☐ Còn hàng                │                                           │
│  │ └───────────────────────────┘                                           │
│  │                                                                         │
│  │ ▶ Xu hướng giá (collapsed)                                              │
│  │                                                                         │
│  │         [Áp dụng bộ lọc]                                                │
│  └─────────────────────────────┘                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.8.2. Props

| Prop | Type | Required | Mô tả |
|------|------|----------|-------|
| filters | FilterState | Yes | State hiện tại |
| facets | Facets | Yes | Facet counts từ API |
| onChange | (filters) => void | Yes | Change handler |
| onReset | () => void | Yes | Reset handler |
| collapsible | boolean | true | Có thể collapse |
| showCounts | boolean | true | Hiện count |

#### 2.8.3. Filter State Interface

```typescript
interface FilterState {
  priceRange: {
    min: number | null;
    max: number | null;
  };
  platforms: string[];
  shopTypes: ('mall' | 'preferred' | 'risky')[];
  minRating: number | null;
  status: {
    onSale: boolean;
    freeShipping: boolean;
    flashSale: boolean;
    inStock: boolean;
  };
  priceTrend: 'decreasing' | 'increasing' | 'stable' | null;
  sortBy: 'price_asc' | 'price_desc' | 'rating' | 'sold' | 'relevance';
}
```

---

## 3. SHARED COMPONENTS

### 3.1. Loading States

```
┌───────────────────────────────────────────────────────────────────────────┐
│                         LOADING STATES                                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Skeleton (Card):        Spinner (Inline):       Progress (Action):       │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     │
│  │ ░░░░░░░░░░░░░░░ │     │                 │     │ ████████░░░░░░░ │     │
│  │ ░░░░░░░░░░░░░░░ │     │    ◌            │     │      75%        │     │
│  │ ░░░░░░░░░       │     │                 │     │                 │     │
│  │ ░░░░░░░░░░░     │     │  Loading...     │     │  Đang tải...    │     │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Toast Notifications

```
┌───────────────────────────────────────────────────────────────────────────┐
│                       TOAST NOTIFICATIONS                                 │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Success:                Error:                   Info:                   │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     │
│  │ ✅ Thành công!  │     │ ❌ Có lỗi xảy ra│     │ ℹ️ Thông báo    │     │
│  │ Đã thêm vào     │     │ Vui lòng thử lại│     │ Đã cập nhật giá │     │
│  │ watchlist       │     │                 │     │ mới             │     │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘     │
│                                                                           │
│  Position: Top-right      Duration: 3-5 seconds   Auto-dismiss: Yes      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. ACCESSIBILITY (A11Y)

### 4.1. Keyboard Navigation

| Component | Tab | Enter | Escape | Arrow Keys |
|-----------|-----|-------|--------|------------|
| SearchBar | Focus | Submit | Close dropdown | Navigate suggestions |
| FilterPanel | Navigate sections | Toggle | - | - |
| Modal | Focus trap | - | Close | - |
| Dropdown | Open | Select | Close | Navigate items |
| ProductCard | Focus | Open detail | - | - |

### 4.2. ARIA Attributes

```html
<!-- SearchBar -->
<input 
  role="combobox"
  aria-label="Tìm kiếm sản phẩm"
  aria-expanded="true|false"
  aria-haspopup="listbox"
  aria-controls="search-suggestions"
/>

<!-- ShopBadge -->
<span 
  role="status"
  aria-label="Shop Mall - Tin cậy cao"
>
  🏢 SHOP MALL
</span>

<!-- Modal -->
<div 
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Cảnh báo</h2>
</div>
```

---

## 5. RESPONSIVE BEHAVIOR

| Breakpoint | SearchBar | FilterPanel | ProductCard | ComparisonTable |
|------------|-----------|-------------|-------------|-----------------|
| Mobile (<768px) | Full width, icon only | Bottom sheet | Full width | Stacked cards |
| Tablet (768-1024px) | Expanded | Sidebar | 2 columns | Horizontal scroll |
| Desktop (>1024px) | Expanded | Sidebar | 3-4 columns | Full table |

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-01  
**Author:** Development Team
