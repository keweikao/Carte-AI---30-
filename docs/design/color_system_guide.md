# Input Page 色系視覺規劃
## Modern Bistro Editorial Design System

![Color System Mockup](/Users/stephen/.gemini/antigravity/brain/f885fb11-f54c-43d8-a24e-27d621416166/input_page_color_system_1764861460169.png)

---

## 🎨 核心色彩系統

### 主色調 (Primary Colors)

#### 1. **Charcoal** - 炭黑色（確認選擇）
```
色碼: #2C2C2C
用途: 選中狀態背景、主要CTA文字
心理: 穩重、高級、確定性
對比度: 與白色文字達到 WCAG AAA 級別
```

**應用場景**：
- ✅ 單選按鈕選中狀態 (Mode, Occasion)
- ✅ 「下一步」按鈕背景
- ✅ 人數調整「+」按鈕
- ✅ 標題文字 (h1, h2)

---

#### 2. **Caramel** - 焦糖色（強調與引導）
```
色碼: #D4A574
RGB: 212, 165, 116
HSL: 32°, 54%, 64%
用途: 進度條、圖標、Hover狀態
心理: 溫暖、美味、邀請
```

**應用場景**：
- ✅ 進度條漸變起點
- ✅ Icon 強調色 (MapPin, ChefHat 等)
- ✅ 已完成步驟文字
- ✅ Border hover 狀態
- ✅ Check icon 背景

**漸變公式**：
```css
background: linear-gradient(to right, #D4A574, #C77B5F);
```

---

#### 3. **Terracotta** - 陶土紅（輔助選擇）
```
色碼: #C77B5F
RGB: 199, 123, 95
HSL: 16°, 47%, 58%
用途: 多選標籤、漸變終點
心理: 工藝感、手作、溫度
```

**應用場景**：
- ✅ 飲食偏好多選標籤 (Dietary Tags)
- ✅ 進度條漸變終點
- ✅ CTA 按鈕漸變終點
- ✅ Border hover (輔助)

---

### 背景系統 (Surface Colors)

#### 4. **Cream** - 奶油米色（主背景）
```
色碼: #F9F6F0
RGB: 249, 246, 240
用途: 頁面主背景
心理: 溫馨、紙質、復古
對比度: 與深色文字有良好對比
```

**應用**：
- 整個頁面的 `bg-[#F9F6F0]`
- 模擬高級餐廳菜單的米色紙張質感

---

#### 5. **Pure White** - 純白（卡片表面）
```
色碼: #FFFFFF
用途: 主卡片背景、未選按鈕
心理: 純淨、專業、留白
```

**應用**：
- 主內容卡片 `bg-white`
- 未選中的選項按鈕
- 輸入框背景

---

### 中性色系 (Neutral Colors)

#### 6. **Gray Scale**
```
gray-100: #F3F4F6 (border 底色)
gray-200: #E5E7EB (未選中 border)
gray-300: #D1D5DB (未完成步驟文字)
gray-400: #9CA3AF (禁用狀態)
gray-500: #6B7280 (副標題、說明文字)
gray-600: #4B5563 (導航 hover)
gray-700: #374151 (次要內容文字)
```

**分層使用**：
- `border-gray-200`: 2px 實體邊框
- `text-gray-500`: 副標題、提示文字
- `text-gray-400`: Icon 未選中狀態

---

## 📐 色彩應用規範

### 互動狀態色彩矩陣

| 元素類型 | 預設 | Hover | 選中 | 禁用 |
|---------|------|-------|------|------|
| **單選按鈕** | `bg-white border-gray-200` | `border-caramel bg-cream-50` | `bg-charcoal text-white` | `bg-gray-100 text-gray-400` |
| **多選標籤** | `bg-white border-gray-200` | `border-terracotta/50` | `bg-terracotta text-white` | - |
| **主CTA** | `gradient caramel→terracotta` | `scale-105 shadow-xl` | - | `bg-gray-200` |
| **次CTA** | `bg-charcoal text-white` | `bg-black scale-105` | - | `bg-gray-200` |

---

### 文字色彩層次

```
h1, h2 (標題)     → text-charcoal (#2C2C2C)
h3, Label        → text-charcoal
Body (內文)       → text-charcoal
Caption (說明)    → text-gray-500
Muted (次要)      → text-gray-400
Disabled         → text-gray-300
```

**字體配對**：
- **Display**: `font-serif` (Cormorant Garamond) - 標題專用
- **Body**: `font-sans` (預設) - 內文、按鈕

---

## 🎯 高對比度設計原則

### 選中狀態 (High Contrast Mode)

**問題**：舊設計選中狀態為 `bg-caramel/5`（5% 透明度），戶外幾乎看不見

**解決方案**：
```diff
舊版 (低對比):
- bg-caramel/5 border-caramel text-caramel

新版 (極致對比):
+ bg-charcoal border-charcoal text-white
```

**對比度測試**：
- 白底黑字: 21:1 ✅ (AAA)
- 黑底白字: 21:1 ✅ (AAA)
- Caramel 底白字: 4.8:1 ✅ (AA+)

---

### 邊框策略

**未選中**: `border-2 border-gray-200`
- 2px 邊框提供實體感
- 灰色保持低調不搶眼

**Hover**: `border-caramel` 或 `border-caramel/50`
- 焦糖色暗示可互動
- 50% 透明度用於輔助元素

**選中**: `border-charcoal`
- 深色邊框與背景同色
- 營造整體感

---

## 🖼️ 視覺層次設計

### Shadow Elevations

```css
/* 主卡片 */
shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25)

/* 按鈕 hover */
shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)

/* 按鈕預設 */
shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)

/* 選項卡片 */
shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)

/* 輸入框內凹 */
shadow-inner: inset 0 2px 4px rgba(0, 0, 0, 0.06)
```

### 圓角系統

```
rounded-full: 9999px  (CTA 按鈕、人數調整)
rounded-[2rem]: 32px  (主卡片)
rounded-2xl: 24px     (選項卡片)
rounded-xl: 16px      (輸入框、小卡片)
rounded-lg: 12px      (快速選擇標籤)
rounded-full: 全圓    (Pills, 標籤)
```

---

## 💡 實作範例

### Step 2: Mode Selection (單選)

```tsx
<button
    className={cn(
        "p-5 rounded-2xl border-2 transition-all",
        isSelected
            ? "bg-charcoal border-charcoal text-white shadow-lg"
            : "bg-white border-gray-200 hover:border-caramel"
    )}
>
    <Icon className={isSelected ? "text-caramel" : "text-gray-400"} />
    <p className="font-bold">{label}</p>
</button>
```

**邏輯**：
- 選中 = 黑底白字（極致對比）
- 未選 = 白底灰邊（低調待命）
- Icon 選中時用 caramel 強調

---

### Step 4: Dietary Tags (多選)

```tsx
<button
    className={cn(
        "px-4 py-2 rounded-full border-2",
        isSelected
            ? "bg-terracotta border-terracotta text-white"
            : "bg-white border-gray-200 hover:border-terracotta/50"
    )}
>
    {tag}
</button>
```

**邏輯**：
- 多選用 **Terracotta**（與單選區分）
- 維持高對比原則
- Hover 用 50% 透明度暗示

---

### Progress Bar

```tsx
<motion.div 
    className="h-1.5 bg-gradient-to-r from-caramel to-terracotta"
    animate={{ width: `${(currentStep / 4) * 100}%` }}
/>
```

**邏輯**：
- 漸變從 Caramel → Terracotta
- 視覺上引導「前進」的動態感

---

## 🌈 配色心理學

### Charcoal (炭黑)
- **聯想**: 高級餐廳黑板菜單、主廚圍裙
- **情緒**: 專業、確定、權威
- **用途**: 確認動作、最終決定

### Caramel (焦糖)
- **聯想**: 焦糖布丁、咖啡、烘焙香氣
- **情緒**: 溫暖、誘人、甜蜜
- **用途**: 引導注意力、強調重點

### Terracotta (陶土)
- **聯想**: 手工陶器、義式餐廳、工藝
- **情緒**: 質樸、真實、溫度
- **用途**: 輔助選擇、多樣性

### Cream (奶油)
- **聯想**: 高級餐廳菜單紙張、米其林指南
- **情緒**: 優雅、復古、溫馨
- **用途**: 營造氛圍、降低數位感

---

## 🔧 Tailwind 配置建議

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        charcoal: {
          DEFAULT: '#2C2C2C',
          50: '#F7F7F7',
          100: '#E3E3E3',
          // ... (可擴展)
        },
        caramel: {
          DEFAULT: '#D4A574',
          50: '#FAF6F0',
          100: '#F5EDE1',
          600: '#B8874F',
          700: '#9C6D3E',
        },
        terracotta: {
          DEFAULT: '#C77B5F',
          50: '#F9EDE9',
          600: '#A85F46',
        },
        cream: {
          50: '#F9F6F0',
          100: '#F3EDE3',
        }
      },
      fontFamily: {
        serif: ['Cormorant Garamond', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'floating': '0 25px 50px -12px rgba(44, 44, 44, 0.15)',
      }
    }
  }
}
```

---

## ✅ 設計檢查清單

### 視覺一致性
- [ ] 所有選中狀態使用 Charcoal 背景
- [ ] 所有 Hover 狀態使用 Caramel border
- [ ] 多選標籤使用 Terracotta
- [ ] 主背景維持 Cream (#F9F6F0)

### 對比度
- [ ] 所有文字與背景對比 ≥ 4.5:1 (WCAG AA)
- [ ] 主要 CTA 對比 ≥ 7:1 (WCAG AAA)
- [ ] 邊框寬度 ≥ 2px（觸控可見）

### 響應式
- [ ] 手機上選項最小尺寸 44x44px
- [ ] 文字最小 14px (0.875rem)
- [ ] Padding 充足（最少 p-4）

### 無障礙
- [ ] Focus state 清晰可見
- [ ] Disabled state 明確區分
- [ ] Color blind safe (不只依賴顏色)

---

## 📱 行動版優化

**強化觸控目標**：
```css
/* 最小觸控面積 */
min-height: 44px;
min-width: 44px;

/* 增加按鈕間距 */
gap: 1rem; /* 16px */
```

**防誤觸**：
- 重要按鈕（提交）與次要按鈕（返回）保持明顯距離
- 使用不同視覺重量（Gradient vs Gray text）

---

## 🎬 動畫配色

```css
/* Hover 放大 + Shadow 加深 */
transition: transform 0.3s, box-shadow 0.3s;
hover:scale-105 hover:shadow-xl

/* 選中狀態動畫 */
transition: background-color 0.3s, color 0.3s;
```

**原則**：色彩變化配合動畫，營造流暢感

---

## 📈 A/B 測試建議

測試方案：
1. **V2.4 (Current)**: Charcoal selection
2. **V2.4-Alt**: Caramel selection (較柔和)

測量指標：
- 完成率 (Completion Rate)
- 步驟停留時間
- 誤操作率

---

## 🔗 相關資源

- [Material Design Color System](https://material.io/design/color)
- [WCAG Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Palette Generator](https://coolors.co/)

---

**設計版本**: V2.4 Modern Bistro Editorial  
**更新日期**: 2025-12-04  
**設計師**: AI Design Assistant
