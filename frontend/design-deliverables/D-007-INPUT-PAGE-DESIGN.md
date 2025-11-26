# D-007: 輸入頁面設計規格

> **Input Page 完整設計規範（4 個 Steps）**

**任務狀態**: ✅ 規格已建立
**建立日期**: 2025-01-26

---

## 📱 設計概覽

### 頁面目標
1. **引導用戶完成 4 步輸入**: 餐廳 → 人數/預算 → 模式 → 偏好
2. **降低認知負擔**: 一次只顯示一個步驟
3. **提供即時回饋**: 每步驟完成後立即視覺化進度
4. **保持輕鬆感**: 避免冗長表單的壓迫感

### 整體結構

```
┌─────────────────────────────────────┐
│  ● ──── ○ ──── ○ ──── ○             │  ← StepIndicator
│  餐廳   人數   模式   偏好           │
├─────────────────────────────────────┤
│                                     │
│         [Step Content]              │  ← 動態切換
│                                     │
├─────────────────────────────────────┤
│  [← 上一步]          [下一步 →]    │  ← Navigation
└─────────────────────────────────────┘
```

---

## 🎯 Step 1: 選擇餐廳

### Mobile 版本

```
┌─────────────────────────────────────┐
│  ● ──── ○ ──── ○ ──── ○             │
│  餐廳   人數   模式   偏好           │
├─────────────────────────────────────┤
│                                     │
│      想去哪家餐廳？                  │  ← H2
│                                     │
│  ┌──────────────────────────┐      │
│  │ 🔍 試試看『鼎泰豐』或...   │      │  ← Search Input
│  └──────────────────────────┘      │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 📍 鼎泰豐 信義店              │ │  ← Result 1
│  │    台北市信義區...            │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │ 📍 添好運 台北車站店          │ │  ← Result 2
│  └───────────────────────────────┘ │
│                                     │
│      ──── 或 ────                   │
│                                     │
│  ┌──────────────────────────┐      │
│  │  讓 AI 幫我推薦餐廳        │      │  ← Secondary Option
│  └──────────────────────────┘      │
│                                     │
└─────────────────────────────────────┘
```

#### 詳細規格

**Container:**
- Background: cream-100
- Min-height: 100vh
- Padding: 24px
- Display: flex, flex-direction: column

**StepIndicator:**
- [使用 StepIndicator component]
- Margin-bottom: 48px
- Fixed at top on scroll (optional)

**Step Title (H2):**
- Font: Display/3XL (39px)
- Color: charcoal
- Text-align: center
- Margin-bottom: 32px

**Search Input:**
- [使用 RestaurantSearch component]
- Width: 100%
- Margin-bottom: 24px
- Placeholder: "試試看『鼎泰豐』或『添好運』"
- Auto-focus on mount

**Results List:**
- Max-height: 320px
- Overflow: auto
- Background: surface
- Border-radius: 12px
- Shadow: shadow-md
- Margin-bottom: 24px

**Result Item:**
- Padding: 16px
- Border-bottom: 1px solid charcoal/10
- Cursor: pointer
- Transition: background 0.15s

**Result Item Hover:**
- Background: cream-100

**Restaurant Name:**
- Font: Body/Base Medium (16px)
- Color: charcoal

**Restaurant Address:**
- Font: Body/SM (13px)
- Color: charcoal/60
- Margin-top: 4px

**Divider:**
- Text: "──── 或 ────"
- Font: Body/SM (13px)
- Color: charcoal/40
- Text-align: center
- Margin: 32px 0

**AI Recommendation Button:**
- [使用 Button component, variant: outline, size: md]
- Width: 100%
- Icon: 🤖 (left side)

**Bottom Navigation:**
- Position: sticky, bottom: 24px
- Display: flex, justify-content: space-between
- Gap: 16px
- Margin-top: auto

**Navigation Buttons:**
- [使用 Button component]
- 上一步: variant: ghost, size: md
- 下一步: variant: primary, size: md, flex: 1

---

## 👥 Step 2: 設定人數與預算

### Mobile 版本

```
┌─────────────────────────────────────┐
│  ● ──── ● ──── ○ ──── ○             │
│  餐廳   人數   模式   偏好           │
├─────────────────────────────────────┤
│                                     │
│      設定用餐條件                    │  ← H2
│                                     │
│  ┌──────────────────────────┐      │
│  │  用餐人數                 │      │  ← Section 1
│  │                          │      │
│  │  ┌───┐ ┌───┐ ┌───┐      │      │
│  │  │ 2 │ │ 4 │ │ 6 │      │      │  ← Quick Select
│  │  └───┘ └───┘ └───┘      │      │
│  │                          │      │
│  │  或輸入人數: [  8  ] 人   │      │  ← Custom Input
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  人均預算                 │      │  ← Section 2
│  │                          │      │
│  │  NT$ 500                 │      │  ← Display Value
│  │  ═════════●═══════════   │      │  ← Slider
│  │  100          1000       │      │
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  預估總價                 │      │  ← Summary
│  │  NT$ 4,000               │      │
│  │  (8人 × NT$ 500)         │      │
│  └──────────────────────────┘      │
│                                     │
│  [← 上一步]      [下一步 →]         │
│                                     │
└─────────────────────────────────────┘
```

#### 詳細規格

**Step Title:**
- Font: Display/3XL (39px)
- Margin-bottom: 40px

**Section Container:**
- Background: surface
- Padding: 32px 24px
- Border-radius: 24px
- Margin-bottom: 24px
- Shadow: shadow-card

**Section Label:**
- Font: Body/Base Medium (16px)
- Color: charcoal
- Margin-bottom: 16px

**Quick Select Buttons (人數):**
- Display: grid
- Grid-template-columns: repeat(3, 1fr)
- Gap: 12px
- Margin-bottom: 16px

**Quick Select Button:**
- [使用 Button component, variant: outline]
- Padding: 20px
- Font: Body/LG Bold (20px)
- Border: 2px solid charcoal/10

**Quick Select Button (Selected):**
- Border: 3px solid success
- Background: success/5
- Color: success-dark

**Custom Input Row:**
- Display: flex
- Align-items: center
- Gap: 8px
- Font: Body/Base (16px)
- Color: charcoal/70

**Number Input:**
- Width: 80px
- Text-align: center
- Font: Body/LG Bold (20px)
- Padding: 12px
- Border: 2px solid charcoal/10
- Border-radius: 8px

**Budget Slider:**
- [使用 BudgetSlider component]
- Min: 100
- Max: 1000
- Step: 50
- Default: 500

**Summary Box:**
- Background: terracotta/10
- Padding: 24px
- Border-radius: 16px
- Border-left: 4px solid terracotta
- Text-align: center

**Summary Total:**
- Font: Display/3XL (39px)
- Color: terracotta
- Margin-bottom: 8px

**Summary Detail:**
- Font: Body/Base (16px)
- Color: charcoal/70

---

## 🍽️ Step 3: 選擇用餐模式

### Mobile 版本

```
┌─────────────────────────────────────┐
│  ● ──── ● ──── ● ──── ○             │
│  餐廳   人數   模式   偏好           │
├─────────────────────────────────────┤
│                                     │
│      選擇用餐模式                    │  ← H2
│                                     │
│  ┌──────────────────────────┐      │
│  │  🍽️                      │      │
│  │                          │      │  ← Mode 1
│  │  大家分食                 │      │
│  │                          │      │
│  │  適合 2-6 人             │      │
│  │  共享美食時光             │      │
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  🥘                      │      │
│  │                          │      │  ← Mode 2
│  │  個人套餐                 │      │
│  │                          │      │
│  │  每人獨立點餐             │      │
│  │  各取所需                 │      │
│  └──────────────────────────┘      │
│                                     │
│  [← 上一步]      [下一步 →]         │
│                                     │
└─────────────────────────────────────┘
```

#### 詳細規格

**Step Title:**
- Font: Display/3XL (39px)
- Margin-bottom: 40px

**Mode Cards Container:**
- Display: flex
- Flex-direction: column
- Gap: 16px
- Margin-bottom: 48px

**Mode Card:**
- [使用 ModeSelector component]
- Background: surface
- Padding: 48px 32px
- Border-radius: 24px
- Border: 2px solid charcoal/10
- Text-align: center
- Cursor: pointer
- Transition: all 0.3s

**Mode Card (Selected):**
- Border: 3px solid success
- Background: success/5
- Shadow: shadow-lg
- CheckCircle icon (top-right, 32px, success color)

**Mode Emoji:**
- Font-size: 80px
- Margin-bottom: 24px

**Mode Title:**
- Font: Body/XL Bold (25px)
- Color: charcoal
- Margin-bottom: 12px

**Mode Description Line 1:**
- Font: Body/Base (16px)
- Color: charcoal/70
- Margin-bottom: 4px

**Mode Description Line 2:**
- Font: Body/SM (13px)
- Color: charcoal/60

---

### Desktop 版本 (Step 3)

```
┌──────────────────────────────────────────────┐
│  ● ──────── ● ──────── ● ──────── ○          │
│  餐廳       人數       模式       偏好        │
├──────────────────────────────────────────────┤
│                                              │
│           選擇用餐模式                        │
│                                              │
│  ┌──────────────┐      ┌──────────────┐    │
│  │  🍽️          │      │  🥘          │    │
│  │              │      │              │    │
│  │  大家分食     │      │  個人套餐     │    │
│  │  適合 2-6人   │      │  每人獨立點餐 │    │
│  │  共享美食時光 │      │  各取所需     │    │
│  └──────────────┘      └──────────────┘    │
│                                              │
│     [← 上一步]           [下一步 →]          │
│                                              │
└──────────────────────────────────────────────┘
```

**Desktop 特殊規格:**
- Mode Cards: Grid, 2 columns, gap: 32px
- Max-width: 800px, margin: 0 auto
- Card padding: 64px 48px

---

## 🎯 Step 4: 設定偏好與禁忌

### Mobile 版本

```
┌─────────────────────────────────────┐
│  ● ──── ● ──── ● ──── ●             │
│  餐廳   人數   模式   偏好           │
├─────────────────────────────────────┤
│                                     │
│      告訴我們你的偏好                │  ← H2
│      (可選，但能讓推薦更精準)         │
│                                     │
│  ┌──────────────────────────┐      │
│  │  飲食禁忌                 │      │  ← Section 1
│  │                          │      │
│  │  [不吃牛] [不吃辣] [×]   │      │  ← Tags
│  │                          │      │
│  │  快選: 不吃牛 | 不吃辣... │      │
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  喜好類別                 │      │  ← Section 2
│  │                          │      │
│  │  [海鮮] [蔬食] [+]       │      │
│  │                          │      │
│  │  快選: 海鮮 | 蔬食...     │      │
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │  特殊需求                 │      │  ← Section 3
│  │                          │      │
│  │  □ 有長輩同行             │      │
│  │  □ 有小孩                 │      │
│  │  □ 慶祝場合               │      │
│  └──────────────────────────┘      │
│                                     │
│  [← 上一步]      [開始推薦 🎯]      │
│                                     │
└─────────────────────────────────────┘
```

#### 詳細規格

**Step Title:**
- Font: Display/3XL (39px)
- Margin-bottom: 8px

**Step Subtitle:**
- Font: Body/Base (16px)
- Color: charcoal/60
- Margin-bottom: 32px
- Text-align: center

**Section Container:**
- Background: surface
- Padding: 24px
- Border-radius: 24px
- Margin-bottom: 16px
- Shadow: shadow-card

**Section Title:**
- Font: Body/Base Medium (16px)
- Color: charcoal
- Margin-bottom: 12px

**Tag Input:**
- [使用 TagInput component]
- 飲食禁忌: sage 色系
- 喜好類別: caramel 色系

**Quick Select Row:**
- Font: Body/SM (13px)
- Color: charcoal/60
- Margin-top: 12px

**Quick Select Tags:**
- Display: inline
- Color: caramel
- Cursor: pointer
- Text-decoration: underline on hover
- 建議選項:
  - 飲食禁忌: 不吃牛 | 不吃辣 | 不吃海鮮 | 素食 | 不吃豬 | 不吃羊
  - 喜好類別: 海鮮 | 蔬食 | 肉類 | 湯品 | 炸物 | 甜點

**Checkboxes Section:**
- Display: flex, flex-direction: column, gap: 12px

**Checkbox Item:**
- Display: flex, align-items: center, gap: 12px
- Padding: 12px
- Border-radius: 8px
- Cursor: pointer
- Transition: background 0.15s

**Checkbox Item Hover:**
- Background: cream-100

**Checkbox:**
- Size: 20px
- Border: 2px solid charcoal/30
- Border-radius: 4px
- [Checked] Background: success, border: success

**Checkbox Label:**
- Font: Body/Base (16px)
- Color: charcoal

**Final CTA Button:**
- [使用 Button component, variant: primary, size: lg]
- Width: 100%
- Text: "開始推薦 🎯"
- Margin-top: auto

---

## 🎨 頁面轉場動畫

### Step 切換動畫

**前往下一步 (Forward):**
```javascript
{
  initial: { x: '100%', opacity: 0 },
  animate: { x: 0, opacity: 1 },
  exit: { x: '-100%', opacity: 0 },
  transition: { duration: 0.3, ease: easing.easeInOut }
}
```

**返回上一步 (Backward):**
```javascript
{
  initial: { x: '-100%', opacity: 0 },
  animate: { x: 0, opacity: 1 },
  exit: { x: '100%', opacity: 0 },
  transition: { duration: 0.3, ease: easing.easeInOut }
}
```

### StepIndicator 動畫

**Dot 完成時:**
```javascript
{
  animate: {
    backgroundColor: success,
    scale: [1, 1.3, 1]
  },
  transition: { duration: 0.4 }
}
```

**Connector Line 填充:**
```javascript
{
  initial: { scaleX: 0 },
  animate: { scaleX: 1 },
  transition: { duration: 0.5, ease: easing.easeOut },
  style: { transformOrigin: 'left' }
}
```

---

## 📊 狀態管理

### 資料結構

```typescript
interface InputState {
  step: 1 | 2 | 3 | 4
  restaurant: {
    id: string | null
    name: string
    address: string
  } | null
  useAIRecommendation: boolean
  people: number
  budgetPerPerson: number
  mode: 'shared' | 'individual' | null
  preferences: {
    restrictions: string[]  // ["不吃牛", "不吃辣"]
    favorites: string[]     // ["海鮮", "蔬食"]
    specialNeeds: {
      hasElderly: boolean
      hasChildren: boolean
      isCelebration: boolean
    }
  }
}
```

### 驗證規則

**Step 1 → Step 2:**
- 必須選擇餐廳 OR 勾選「讓 AI 推薦」

**Step 2 → Step 3:**
- 人數 >= 1
- 預算 >= 100

**Step 3 → Step 4:**
- 必須選擇模式（shared 或 individual）

**Step 4 → 推薦頁:**
- 無必填項（偏好為選填）

---

## 💾 資料持久化

### LocalStorage 策略

```typescript
// 每次 step 切換時自動儲存
useEffect(() => {
  localStorage.setItem('oderwhat_input_state', JSON.stringify(inputState))
}, [inputState])

// 頁面載入時恢復
useEffect(() => {
  const saved = localStorage.getItem('oderwhat_input_state')
  if (saved) {
    const parsed = JSON.parse(saved)
    // 驗證資料有效性
    if (isValidInputState(parsed)) {
      setInputState(parsed)
    }
  }
}, [])
```

### 返回處理

- 從推薦頁返回輸入頁：恢復上次狀態
- 關閉瀏覽器重開：仍可恢復（7 天內）
- 提供「重新開始」按鈕清除所有資料

---

## ♿ 無障礙考量

### 鍵盤導航

**Tab 順序:**
1. StepIndicator (可選，僅視覺)
2. 主要輸入欄位/選項
3. 上一步按鈕
4. 下一步按鈕

**Enter 鍵行為:**
- Step 1: 按下 Enter → 選擇第一個搜尋結果
- Step 2-4: 按下 Enter → 等同點擊「下一步」

### ARIA 標籤

```html
<div role="progressbar" aria-valuenow="2" aria-valuemin="1" aria-valuemax="4">
  <!-- StepIndicator -->
</div>

<form aria-label="輸入用餐條件" onSubmit={handleNext}>
  <!-- Step content -->
</form>

<nav aria-label="步驟導航">
  <button aria-label="返回上一步">← 上一步</button>
  <button aria-label="前往下一步">下一步 →</button>
</nav>
```

---

## 📱 響應式設計

### Mobile (375px - 767px)
- Single column layout
- Full-width inputs and buttons
- Sticky bottom navigation
- Padding: 24px

### Tablet (768px - 1279px)
- Max-width: 640px, centered
- Larger padding: 32px
- Step 3 仍保持單欄（卡片較大更好點選）

### Desktop (1280px+)
- Max-width: 800px, centered
- Padding: 48px
- Step 3: 兩欄佈局（Mode cards 並排）
- Step 2: 可考慮左右分欄（人數 | 預算）

---

## 📝 D-007 任務完成報告

### 完成項目
✅ 設計 4 個步驟的完整流程
✅ Step 1: 餐廳搜尋 + AI 推薦選項
✅ Step 2: 人數與預算設定（快選 + 滑桿）
✅ Step 3: 用餐模式選擇（大卡片）
✅ Step 4: 偏好與禁忌（標籤輸入）
✅ 定義頁面轉場動畫
✅ 定義資料結構與驗證
✅ 規劃資料持久化策略
✅ 無障礙與響應式規範

### 交付物
- `D-007-INPUT-PAGE-DESIGN.md` - 完整輸入頁設計規格

### 設計重點

#### 漸進式揭露:
- 一次只顯示一個步驟，降低認知負擔
- StepIndicator 提供清晰進度回饋
- 每步驟都有「上一步」選項，允許修改

#### 輸入優化:
- **Step 2**: 提供快選按鈕（2/4/6 人），降低輸入成本
- **Step 3**: 大卡片 + emoji，清楚視覺化選項
- **Step 4**: 快選標籤 + 自訂輸入，兼顧效率與彈性

#### 彈性設計:
- Step 4 為選填（但鼓勵填寫以提升推薦品質）
- Step 1 提供「AI 推薦餐廳」選項（無特定餐廳時）
- 所有資料自動儲存，關閉瀏覽器也不會遺失

### 實際執行事項（設計師需完成）

**今日完成** (5 小時):
1. 在 Figma 建立 Input Page Frame (4 個 Steps)
2. 設計 Step 1（RestaurantSearch component 實例）
3. 設計 Step 2（人數快選 + BudgetSlider）
4. 設計 Step 3（ModeSelector 大卡片）
5. 設計 Step 4（TagInput + Checkboxes）

**明日完成** (2 小時):
6. 設計 StepIndicator 的 4 種狀態
7. 建立 Desktop 版本（主要是 Step 3 並排）
8. 設計頁面轉場動畫原型
9. 測試所有互動流程

### 技術考量

- 使用 React Context 管理跨步驟狀態
- Framer Motion AnimatePresence 處理步驟切換
- LocalStorage 自動儲存（每次 onChange）
- 表單驗證在「下一步」時觸發

### 下一步
D-008: 推薦頁面設計（Recommendation Page - 核心頁面）

---

**任務狀態**: ✅ 規格完成
**建立時間**: 2025-01-26
**預估時間**: 5 小時（規格建立） + 7 小時（實際設計）
