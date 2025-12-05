# Carte AI - 設計交接文件
> 供 IDE LLM (Cursor, Copilot, Windsurf) 使用的完整設計規範

---

## 1. 專案概述

**產品名稱**: Carte AI  
**產品定位**: AI 驅動的餐廳菜單推薦助手  
**設計風格**: Modern Bistro Editorial  
**目標用戶**: 25-45 歲都市專業人士

### 核心用戶流程
\`\`\`
Landing → Input (4步驟) → Waiting (AI處理) → Recommendation → Final Menu
\`\`\`

---

## 2. 設計系統 (Design Tokens)

### 2.1 色彩系統 (必須在 globals.css 設定)

\`\`\`css
/* CSS Variables - 加入到 :root */
--color-charcoal: #2C2C2C;      /* 主要文字、標題 */
--color-caramel: #D4A574;       /* 主要 CTA、漸層起點 */
--color-terracotta: #C77B5F;    /* 次要強調、漸層終點 */
--color-cream: #F9F6F0;         /* 背景色 */
--color-cream-dark: #EDE8E0;    /* 卡片背景、hover 狀態 */

/* Tailwind 主題對應 */
--background: var(--color-cream);
--foreground: var(--color-charcoal);
--primary: var(--color-caramel);
--primary-foreground: #FFFFFF;
--secondary: var(--color-terracotta);
--muted: var(--color-cream-dark);
--accent: var(--color-terracotta);
\`\`\`

### 2.2 漸層按鈕 (核心 UI 元素)

\`\`\`css
/* Primary Button Gradient */
.btn-primary {
  background: linear-gradient(135deg, #D4A574 0%, #C77B5F 100%);
  color: white;
  border-radius: 9999px; /* fully rounded */
  padding: 12px 32px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
  box-shadow: 0 10px 40px -10px rgba(212, 165, 116, 0.5);
}

/* Tailwind 寫法 */
className="bg-gradient-to-br from-caramel to-terracotta text-white rounded-full px-8 py-3 font-medium hover:brightness-105 hover:-translate-y-0.5 transition-all shadow-lg hover:shadow-caramel/30"
\`\`\`

### 2.3 字體系統

\`\`\`css
/* Google Fonts 引入 */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* 字體變數 */
--font-serif: 'Cormorant Garamond', Georgia, serif;  /* 標題用 */
--font-sans: 'Inter', system-ui, sans-serif;         /* 內文用 */
\`\`\`

### 2.4 字體尺寸規範

| 元素 | 尺寸 | 字重 | 字體 | Tailwind Class |
|------|------|------|------|----------------|
| H1 | 48px | 600 | Serif | `text-5xl font-serif font-semibold` |
| H2 | 32px | 600 | Serif | `text-3xl font-serif font-semibold` |
| H3 | 24px | 500 | Serif | `text-2xl font-serif font-medium` |
| Body | 16px | 400 | Sans | `text-base font-sans` |
| Caption | 12px | 400 | Sans | `text-xs font-sans text-muted-foreground` |

### 2.5 間距系統 (8px base)

| Token | 值 | 用途 |
|-------|-----|------|
| spacing-xs | 4px | 緊密元素間距 |
| spacing-sm | 8px | 內部 padding |
| spacing-md | 16px | 標準間距 |
| spacing-lg | 24px | 區塊間距 |
| spacing-xl | 32px | 大區塊間距 |
| spacing-2xl | 48px | Section 間距 |

### 2.6 陰影系統

\`\`\`css
/* 三層陰影 */
--shadow-subtle: 0 2px 8px rgba(44, 44, 44, 0.06);
--shadow-medium: 0 4px 20px rgba(44, 44, 44, 0.1);
--shadow-prominent: 0 10px 40px rgba(44, 44, 44, 0.15);
--shadow-floating: 0 20px 60px -10px rgba(212, 165, 116, 0.3);

/* Tailwind 自定義 */
shadow-subtle: '0 2px 8px rgba(44, 44, 44, 0.06)'
shadow-floating: '0 20px 60px -10px rgba(212, 165, 116, 0.3)'
\`\`\`

### 2.7 圓角系統

| Token | 值 | 用途 |
|-------|-----|------|
| rounded-sm | 8px | 小元素 |
| rounded-md | 12px | 按鈕、輸入框 |
| rounded-lg | 16px | 卡片 |
| rounded-xl | 20px | 大卡片 |
| rounded-2xl | 24px | Modal |
| rounded-full | 9999px | Pill 按鈕、Tag |

---

## 3. 頁面結構與路由

### 3.1 路由表

| 路由 | 頁面 | 狀態 |
|------|------|------|
| `/` | Landing Page | 必建 |
| `/onboarding` | 首次使用引導 | 必建 |
| `/input` | 4 步驟輸入表單 | 必建 |
| `/waiting` | AI 處理等待畫面 | 必建 |
| `/recommendation` | 菜色推薦結果 | 必建 |
| `/final-menu` | 最終菜單確認 | 必建 |
| `/error` | 錯誤狀態展示 | 必建 |

### 3.2 頁面詳細規格

#### Landing Page (`/`)
\`\`\`
結構:
├── Header (Logo + Nav)
├── Hero Section
│   ├── H1: "讓 AI 為您規劃完美的用餐體驗"
│   ├── Subtitle: 描述文字
│   └── CTA Button: "開始探索" → /input
├── Features Section (3 cards)
│   ├── 智慧分析
│   ├── 個人化推薦
│   └── 即時更新
├── How It Works (3 steps)
└── Footer
\`\`\`

#### Input Page (`/input`)
\`\`\`
結構:
├── Progress Bar (4 步驟指示器)
├── Step Content (根據當前步驟切換)
│   ├── Step 1: 餐廳搜尋 (Search Input)
│   ├── Step 2: 用餐模式 (3 選項卡片)
│   ├── Step 3: 用餐人數 (數字選擇器)
│   └── Step 4: 飲食偏好 (多選 Pill)
├── Navigation
│   ├── Back Button (Steps 2-4)
│   └── Next/Submit Button
└── Step Indicator Text

互動狀態:
- 選項卡片: Default → Hover (border-caramel/30) → Selected (border-caramel + checkmark)
- Pill Tags: Default (outline) → Selected (filled caramel)
- 進度條: 已完成 (caramel fill) + 當前 (pulse animation)
\`\`\`

#### Waiting Screen (`/waiting`)
\`\`\`
結構:
├── Animated Icon (根據階段變化)
├── Phase Title
├── Phase Description
├── Progress Indicator
└── Transparency Stream (AI 思考過程)

三階段動畫 (每階段 2-3 秒):
1. 探索階段: "正在探索菜單..." + 搜尋動畫
2. 分析階段: "分析您的偏好..." + 處理動畫
3. 生成階段: "生成推薦菜單..." + 完成動畫

完成後自動跳轉 → /recommendation
\`\`\`

#### Recommendation Page (`/recommendation`)
\`\`\`
結構 (Desktop):
├── 左側: 菜色卡片列表 (2/3 寬度)
│   ├── 分類標題 (前菜、主菜、甜點...)
│   └── Dish Cards (可選擇)
└── 右側: Menu Summary Sidebar (1/3 寬度, sticky)
    ├── 已選菜色列表
    ├── 預估總價
    └── 確認按鈕 → /final-menu

結構 (Mobile):
├── 菜色卡片列表 (全寬)
└── Bottom Fixed Bar (已選數量 + 確認按鈕)

Dish Card 規格:
├── 圖片 (aspect-video, rounded-lg)
├── 菜名 (font-serif, text-lg)
├── 價格 (font-medium)
├── AI 推薦理由 (text-sm, text-muted)
├── Tags (Pill: 招牌、素食、辣...)
└── Selection Checkbox (右上角)
\`\`\`

#### Final Menu Page (`/final-menu`)
\`\`\`
結構:
├── Success Header
│   ├── Checkmark Animation
│   └── "您的菜單已準備好"
├── Menu Card (所有已選菜色)
├── Total Summary
├── Action Buttons
│   ├── 分享菜單 (LINE/複製連結)
│   ├── 在 Google Maps 開啟
│   └── 重新選擇
└── Restaurant Info Card
\`\`\`

---

## 4. 共用元件清單

### 4.1 必建元件

| 元件 | 路徑 | 用途 |
|------|------|------|
| Header | `components/carte/header.tsx` | 全站導覽 |
| Footer | `components/carte/footer.tsx` | 全站頁尾 |
| ProgressBar | `components/carte/progress-bar.tsx` | Input 頁步驟指示 |
| DishCard | `components/carte/dish-card.tsx` | 菜色卡片 |
| MenuSummary | `components/carte/menu-summary.tsx` | 側邊摘要 |
| EmptyState | `components/carte/empty-state.tsx` | 空狀態 |
| ErrorState | `components/carte/error-state.tsx` | 錯誤狀態 |
| Onboarding | `components/carte/onboarding.tsx` | 引導流程 |

### 4.2 步驟元件 (Input Page)

| 元件 | 路徑 |
|------|------|
| StepRestaurant | `components/carte/step-restaurant.tsx` |
| StepDiningMode | `components/carte/step-dining-mode.tsx` |
| StepPartySize | `components/carte/step-party-size.tsx` |
| StepPreferences | `components/carte/step-preferences.tsx` |

---

## 5. 互動狀態規範

### 5.1 按鈕狀態

\`\`\`tsx
// Primary Button (漸層)
const primaryButton = {
  default: "bg-gradient-to-br from-caramel to-terracotta text-white",
  hover: "hover:brightness-105 hover:-translate-y-0.5 hover:shadow-floating",
  active: "active:scale-[0.98]",
  disabled: "opacity-50 cursor-not-allowed",
  loading: "animate-pulse"
}

// Secondary Button (outline)
const secondaryButton = {
  default: "border-2 border-charcoal/20 text-charcoal bg-transparent",
  hover: "hover:border-caramel hover:text-caramel",
  active: "active:bg-caramel/5"
}

// Ghost Button
const ghostButton = {
  default: "text-charcoal/70 bg-transparent",
  hover: "hover:text-charcoal hover:bg-cream-dark"
}
\`\`\`

### 5.2 卡片選擇狀態

\`\`\`tsx
// Selection Card
const selectionCard = {
  default: "border-2 border-transparent bg-white shadow-subtle",
  hover: "hover:border-caramel/30 hover:shadow-medium",
  selected: "border-caramel bg-caramel/5 shadow-medium",
  disabled: "opacity-50 cursor-not-allowed"
}
\`\`\`

### 5.3 輸入框狀態

\`\`\`tsx
const inputField = {
  default: "border border-charcoal/20 bg-white rounded-xl px-4 py-3",
  focus: "focus:border-caramel focus:ring-2 focus:ring-caramel/20",
  error: "border-red-500 focus:ring-red-500/20",
  disabled: "bg-cream-dark opacity-50"
}
\`\`\`

---

## 6. 響應式斷點

\`\`\`css
/* Tailwind 預設斷點 */
sm: 640px   /* 大手機 */
md: 768px   /* 平板 */
lg: 1024px  /* 小桌面 */
xl: 1280px  /* 大桌面 */

/* 佈局變化 */
Mobile (< 768px):
- 單欄佈局
- Bottom fixed bar 取代 sidebar
- 漢堡選單

Tablet (768px - 1024px):
- 2 欄網格
- Sidebar 可收合

Desktop (> 1024px):
- 3 欄網格
- Sticky sidebar
\`\`\`

---

## 7. 動畫規範

### 7.1 基礎過渡

\`\`\`css
/* 標準過渡 */
transition-all duration-200 ease-out

/* 彈性過渡 */
transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]
\`\`\`

### 7.2 微互動

\`\`\`tsx
// Hover lift
"hover:-translate-y-1 transition-transform"

// Scale on press
"active:scale-[0.98] transition-transform"

// Fade in
"animate-in fade-in duration-300"

// Slide up
"animate-in slide-in-from-bottom-4 duration-300"
\`\`\`

### 7.3 Loading 動畫

\`\`\`tsx
// Pulse
"animate-pulse"

// Spin
"animate-spin"

// Bounce
"animate-bounce"

// Custom skeleton
"animate-pulse bg-gradient-to-r from-cream-dark via-cream to-cream-dark bg-[length:200%_100%]"
\`\`\`

---

## 8. 錯誤與空狀態

### 8.1 錯誤狀態類型

| 類型 | 標題 | 描述 | CTA |
|------|------|------|-----|
| network | 網路連線失敗 | 請檢查網路連線 | 重試 |
| server | 伺服器忙碌中 | 請稍後再試 | 重試 |
| timeout | 請求逾時 | 處理時間過長 | 重試 |
| not-found | 找不到餐廳 | 請嘗試其他關鍵字 | 重新搜尋 |

### 8.2 空狀態類型

| 類型 | 標題 | 描述 |
|------|------|------|
| no-restaurant | 找不到餐廳 | 請嘗試其他搜尋條件 |
| no-reviews | 暫無評論 | 成為第一個評論者 |
| no-selection | 尚未選擇菜色 | 點擊菜色卡片開始選擇 |
| no-results | 無符合結果 | 調整篩選條件 |

---

## 9. Tailwind 配置

### 9.1 tailwind.config.js 擴展

\`\`\`js
// 如果使用 Tailwind v3，加入以下配置
module.exports = {
  theme: {
    extend: {
      colors: {
        charcoal: '#2C2C2C',
        caramel: '#D4A574',
        terracotta: '#C77B5F',
        cream: {
          DEFAULT: '#F9F6F0',
          dark: '#EDE8E0'
        }
      },
      fontFamily: {
        serif: ['Cormorant Garamond', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      boxShadow: {
        'subtle': '0 2px 8px rgba(44, 44, 44, 0.06)',
        'medium': '0 4px 20px rgba(44, 44, 44, 0.1)',
        'prominent': '0 10px 40px rgba(44, 44, 44, 0.15)',
        'floating': '0 20px 60px -10px rgba(212, 165, 116, 0.3)'
      }
    }
  }
}
\`\`\`

### 9.2 globals.css (Tailwind v4)

\`\`\`css
@import 'tailwindcss';

@theme inline {
  --font-serif: 'Cormorant Garamond', Georgia, serif;
  --font-sans: 'Inter', system-ui, sans-serif;
  
  --color-charcoal: #2C2C2C;
  --color-caramel: #D4A574;
  --color-terracotta: #C77B5F;
  --color-cream: #F9F6F0;
  --color-cream-dark: #EDE8E0;
  
  --shadow-subtle: 0 2px 8px rgba(44, 44, 44, 0.06);
  --shadow-medium: 0 4px 20px rgba(44, 44, 44, 0.1);
  --shadow-floating: 0 20px 60px -10px rgba(212, 165, 116, 0.3);
}

@layer base {
  :root {
    --background: var(--color-cream);
    --foreground: var(--color-charcoal);
    --primary: var(--color-caramel);
    --primary-foreground: #ffffff;
    --secondary: var(--color-terracotta);
    --muted: var(--color-cream-dark);
    --muted-foreground: #6b6b6b;
    --accent: var(--color-terracotta);
    --radius: 0.75rem;
  }
}
\`\`\`

---

## 10. 遷移指令 (給 LLM)

將以下指令複製到你的 IDE LLM：

\`\`\`
請根據以下設計規範，將 Carte AI 的設計遷移到我的專案中：

1. 設計風格：Modern Bistro Editorial
2. 色彩：Charcoal (#2C2C2C)、Caramel (#D4A574)、Terracotta (#C77B5F)、Cream (#F9F6F0)
3. 字體：Cormorant Garamond (標題) + Inter (內文)
4. 主要 CTA 按鈕使用 caramel → terracotta 漸層

請建立以下頁面和元件：
- Landing Page (/)
- Input Page (/input) - 4 步驟表單
- Waiting Screen (/waiting) - AI 處理動畫
- Recommendation Page (/recommendation) - 菜色卡片 + 側邊摘要
- Final Menu Page (/final-menu)
- Error/Empty States

所有元件放在 components/carte/ 目錄下。
確保所有互動狀態 (hover, active, selected, disabled) 都有定義。
支援響應式設計 (mobile-first)。
\`\`\`

---

## 11. 檔案結構

\`\`\`
app/
├── page.tsx                    # Landing
├── layout.tsx                  # Root layout (fonts, metadata)
├── globals.css                 # Design tokens
├── loading.tsx                 # Global loading
├── input/
│   └── page.tsx               # 4-step form
├── waiting/
│   └── page.tsx               # AI processing
├── recommendation/
│   └── page.tsx               # Dish cards
├── final-menu/
│   └── page.tsx               # Confirmation
├── onboarding/
│   └── page.tsx               # First-time guide
└── error/
    └── page.tsx               # Error states demo

components/
└── carte/
    ├── header.tsx
    ├── footer.tsx
    ├── progress-bar.tsx
    ├── dish-card.tsx
    ├── menu-summary.tsx
    ├── empty-state.tsx
    ├── error-state.tsx
    ├── onboarding.tsx
    ├── step-restaurant.tsx
    ├── step-dining-mode.tsx
    ├── step-party-size.tsx
    └── step-preferences.tsx
\`\`\`

---

## 12. 快速複製區塊

### Primary Button
\`\`\`tsx
<button className="bg-gradient-to-br from-caramel to-terracotta text-white rounded-full px-8 py-3 font-medium hover:brightness-105 hover:-translate-y-0.5 transition-all shadow-lg hover:shadow-floating active:scale-[0.98]">
  開始探索
</button>
\`\`\`

### Selection Card
\`\`\`tsx
<div className={cn(
  "border-2 rounded-2xl p-6 cursor-pointer transition-all",
  selected 
    ? "border-caramel bg-caramel/5 shadow-medium" 
    : "border-transparent bg-white shadow-subtle hover:border-caramel/30"
)}>
  {/* content */}
</div>
\`\`\`

### Dish Card
\`\`\`tsx
<div className="bg-white rounded-2xl shadow-subtle overflow-hidden hover:shadow-medium transition-shadow">
  <div className="aspect-video relative">
    <Image src={image || "/placeholder.svg"} alt={name} fill className="object-cover" />
  </div>
  <div className="p-4">
    <h3 className="font-serif text-lg font-semibold text-charcoal">{name}</h3>
    <p className="text-caramel font-medium">${price}</p>
    <p className="text-sm text-charcoal/60 mt-2">{aiReason}</p>
  </div>
</div>
\`\`\`

---

*最後更新: 2024-12*
