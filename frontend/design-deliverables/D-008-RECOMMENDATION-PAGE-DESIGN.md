# D-008: 推薦頁面設計規格

> **Recommendation Page 完整設計規範（核心頁面）**

**任務狀態**: ✅ 規格已建立
**建立日期**: 2025-01-26

---

## 📱 設計概覽

### 頁面目標
1. **核心體驗**: 一次一道菜的卡片翻轉推薦
2. **降低決策疲勞**: 只提供「要」或「換」兩個選項
3. **即時價格回饋**: 換菜時立即顯示價格變化
4. **進度可視化**: 清楚顯示已決定幾道菜
5. **建立期待感**: 動畫營造開盲盒的興奮感

### 頁面結構

```
┌─────────────────────────────────────┐
│  [MenuSummary Card]                 │  ← 固定頂部
│  本次菜單組成 | 已決定 2/6 道        │
├─────────────────────────────────────┤
│                                     │
│         [DishCard]                  │  ← 主要內容區
│      (當前推薦的菜品)                 │
│                                     │
│  [✅ 我要點這道] [🔄 換一道]         │
│                                     │
├─────────────────────────────────────┤
│  [PriceIndicator]                   │  ← 浮動提示
│  +NT$ 40 ⚠️                         │  (價格變化時)
└─────────────────────────────────────┘
```

---

## 🎯 MenuSummary Section (菜單摘要)

### Mobile 版本

```
┌─────────────────────────────────────┐
│  本次菜單組成                        │  ← H2
├─────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐    │
│  │ 🥗 冷菜 ×1 │  │ 🍖 熱菜 ×2 │    │  ← Category Grid
│  └────────────┘  └────────────┘    │
│  ┌────────────┐  ┌────────────┐    │
│  │ 🍚 主食 ×1 │  │ 🥟 點心 ×2 │    │
│  └────────────┘  └────────────┘    │
├─────────────────────────────────────┤
│  共 6 道                            │
│  總價 NT$ 1,200                     │  ← Display/3XL
│  人均 NT$ 400 (3人)                 │
├─────────────────────────────────────┤
│  已決定 2/6 道            33%       │
│  ████████░░░░░░░░░░░░              │  ← Progress Bar
└─────────────────────────────────────┘
```

#### 詳細規格

**Container:**
- [使用 MenuSummary component]
- Background: surface (#FFFFFF)
- Padding: 24px
- Border-radius: 24px (top corners only, 底部直角)
- Shadow: shadow-card
- Margin-bottom: 24px
- Position: sticky, top: 0, z-index: 10 (optional)

**Title:**
- Font: Display/2XL (31px)
- Color: charcoal
- Margin-bottom: 16px

**Category Grid:**
- Display: grid
- Grid-template-columns: repeat(2, 1fr)
- Gap: 12px
- Margin-bottom: 16px

**Category Item:**
- Background: cream-100
- Padding: 12px 16px
- Border-radius: 8px
- Display: flex, align-items: center, gap: 8px

**Category Emoji:**
- Font-size: 32px

**Category Label:**
- Font: Body/SM Medium (13px)
- Color: charcoal
- Flex: 1

**Category Count:**
- Font: Body/LG Bold (20px)
- Color: terracotta
- Margin-left: auto

**Divider:**
- Height: 1px
- Background: charcoal/10
- Margin: 16px 0

**Summary Row:**
- Display: flex
- Justify-content: space-between
- Align-items: baseline
- Margin-bottom: 8px

**Total Dishes:**
- Font: Body/Base (16px)
- Color: charcoal/70

**Total Price:**
- Font: Display/3XL (39px)
- Color: charcoal
- Font-weight: Semibold

**Per Person:**
- Font: Body/LG (20px)
- Color: sage-700
- Margin-top: 4px

**Progress Section:**
- Margin-top: 16px

**Progress Text Row:**
- Display: flex
- Justify-content: space-between
- Font: Body/SM (13px)
- Color: charcoal/80
- Margin-bottom: 8px

**Progress Percentage:**
- Font: Body/SM Medium (13px)
- Color: terracotta

**Progress Bar:**
- [使用 Progress Bar component]
- Height: 12px
- Background: charcoal/10
- Fill: gradient-accent
- Border-radius: full

---

## 🃏 DishCard Section (菜品卡片)

### Mobile 版本

```
┌─────────────────────────────────────┐
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │   [Photo Placeholder]       │   │  ← 192px height
│  │   (淡色背景 + emoji)         │   │
│  │                             │   │
│  │   🥗 冷菜                   │   │  ← Badge (左上角)
│  └─────────────────────────────┘   │
│                                     │
│  涼拌黃瓜                            │  ← H3
│  NT$ 80                             │  ← Price
│                                     │
│  ┌───────────────────────────┐     │
│  │ ✍️ "清爽開胃，搭配熱菜更... │     │  ← Reason Box
│  │    45 則評論推薦"           │     │  (Handwriting)
│  └───────────────────────────┘     │
│                                     │
│  ┌──────────────┐ ┌──────────┐    │
│  │✅ 我要點這道  │ │🔄 換一道  │    │  ← Action Buttons
│  └──────────────┘ └──────────┘    │
└─────────────────────────────────────┘
```

#### 詳細規格

**Container:**
- [使用 SwappingCard + DishCard components]
- Background: surface
- Border-radius: 24px
- Shadow: shadow-card
- Padding: 0 (photo full bleed), then 24px
- Margin: 0 24px 120px 24px (bottom margin 為按鈕空間)
- Max-width: 480px (desktop)
- Margin: 0 auto

**Photo Placeholder:**
- Height: 192px (mobile) / 256px (desktop)
- Background: linear-gradient(135deg, cream-50, caramel-50)
- Display: flex, align-items: center, justify-content: center
- Border-radius: 24px 24px 0 0

**Photo Emoji:**
- Font-size: 96px (mobile) / 120px (desktop)
- Opacity: 30%
- 菜系對應 emoji:
  - 冷菜: 🥗
  - 熱菜: 🍖
  - 湯品: 🍲
  - 主食: 🍚
  - 點心: 🥟
  - 甜點: 🍰

**Category Badge:**
- [使用 Badge component]
- Position: absolute, top: 16px, left: 16px
- Background: sage/10
- Color: sage-700
- Padding: 6px 12px
- Font: Body/SM Medium (13px)

**Content Area:**
- Padding: 24px

**Dish Name (H3):**
- Font: Body/XL Bold (25px)
- Color: charcoal
- Margin-bottom: 8px

**Price:**
- Font: Display/2XL (31px)
- Color: terracotta
- Font-weight: Semibold
- Margin-bottom: 16px

**Reason Box:**
- Background: linear-gradient(to right, cream-100 0%, transparent 100%) @ 50% opacity
- Padding: 16px
- Border-left: 4px solid caramel
- Border-radius: 0 8px 8px 0
- Transform: rotate(-1deg) (整個 box 微微傾斜)
- Margin-bottom: 24px

**Reason Text:**
- Font: Handwriting/XL (25px)
- Color: caramel-700
- Line-height: 1.75
- Font-family: Caveat

**Review Count (optional):**
- Font: Body/SM (13px)
- Color: charcoal/60
- Margin-top: 8px

**Action Buttons Container:**
- Display: flex
- Gap: 12px
- Padding: 0 24px 24px 24px

**Confirm Button:**
- [使用 Button component, variant: primary, size: md]
- Flex: 1
- Icon: ✅ (left)
- Text: "我要點這道"

**Swap Button:**
- [使用 Button component, variant: outline, size: md]
- Flex: 1
- Icon: 🔄 (left)
- Text: "換一道"

---

### DishCard States (狀態)

#### Default State (預設)
- 上述所有樣式
- 兩個按鈕都可見
- 卡片 opacity: 1

#### Confirmed State (已確認)
- Card opacity: 0.75
- Border: 3px solid success (#6B9D7F)
- CheckCircle icon: 右上角, 32px, success color
- Action Buttons: 隱藏
- 不可再互動（pointer-events: none）

#### Loading State (載入中)
- Skeleton screen
- Photo area: shimmer animation
- Text areas: pulse animation
- Buttons: disabled

---

## 💰 PriceIndicator (價格變化提示)

### 顯示時機

**觸發條件:**
- 點擊「換一道」時
- 新菜品價格 ≠ 舊菜品價格

**顯示內容:**
- 價格上升: `+NT$ 40 ⚠️` (warning color)
- 價格下降: `-NT$ 30 ✓` (success color)

### 詳細規格

```
┌──────────────┐
│  +NT$ 40 ⚠️  │  ← 浮動 badge
└──────────────┘
```

**Container:**
- [使用 PriceIndicator component]
- Position: fixed
- Top: 96px (MenuSummary 下方)
- Right: 16px
- Z-index: 50

**Badge:**
- Background: warning (#E89C5C) 上升 / success (#6B9D7F) 下降
- Color: white
- Padding: 12px 20px
- Border-radius: 9999px (full)
- Shadow: shadow-floating
- Font: Body/LG Bold (20px)

**Icon:**
- ⚠️ 上升且超過 $50
- ✓ 下降

**Animation:**
```javascript
// 進場
{
  initial: { x: 400, opacity: 0, scale: 0.8 },
  animate: { x: 0, opacity: 1, scale: 1 },
  transition: { type: 'spring', stiffness: 200, damping: 25 }
}

// Pulse (重複 2 次)
{
  animate: { scale: [1, 1.15, 1, 1.15, 1] },
  transition: { duration: 0.8 }
}

// 離場 (2 秒後)
{
  animate: { opacity: 0, y: -20 },
  transition: { duration: 0.3, delay: 2 }
}
```

---

## 🎬 動畫規範

### Card Swap Animation (核心動畫)

#### Swap Out (舊卡片)

```javascript
{
  initial: { x: 0, rotate: 0, opacity: 1, scale: 1 },
  exit: {
    x: '-100vw',
    rotate: -15,
    opacity: 0,
    scale: 0.8
  },
  transition: {
    duration: 0.4,
    ease: [0.4, 0, 0.2, 1]
  }
}
```

#### Swap In (新卡片)

```javascript
{
  initial: { x: '100vw', rotate: 15, opacity: 0, scale: 0.8 },
  animate: {
    x: 0,
    rotate: 0,
    opacity: 1,
    scale: 1
  },
  transition: {
    type: 'spring',
    stiffness: 100,
    damping: 20,
    mass: 1
  }
}
```

#### Confirm Animation (確認)

```javascript
// Stage 1: 輕微放大
{
  animate: { scale: 1.02 },
  transition: { duration: 0.2 }
}

// Stage 2: 降低透明度 + 加邊框
{
  animate: {
    opacity: 0.75,
    border: '3px solid #6B9D7F'
  },
  transition: { duration: 0.3 }
}

// Stage 3: CheckCircle icon 彈出
{
  initial: { scale: 0, rotate: -180 },
  animate: { scale: 1, rotate: 0 },
  transition: {
    type: 'spring',
    stiffness: 200,
    damping: 15,
    delay: 0.2
  }
}
```

### MenuSummary 更新動畫

**Price 數字變化:**
```javascript
// 使用 react-countup 或 Framer Motion
{
  animate: { value: newPrice },
  transition: {
    duration: 0.8,
    ease: 'easeOut'
  }
}
```

**Progress Bar 增長:**
```javascript
{
  animate: { width: `${newPercentage}%` },
  transition: {
    duration: 0.6,
    ease: 'easeOut',
    delay: 0.3  // 在卡片確認後再增長
  }
}
```

**Category Count 更新:**
```javascript
{
  animate: {
    scale: [1, 1.2, 1],
    color: [charcoal, terracotta, charcoal]
  },
  transition: { duration: 0.4 }
}
```

---

## 🔄 互動流程

### 用戶點擊「我要點這道」

```
1. 卡片執行 Confirm Animation (600ms)
   - 放大 → 降低透明度 → 加邊框 → CheckCircle 彈出

2. MenuSummary 同步更新 (800ms)
   - Progress Bar 增長
   - 已決定數字 +1
   - 總價數字滾動
   - 對應類別 count +1 並閃爍

3. 延遲 800ms 後，載入下一張卡片
   - 舊卡片淡出（不翻轉，因為已確認）
   - 新卡片從右側滑入

4. 如果已完成所有菜品
   - 觸發慶祝動畫（confetti）
   - 顯示「完成菜單」按鈕
   - 自動跳轉至 Menu Page (2 秒後)
```

### 用戶點擊「換一道」

```
1. 舊卡片執行 Swap Out Animation (400ms)
   - 向左飛出 + 旋轉 -15deg + 縮小

2. 同時，API 請求新菜品
   - 顯示 Loading Skeleton (如果 API 未返回)

3. 新卡片執行 Swap In Animation (600ms)
   - 從右側飛入 + 旋轉 15deg → 0deg + 彈跳

4. 如果價格有變化
   - PriceIndicator 從右側飛入
   - Pulse 動畫 × 2
   - MenuSummary 總價同步更新
   - 2 秒後自動消失
```

### 邊界情況處理

**連續快速點擊「換一道」:**
- 禁用按鈕直到動畫完成（400ms）
- 防止重複請求 API

**API 請求失敗:**
- 顯示 Toast: "哎呀，載入失敗了，請再試一次"
- 保留舊卡片，允許重試

**菜池耗盡（換了 20 次還不滿意）:**
- 提示: "我們已經為您挑選了最合適的菜品囉！"
- 建議確認當前菜品或調整偏好設定

---

## 📊 資料流

### API Request (換菜)

```typescript
POST /api/recommendations/swap
{
  "sessionId": "abc123",
  "currentDishId": "dish_456",
  "categoryIndex": 0,  // 第幾道菜（0-based）
  "context": {
    "alreadySelected": ["dish_123", "dish_789"],
    "totalBudget": 1200,
    "remainingBudget": 800
  }
}

Response:
{
  "dish": {
    "id": "dish_999",
    "name": "涼拌黃瓜",
    "category": "冷菜",
    "price": 80,
    "reason": "清爽開胃，搭配熱菜更均衡，45 則評論推薦",
    "emoji": "🥗",
    "reviewCount": 45
  },
  "priceDiff": -20,  // 相較於舊菜品
  "newTotal": 1180
}
```

### 前端狀態管理

```typescript
interface RecommendationState {
  menu: {
    totalDishes: number
    categories: {
      name: string
      emoji: string
      count: number
    }[]
    totalPrice: number
    perPerson: number
    people: number
  }

  currentDish: Dish | null
  confirmedDishes: Dish[]
  currentIndex: number  // 目前推薦第幾道（0-based）

  isSwapping: boolean
  isConfirming: boolean
  showPriceIndicator: boolean
  priceDiff: number | null
}
```

---

## 🎉 完成狀態

### 所有菜品確認完成時

```
┌─────────────────────────────────────┐
│                                     │
│         🎉                          │
│                                     │
│      菜單完成！                      │  ← H2
│      共 6 道菜 NT$ 1,200            │
│                                     │
│  [已選菜品縮圖列表]                  │
│  🥗 🍖 🍖 🍚 🥟 🥟                  │
│                                     │
│  ┌──────────────────────────┐      │
│  │  📋 查看完整菜單          │      │  ← Primary CTA
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  🔄 重新推薦              │      │  ← Secondary CTA
│  └──────────────────────────┘      │
│                                     │
└─────────────────────────────────────┘
```

#### 詳細規格

**Confetti Animation:**
- [使用 canvas-confetti]
- 觸發時機: Progress 達到 100% 時
- 延遲 500ms 觸發
- 150 顆粒子，暖色系
- 持續 3 秒

**Success Screen:**
- Background: cream-100
- Padding: 48px 24px
- Text-align: center

**Celebration Emoji:**
- Font-size: 120px
- Margin-bottom: 24px
- Animation: bounce + rotate

**Title:**
- Font: Display/3XL (39px)
- Color: charcoal
- Margin-bottom: 8px

**Summary:**
- Font: Body/LG (20px)
- Color: charcoal/70
- Margin-bottom: 32px

**Dish Icons Row:**
- Display: flex, gap: 8px, justify-content: center
- Margin-bottom: 40px

**Dish Icon:**
- Font-size: 48px
- Background: cream-200
- Padding: 12px
- Border-radius: 50%
- Box-shadow: shadow-sm

**Primary CTA:**
- [Button component, variant: primary, size: lg]
- Width: 100% (max-width: 320px)
- Margin-bottom: 16px

**Secondary CTA:**
- [Button component, variant: ghost, size: md]
- Width: auto

**Auto-redirect:**
- 2 秒後自動跳轉至 Menu Page
- 顯示倒數計時: "2 秒後自動跳轉..."

---

## 📱 響應式設計

### Mobile (375px - 767px)
- MenuSummary: Full-width, sticky top (optional)
- DishCard: Max-width 100%, padding 24px
- Buttons: Full-width stack
- PriceIndicator: Right 16px

### Desktop (1280px+)
- MenuSummary: Max-width 480px, 不 sticky（改為左側固定欄）
- DishCard: Max-width 480px, 居中
- Buttons: 並排，各佔 50%
- PriceIndicator: Right 32px

**Desktop 佈局 (Optional Advanced):**
```
┌──────────────────────────────────────────┐
│  ┌─────────────┐    ┌──────────────┐    │
│  │             │    │              │    │
│  │ MenuSummary │    │   DishCard   │    │
│  │ (固定左側)   │    │   (居中)     │    │
│  │             │    │              │    │
│  └─────────────┘    └──────────────┘    │
│   ← 左欄 30%         右欄 70% →          │
└──────────────────────────────────────────┘
```

---

## ♿ 無障礙考量

### 鍵盤操作

**快捷鍵:**
- `Enter` 或 `Space`: 確認當前菜品
- `→` (右箭頭): 換一道菜
- `Esc`: 退出推薦流程（返回輸入頁）

### ARIA 標籤

```html
<main aria-label="菜品推薦">
  <section aria-label="菜單摘要" aria-live="polite">
    <!-- MenuSummary -->
  </section>

  <article aria-label="當前推薦菜品" role="article">
    <h3>{dishName}</h3>
    <p aria-label="價格">NT$ {price}</p>
    <p aria-label="推薦理由">{reason}</p>
  </article>

  <nav aria-label="菜品操作">
    <button aria-label="確認此菜品">我要點這道</button>
    <button aria-label="換一道菜">換一道</button>
  </nav>
</main>
```

### 動畫減弱

```javascript
const shouldReduceMotion = useReducedMotion()

// 如果用戶偏好減少動畫
if (shouldReduceMotion) {
  // 卡片翻轉改為淡入淡出
  swapAnimation = { opacity: [0, 1], duration: 0.15 }
  // 取消 confetti
  skipConfetti = true
}
```

---

## 📝 D-008 任務完成報告

### 完成項目
✅ 設計核心推薦頁面結構
✅ MenuSummary 摘要卡片設計（類別統計 + 進度）
✅ DishCard 菜品卡片設計（3 種狀態）
✅ PriceIndicator 價格變化提示
✅ 完整的卡片翻轉動畫規範
✅ 互動流程設計（確認/換菜）
✅ 完成狀態設計（慶祝動畫）
✅ 資料流與狀態管理
✅ 響應式與無障礙規範

### 交付物
- `D-008-RECOMMENDATION-PAGE-DESIGN.md` - 完整推薦頁設計規格

### 設計重點

#### 核心體驗設計:
1. **一次一道菜**: 降低決策疲勞，聚焦當前選擇
2. **卡片翻轉**: 營造開盲盒的期待感與驚喜
3. **即時回饋**: 價格變化、進度更新都即時可見
4. **慶祝時刻**: 完成時的 confetti 動畫強化成就感

#### 動畫策略:
- **Swap Out + Swap In**: 400ms + 600ms，流暢的卡片交替
- **Confirm Animation**: 多階段動畫，清楚標示已確認
- **Price Indicator**: Spring 動畫 + Pulse，吸引注意力
- **Progress Update**: Stagger 動畫，視覺上更豐富

#### 資訊架構:
- **MenuSummary**: 提供全局視角（共幾道、總價、進度）
- **DishCard**: 聚焦單一菜品（名稱、價格、推薦理由）
- **PriceIndicator**: 即時回饋（價格變化提醒）

### 實際執行事項（設計師需完成）

**今日完成** (6 小時):
1. 在 Figma 建立 Recommendation Page Frame
2. 設計 MenuSummary 卡片（包含 Grid + Progress）
3. 設計 DishCard（3 種狀態: Default, Confirmed, Loading）
4. 設計 PriceIndicator 浮動提示
5. 設計完成狀態畫面（Success Screen）

**明日完成** (4 小時):
6. 建立卡片翻轉動畫原型（Figma Smart Animate）
7. 建立 Desktop 版本（左右分欄佈局）
8. 測試所有互動流程
9. 調整細節（間距、顏色、陰影）

### 技術要點

- 使用 Framer Motion 的 AnimatePresence 處理卡片切換
- 使用 react-countup 或 Framer Motion 處理數字動畫
- 使用 canvas-confetti 處理慶祝動畫
- 狀態管理: React Context + useReducer
- API 請求: SWR 或 React Query (處理快取與重試)

### 效能考量

- 卡片圖片使用 lazy loading
- 動畫只使用 transform 和 opacity (GPU 加速)
- 限制換菜次數（防止惡意請求）
- 前端快取候選菜品（減少 API 請求）

### 下一步
D-009: 菜單頁面設計（Menu Page）

---

**任務狀態**: ✅ 規格完成
**建立時間**: 2025-01-26
**預估時間**: 6 小時（規格建立） + 10 小時（實際設計）
