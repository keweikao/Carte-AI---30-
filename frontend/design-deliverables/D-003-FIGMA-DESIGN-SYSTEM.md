# D-003: Figma 設計系統規格

> **完整的組件庫與樣式庫規範**

**任務狀態**: ✅ 規格已建立
**建立日期**: 2025-01-26

---

## 📚 設計系統架構

```
OderWhat Design System/
├── 🎨 Foundations/
│   ├── Colors (色彩變數 - 已完成於 D-002)
│   ├── Typography (字體樣式)
│   ├── Spacing (間距 Token)
│   ├── Shadows (陰影樣式)
│   └── Radius (圓角樣式)
│
├── 🧩 Components/
│   ├── Buttons
│   ├── Cards
│   ├── Inputs
│   ├── Badges
│   ├── Progress Bars
│   └── (其他組件)
│
└── 📄 Pages/
    ├── Landing Page
    ├── Input Page
    ├── Recommendation Page
    └── Menu Page
```

---

## 🎨 Foundations - 基礎樣式

### 1. Typography Styles (字體樣式)

在 Figma 中建立 Text Styles：

#### Display (標題用 - Cormorant Garamond)

| Style Name | 字體 | 大小 | 字重 | 行高 | 字距 |
|-----------|------|------|------|------|------|
| Display/5XL | Cormorant Garamond | 61px | Semibold (600) | 73px (1.2) | -1% |
| Display/4XL | Cormorant Garamond | 49px | Semibold (600) | 59px (1.2) | -1% |
| Display/3XL | Cormorant Garamond | 39px | Semibold (600) | 47px (1.2) | -0.5% |
| Display/2XL | Cormorant Garamond | 31px | Medium (500) | 37px (1.2) | 0% |

#### Body (內文用 - Noto Sans TC)

| Style Name | 字體 | 大小 | 字重 | 行高 | 字距 |
|-----------|------|------|------|------|------|
| Body/XL | Noto Sans TC | 25px | Bold (700) | 38px (1.5) | 0% |
| Body/LG | Noto Sans TC | 20px | Bold (700) | 30px (1.5) | 0% |
| Body/Base | Noto Sans TC | 16px | Regular (400) | 24px (1.5) | 0% |
| Body/SM | Noto Sans TC | 13px | Regular (400) | 20px (1.5) | 0% |
| Body/XS | Noto Sans TC | 10px | Regular (400) | 15px (1.5) | 0% |

#### Handwriting (手寫註記用 - Caveat)

| Style Name | 字體 | 大小 | 字重 | 行高 | 字距 | 特殊 |
|-----------|------|------|------|------|------|------|
| Handwriting/XL | Caveat | 25px | Medium (500) | 44px (1.75) | 0% | rotation: -2deg |
| Handwriting/LG | Caveat | 20px | Medium (500) | 35px (1.75) | 0% | rotation: -2deg |

#### Button (按鈕用 - Noto Sans TC)

| Style Name | 字體 | 大小 | 字重 | 行高 | 字距 |
|-----------|------|------|------|------|------|
| Button/LG | Noto Sans TC | 18px | Medium (500) | 22px (1.2) | 0% |
| Button/Base | Noto Sans TC | 16px | Medium (500) | 19px (1.2) | 0% |
| Button/SM | Noto Sans TC | 14px | Medium (500) | 17px (1.2) | 0% |

---

### 2. Spacing Tokens (間距標記)

建議在 Figma 中建立 Auto Layout 預設：

```
space-1:  4px
space-2:  8px
space-3:  12px
space-4:  16px   ← 最常用
space-5:  24px   ← 最常用
space-6:  32px   ← 最常用
space-8:  48px
space-10: 64px
space-12: 96px
```

### 3. Shadow Effects (陰影效果)

在 Figma 中建立 Effect Styles：

| Effect Name | Type | X | Y | Blur | Spread | Color |
|------------|------|---|---|------|--------|-------|
| Shadow/SM | Drop Shadow | 0 | 1px | 2px | 0 | #2D2D2D @ 5% |
| Shadow/Base | Drop Shadow | 0 | 2px | 8px | 0 | #2D2D2D @ 8% |
| Shadow/MD | Drop Shadow | 0 | 4px | 16px | 0 | #2D2D2D @ 12% |
| Shadow/LG | Drop Shadow | 0 | 8px | 32px | 0 | #2D2D2D @ 16% |
| Shadow/Card | Drop Shadow | 0 | 4px | 20px | 0 | #D4A574 @ 15% (暖色調) |
| Shadow/Floating | Drop Shadow | 0 | 12px | 40px | 0 | #2D2D2D @ 25% |

### 4. Border Radius (圓角半徑)

```
radius-sm:     4px
radius-base:   8px
radius-md:     12px  (input)
radius-lg:     16px  (button)
radius-xl:     24px  (card)
radius-2xl:    32px
radius-full:   9999px
```

---

## 🧩 Components - 組件庫

### Component 1: Button

#### 變體設定 (Variants)

**Properties:**
- `variant`: primary | secondary | outline | ghost
- `size`: sm | md | lg
- `state`: default | hover | active | disabled

#### 各變體規格

##### Primary Button
```
Background: gradient-accent (linear-gradient from caramel to terracotta)
Text Color: White (#FFFFFF)
Padding:
  - SM: 16px horizontal, 8px vertical
  - MD: 24px horizontal, 12px vertical
  - LG: 32px horizontal, 16px vertical
Border Radius: 16px (radius-button)
Shadow: shadow-md
Font: Button/[size]

States:
- Default: gradient + shadow-md
- Hover: gradient + shadow-lg + scale(1.05)
- Active: gradient + scale(0.95)
- Disabled: gradient @ 50% opacity + cursor not-allowed
```

##### Secondary Button
```
Background: sage (#8B9D83)
Text Color: White
Padding: [same as primary]
Border Radius: 16px
Shadow: shadow-base

States:
- Default: sage + shadow-base
- Hover: sage/700 (#6F7D68)
- Active: sage/900 (#4A5145)
- Disabled: sage @ 50% opacity
```

##### Outline Button
```
Background: Transparent
Text Color: charcoal (#2D2D2D)
Border: 2px solid charcoal/20 (rgba(45,45,45,0.2))
Padding: [same as primary, 內縮 2px 因為有 border]
Border Radius: 16px

States:
- Default: border charcoal/20
- Hover: border charcoal + background charcoal/5
- Active: background charcoal/10
- Disabled: text @ 50% opacity
```

##### Ghost Button
```
Background: Transparent
Text Color: charcoal
Border: None
Padding: [same as primary]

States:
- Default: transparent
- Hover: background charcoal/10
- Active: background charcoal/15
- Disabled: text @ 50% opacity
```

#### Figma 建立步驟：
1. 建立 Frame，命名 `Button`
2. 加入 Text layer
3. 套用 Auto Layout (padding 依上方規格)
4. 加入 Component 屬性（右側面板 → Add variant）
5. 設定 Properties: variant, size, state
6. 為每個狀態設定不同樣式

---

### Component 2: Card

#### 變體設定

**Properties:**
- `variant`: default | selected
- `state`: default | hover

#### 規格

##### Default Card
```
Background: surface (#FFFFFF)
Padding: 32px (space-6)
Border Radius: 24px (radius-card)
Shadow: shadow-card
Border: None

States:
- Default: shadow-card
- Hover: shadow-lg
```

##### Selected Card
```
Background: surface (#FFFFFF) @ 75% opacity
Padding: 32px
Border Radius: 24px
Border: 3px solid success (#6B9D7F)
Shadow: shadow-card

Icon: CheckCircle (Lucide) @ top-right
  - Color: success
  - Size: 32px

States:
- Default: [as above]
- Hover: [same as default, no change]
```

---

### Component 3: Input

#### 變體設定

**Properties:**
- `type`: text | search | number
- `state`: default | focus | error | disabled

#### 規格

```
Background: surface (#FFFFFF)
Padding: 16px horizontal, 12px vertical
Border Radius: 12px (radius-input)
Border: 2px solid charcoal/10
Font: Body/Base
Text Color: charcoal

States:
- Default: border charcoal/10
- Focus: border caramel + ring (4px caramel @ 20%)
- Error: border error + ring (4px error @ 20%)
- Disabled: background charcoal/5 + text @ 50%
```

#### Search Input 特殊處理：
- 左側加入 Search Icon (Lucide)
- Icon color: charcoal/60
- Icon size: 20px
- Padding-left: 44px (16px + 20px icon + 8px gap)

---

### Component 4: Badge

用於類別標籤（冷菜、熱菜等）

#### 規格

```
Background: sage/10 (rgba(139,157,131,0.1))
Text Color: sage/700 (#6F7D68)
Padding: 12px horizontal, 4px vertical
Border Radius: 9999px (radius-full)
Font: Body/SM
Font Weight: Medium (500)
```

#### 顏色變體（可選）：
- Default: sage/10 + sage/700
- Caramel: caramel/10 + caramel/700
- Terracotta: terracotta/10 + terracotta/700

---

### Component 5: Progress Bar

#### 規格

```
Container:
  - Height: 12px
  - Background: charcoal/10
  - Border Radius: 9999px
  - Overflow: hidden

Fill:
  - Height: 12px
  - Background: gradient-accent
  - Border Radius: 9999px
  - Width: 0-100% (由 data 控制)
  - Transition: width 0.6s ease-out

Complete State (100%):
  - Add pulsing animation overlay (white @ 30% opacity)
```

---

## 📄 組件組合範例

### DishCard Component (核心組件)

這是推薦頁面的核心組件，需要特別設計：

#### 結構

```
┌─────────────────────────────────────┐
│  [Photo Placeholder Area]           │  ← 192px height
│  (淡色背景 + 菜系 emoji)             │
├─────────────────────────────────────┤
│  🥗 冷菜                             │  ← Badge
│                                     │
│  涼拌黃瓜                            │  ← H3 (Body/XL Bold)
│  NT$ 80                             │  ← Price (Terracotta, Body/2XL)
│                                     │
│  ┌─────────────────────────────┐   │
│  │ ✍️ "清爽開胃，45則評論..."   │   │  ← Handwriting
│  └─────────────────────────────┘   │     (Caveat, -2deg rotation)
│                                     │
│  [✅ 我要點這道] [🔄 換一道]       │  ← Buttons
└─────────────────────────────────────┘
```

#### 詳細規格

**Container:**
- Width: 100% (max-width: 480px on desktop)
- Background: surface
- Border Radius: 24px (radius-card)
- Shadow: shadow-card
- Padding: 0 (photo full bleed), then 24px for content

**Photo Placeholder:**
- Height: 192px
- Background: gradient from cream-50 to caramel-50
- Display: emoji (text-6xl, 96px, opacity 30%)
- Alignment: center

**Badge:**
- Positioned: 16px from top-left (over photo)
- Style: [use Badge component]

**Dish Name:**
- Font: Body/XL Bold
- Color: charcoal
- Margin-top: 16px

**Price:**
- Font: Display/2XL
- Color: terracotta
- Margin-top: 8px

**Reason Box:**
- Background: cream-100 @ 50% opacity
- Padding: 16px
- Border-left: 4px solid caramel
- Border-radius: 8px
- Margin-top: 16px

**Reason Text:**
- Font: Handwriting/XL
- Color: caramel-700
- Rotation: -2deg (整個 box rotate)
- Leading: relaxed

**Review Count (optional):**
- Font: Body/SM
- Color: charcoal/60
- Margin-top: 8px

**Button Container:**
- Display: flex, gap: 12px
- Margin-top: 24px

**Buttons:**
- Left: Primary button "✅ 我要點這道"
- Right: Outline button "🔄 換一道"
- Both: size MD, flex: 1 (equal width)

#### Selected State:
- Entire card: opacity 75%
- Border: 3px solid success
- CheckCircle icon: top-right corner (outside padding)
- Buttons: hidden

---

## 📝 D-003 任務完成報告

### 完成項目
✅ 定義完整的設計系統架構
✅ 建立 Typography Styles 規範（15+ 個）
✅ 建立 Spacing Tokens 規範
✅ 建立 Shadow Effects 規範（6 個）
✅ 建立 Border Radius 規範
✅ 設計 5 個基礎組件（Button, Card, Input, Badge, Progress）
✅ 設計核心組件 DishCard 完整規格

### 交付物
- `D-003-FIGMA-DESIGN-SYSTEM.md` - 完整設計系統規格

### 實際執行事項（設計師需完成）

**今日完成** (3 小時):
1. 在 Figma 中建立 Typography Styles（15 個）
2. 建立 Shadow Effects（6 個）
3. 建立 Button Component（4 variants × 3 sizes × 4 states = 48 個變體）
4. 建立 Card Component（2 variants × 2 states = 4 個變體）
5. 建立 Input Component（3 types × 4 states = 12 個變體）

**明日完成** (2 小時):
6. 建立 Badge Component（3 color variants）
7. 建立 Progress Component
8. 建立 DishCard Component（2 states: pending, selected）
9. 測試所有組件在不同尺寸下的表現

### 設計提示

#### Button 組件建立技巧：
1. 先建立 Primary/MD/Default 變體
2. 複製為其他 variant
3. 使用 Component Properties 切換樣式
4. 善用 Auto Layout 確保 padding 一致

#### DishCard 建立技巧：
1. 使用 Auto Layout 從上到下排列
2. Photo area 使用 Frame + emoji text
3. Reason box 使用獨立 Frame 並 rotate -2deg
4. Buttons 使用已建立的 Button component instance

### 下一步
D-004: 基礎組件庫設計（繼續建立其他組件）

---

**任務狀態**: ✅ 規格完成（實際建立需人類設計師執行）
**建立時間**: 2025-01-26
**預估時間**: 3 小時（規格建立） + 5 小時（實際建立）
