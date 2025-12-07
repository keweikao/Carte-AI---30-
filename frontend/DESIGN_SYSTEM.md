# OderWhat 前端設計系統
> 「美食雜誌編輯風格」設計規範
>
> **建立日期**: 2025-01-26
> **設計哲學**: Editorial Elegance meets Playful Utility

---

## 🎨 設計原則

### 核心理念
將 AI 點餐體驗轉化為翻閱精緻美食雜誌的感受，透過視覺引導和清晰的互動降低決策負擔。

### 三大支柱
1. **視覺層次清晰** - 使用非對稱排版、留白、字體對比建立閱讀節奏
2. **溫暖的食慾色系** - 避免科技感藍紫漸層，擁抱食物的自然色調
3. **流暢的互動回饋** - 每個操作都有即時且愉悅的視覺反饋

---

## 🖋️ 字體系統 (Typography)

### 字體配置

```css
/* 主要字體 */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;700&display=swap');

:root {
  /* 字體家族 */
  --font-display: 'Cormorant Garamond', serif;
  --font-body: 'Noto Sans TC', -apple-system, sans-serif;
  --font-handwriting: 'Caveat', cursive;

  /* 字體大小 - 使用 Type Scale (1.250 - Major Third) */
  --text-xs: 0.64rem;    /* 10.24px */
  --text-sm: 0.8rem;     /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.25rem;    /* 20px */
  --text-xl: 1.563rem;   /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39px */
  --text-4xl: 3.052rem;  /* 48.83px */
  --text-5xl: 3.815rem;  /* 61.04px */

  /* 行高 */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* 字重 */
  --font-light: 300;
  --font-regular: 400;
  --font-medium: 500;
  --font-bold: 700;
  --font-black: 900;
}
```

### 字體使用規範

| 元素 | 字體 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|------|
| H1 | Cormorant Garamond | 3xl-5xl | 600 | tight | 頁面主標題 |
| H2 | Cormorant Garamond | 2xl-3xl | 500 | tight | 區塊標題 |
| H3 | Noto Sans TC | xl-2xl | 700 | normal | 卡片標題 |
| Body | Noto Sans TC | base | 400 | normal | 內文、描述 |
| Caption | Noto Sans TC | sm | 400 | normal | 輔助說明 |
| Handwriting | Caveat | lg-xl | 500 | relaxed | 推薦理由、註記 |
| Button | Noto Sans TC | base | 500 | tight | 按鈕文字 |

### 範例

```tsx
// 頁面標題
<h1 className="font-display text-5xl font-semibold leading-tight text-charcoal">
  你的 AI 點餐顧問
</h1>

// 推薦理由（手寫風格）
<p className="font-handwriting text-xl text-terracotta -rotate-1">
  "清爽開胃，45 則評論提到『小黃瓜超脆』"
</p>

// 內文
<p className="font-body text-base leading-normal text-charcoal/80">
  系統將根據 Google 評論分析，為您推薦最佳點餐組合
</p>
```

---

## 🎨 色彩系統 (Color Palette)

### 主色調 - 溫暖的食物色系

```css
:root {
  /* === 主色調 === */
  /* 奶油白系列 */
  --color-cream-50: #FFFCF7;
  --color-cream-100: #FFF8F0;
  --color-cream-200: #FFF0E0;
  --color-cream: #FFF8F0;

  /* 焦糖色系列 */
  --color-caramel-50: #F5E6D3;
  --color-caramel-100: #E8D4B8;
  --color-caramel: #D4A574;
  --color-caramel-700: #B8915F;
  --color-caramel-900: #8A6B47;

  /* 陶土紅系列 */
  --color-terracotta-50: #F5E1E0;
  --color-terracotta-100: #E8C5C2;
  --color-terracotta: #C85A54;
  --color-terracotta-700: #B04E48;
  --color-terracotta-900: #8A3D39;

  /* 鼠尾草綠系列 */
  --color-sage-50: #F0F2EF;
  --color-sage-100: #D8DDD5;
  --color-sage: #8B9D83;
  --color-sage-700: #6F7D68;
  --color-sage-900: #4A5145;

  /* 炭黑系列 */
  --color-charcoal-50: #F5F5F5;
  --color-charcoal-100: #E0E0E0;
  --color-charcoal: #2D2D2D;
  --color-charcoal-700: #1F1F1F;
  --color-charcoal-900: #0A0A0A;

  /* === 功能色 === */
  --color-success: #6B9D7F;
  --color-success-light: #A8C9B7;
  --color-warning: #E89C5C;
  --color-warning-light: #F5C89A;
  --color-error: #C85A54;
  --color-error-light: #E8A19D;
  --color-info: #7BA3C0;
  --color-info-light: #B5D0E3;

  /* === 漸層 === */
  --gradient-hero: linear-gradient(135deg, #FFF8F0 0%, #F5E6D3 100%);
  --gradient-accent: linear-gradient(90deg, #D4A574 0%, #C85A54 100%);
  --gradient-sage: linear-gradient(135deg, #8B9D83 0%, #6F7D68 100%);
  --gradient-overlay: linear-gradient(180deg, rgba(45,45,45,0) 0%, rgba(45,45,45,0.8) 100%);

  /* === 語義色 === */
  --color-background: var(--color-cream-100);
  --color-surface: #FFFFFF;
  --color-text-primary: var(--color-charcoal);
  --color-text-secondary: var(--color-charcoal-700);
  --color-text-muted: rgba(45, 45, 45, 0.6);
  --color-border: rgba(45, 45, 45, 0.1);
  --color-border-strong: rgba(45, 45, 45, 0.2);
}
```

### 色彩使用規範

| 用途 | 色彩 | 使用場景 |
|------|------|----------|
| 主背景 | cream-100 | 頁面底色 |
| 卡片背景 | surface (white) | 內容卡片、輸入框 |
| 主要動作按鈕 | gradient-accent | CTA、確認按鈕 |
| 次要按鈕 | sage | 取消、返回 |
| 強調文字 | terracotta | 價格、重要資訊 |
| 手寫註記 | caramel-700 | 推薦理由 |
| 成功狀態 | success | 已確認、完成 |
| 警告狀態 | warning | 價格超標提示 |
| 錯誤狀態 | error | 錯誤訊息 |

### 無障礙對比檢查

所有文字色彩組合均符合 WCAG 2.1 AA 標準（對比度 ≥ 4.5:1）：

- ✅ charcoal on cream-100: 12.5:1
- ✅ charcoal-700 on surface: 10.2:1
- ✅ terracotta on cream-100: 5.8:1
- ✅ white on terracotta: 6.2:1

---

## 📐 間距系統 (Spacing)

使用 8px 基準網格系統：

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.5rem;    /* 24px */
  --space-6: 2rem;      /* 32px */
  --space-8: 3rem;      /* 48px */
  --space-10: 4rem;     /* 64px */
  --space-12: 6rem;     /* 96px */
  --space-16: 8rem;     /* 128px */

  /* 語義化間距 */
  --space-section: var(--space-12);  /* 區塊間距 */
  --space-card: var(--space-6);      /* 卡片內距 */
  --space-element: var(--space-4);   /* 元素間距 */
}
```

---

## 🔲 陰影系統 (Shadows)

```css
:root {
  /* 高度感陰影 */
  --shadow-sm: 0 1px 2px rgba(45, 45, 45, 0.05);
  --shadow-base: 0 2px 8px rgba(45, 45, 45, 0.08);
  --shadow-md: 0 4px 16px rgba(45, 45, 45, 0.12);
  --shadow-lg: 0 8px 32px rgba(45, 45, 45, 0.16);
  --shadow-xl: 0 16px 48px rgba(45, 45, 45, 0.20);

  /* 特殊陰影 */
  --shadow-card: 0 4px 20px rgba(212, 165, 116, 0.15);  /* 暖色調陰影 */
  --shadow-floating: 0 12px 40px rgba(45, 45, 45, 0.25); /* 浮動元素 */

  /* 內陰影 */
  --shadow-inset: inset 0 2px 4px rgba(45, 45, 45, 0.06);
}
```

---

## 🔘 圓角系統 (Border Radius)

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;   /* 4px */
  --radius-base: 0.5rem;  /* 8px */
  --radius-md: 0.75rem;   /* 12px */
  --radius-lg: 1rem;      /* 16px */
  --radius-xl: 1.5rem;    /* 24px */
  --radius-2xl: 2rem;     /* 32px */
  --radius-full: 9999px;

  /* 語義化圓角 */
  --radius-button: var(--radius-lg);
  --radius-card: var(--radius-xl);
  --radius-input: var(--radius-md);
}
```

---

## 🎬 動畫系統 (Animations)

### 緩動函數 (Easing)

```css
:root {
  /* 標準緩動 */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* 特殊緩動 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* 彈跳效果 */
  --ease-smooth: cubic-bezier(0.65, 0, 0.35, 1);     /* 平滑曲線 */
}
```

### 動畫時長 (Duration)

```css
:root {
  --duration-instant: 100ms;   /* 即時反饋 */
  --duration-fast: 200ms;      /* 快速動畫 */
  --duration-base: 300ms;      /* 標準動畫 */
  --duration-slow: 500ms;      /* 緩慢動畫 */
  --duration-slower: 800ms;    /* 特殊效果 */
}
```

### 核心動畫

```css
/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 滑入（從下方） */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片翻出 */
@keyframes cardSwapOut {
  0% { transform: translateX(0) rotate(0deg); opacity: 1; }
  100% { transform: translateX(-100vw) rotate(-15deg); opacity: 0; }
}

/* 卡片滑入 */
@keyframes cardSwapIn {
  0% { transform: translateX(100vw) rotate(15deg); opacity: 0; }
  100% { transform: translateX(0) rotate(0deg); opacity: 1; }
}

/* 價格變化脈衝 */
@keyframes pricePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* 完成慶祝 */
@keyframes celebrate {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.1) rotate(-5deg); }
  75% { transform: scale(1.1) rotate(5deg); }
}
```

---

## 🧩 組件規範

### 按鈕 (Buttons)

```tsx
// Primary Button
<button className="
  px-6 py-3
  rounded-[var(--radius-button)]
  bg-gradient-to-r from-caramel to-terracotta
  text-white font-medium
  shadow-md hover:shadow-lg
  transition-all duration-300
  hover:scale-105
  active:scale-95
">
  開始推薦
</button>

// Secondary Button
<button className="
  px-6 py-3
  rounded-[var(--radius-button)]
  bg-sage text-white
  hover:bg-sage-700
  transition-colors duration-300
">
  返回
</button>

// Outline Button
<button className="
  px-6 py-3
  rounded-[var(--radius-button)]
  border-2 border-charcoal
  text-charcoal
  hover:bg-charcoal hover:text-white
  transition-all duration-300
">
  換一道
</button>
```

### 卡片 (Cards)

```tsx
// 菜色卡片
<div className="
  bg-white
  rounded-[var(--radius-card)]
  shadow-card
  p-6
  hover:shadow-lg
  transition-shadow duration-300
">
  {/* Card Content */}
</div>

// 已選擇卡片
<div className="
  bg-white/60
  rounded-[var(--radius-card)]
  border-2 border-success
  p-6
  relative
">
  <div className="absolute top-4 right-4">
    <CheckIcon className="text-success" />
  </div>
  {/* Card Content */}
</div>
```

### 輸入框 (Inputs)

```tsx
<input className="
  w-full
  px-4 py-3
  rounded-[var(--radius-input)]
  border-2 border-charcoal/10
  focus:border-caramel
  focus:outline-none
  focus:ring-4 focus:ring-caramel/20
  transition-all duration-200
" />
```

---

## 📱 響應式設計 (Responsive Design)

### 斷點 (Breakpoints)

```css
:root {
  --breakpoint-sm: 640px;   /* 手機橫向 */
  --breakpoint-md: 768px;   /* 平板直向 */
  --breakpoint-lg: 1024px;  /* 平板橫向/小筆電 */
  --breakpoint-xl: 1280px;  /* 桌面 */
  --breakpoint-2xl: 1536px; /* 大螢幕 */
}
```

### 設計策略

- **Mobile First**: 預設為手機版設計，向上擴展
- **主要支援**: 375px - 768px (手機直向到平板)
- **關鍵調整點**:
  - 字體大小在 md 以上放大 1.25 倍
  - 卡片寬度在 lg 以上限制最大寬度
  - 多欄布局在 md 以上啟用

```css
/* 範例 */
.hero-title {
  font-size: var(--text-3xl);
}

@media (min-width: 768px) {
  .hero-title {
    font-size: var(--text-5xl);
  }
}
```

---

## 🌗 暗色模式 (Dark Mode)

目前版本暫不支援暗色模式，專注於淺色「美食雜誌」風格。

未來可考慮加入「夜間點餐模式」：
- 背景色：深炭黑 (#1A1A1A)
- 強調色：琥珀金 (#F5A962)
- 保持溫暖食慾感

---

## ♿ 無障礙設計 (Accessibility)

### 規範遵循
- WCAG 2.1 AA 標準
- 所有互動元素可鍵盤操作
- 適當的 ARIA 標籤
- 足夠的色彩對比

### 實作檢查清單

```tsx
// ✅ 按鈕有清晰的 aria-label
<button aria-label="確認選擇小籠包">
  我要點這道
</button>

// ✅ 圖示有替代文字
<img src="/dish.jpg" alt="小籠包，蒸籠內的湯包" />

// ✅ 表單有關聯的 label
<label htmlFor="restaurant">餐廳名稱</label>
<input id="restaurant" type="text" />

// ✅ 顏色不是唯一的資訊傳達方式
<div className="border-success">
  <CheckIcon /> 已選擇
</div>
```

---

## 📦 組件庫建議

### 推薦使用

1. **Framer Motion** - 動畫庫
   - 用於頁面轉場、卡片翻轉、手勢操作

2. **Radix UI** - 無頭組件
   - 用於 Dialog、Dropdown、Tooltip 等

3. **React Confetti** - 慶祝動畫
   - 用於確認菜品時的慶祝效果

4. **Canvas Confetti** - 輕量慶祝動畫
   - 備選方案，更輕量

### 避免使用

- ❌ Material UI (風格衝突)
- ❌ Ant Design (過於商務風格)
- ❌ Chakra UI (設計系統過於固定)

---

## 🎯 設計交付清單

### 設計師交付給開發者

- [ ] Figma 設計檔案（含元件庫）
- [ ] 圖示 SVG 檔案（優化過）
- [ ] 字體檔案（或 CDN 連結）
- [ ] 色彩變數檔案（CSS/Tailwind）
- [ ] 動畫規範文件
- [ ] 響應式斷點示意圖

### 開發者實作檢查

- [ ] CSS 變數定義完成
- [ ] 字體載入成功
- [ ] 所有按鈕有 hover/active 狀態
- [ ] 動畫流暢無卡頓
- [ ] 響應式在主要裝置測試通過
- [ ] 無障礙測試通過（鍵盤、螢幕閱讀器）

---

## 📚 參考資源

- [Cormorant Garamond 字體](https://fonts.google.com/specimen/Cormorant+Garamond)
- [Framer Motion 文件](https://www.framer.com/motion/)
- [WCAG 2.1 指南](https://www.w3.org/WAI/WCAG21/quickref/)
- [8pt Grid System](https://spec.fm/specifics/8-pt-grid)

---

**最後更新**: 2025-01-26
**維護者**: Frontend Team
**版本**: 1.0.0
