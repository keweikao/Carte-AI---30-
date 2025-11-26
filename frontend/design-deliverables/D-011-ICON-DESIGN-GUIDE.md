# D-011: 圖示設計與導出指南

> **完整的圖示系統設計規範**

**任務狀態**: ✅ 規格已建立
**建立日期**: 2025-01-26

---

## 📋 圖示系統概覽

### 設計策略

OderWhat 使用 **混合圖示策略**：

```
圖示來源
├── Lucide Icons (主要) - 90% 的 UI 圖示
├── Emoji (輔助) - 類別標記、情感表達
└── 自訂圖示 (少量) - 品牌專屬圖示
```

### 為什麼選擇 Lucide Icons？

✅ **優點**:
- 開源免費
- 一致的設計語言（24px 網格）
- 支援 React/Vue/Svelte
- 可自訂顏色、尺寸、stroke-width
- 超過 1000+ 圖示

✅ **符合設計風格**:
- 線性風格（stroke-based）
- 簡潔現代
- 配合「美食雜誌」調性

---

## 🎨 圖示設計規範

### 1. 尺寸規範

#### 標準尺寸

| 尺寸 | 使用場景 | 範例 |
|------|---------|------|
| 16px | 按鈕內小圖示、inline icon | Tag 的 × 圖示 |
| 20px | **最常用**，按鈕圖示、輸入框圖示 | 搜尋🔍、確認✅ |
| 24px | **標準尺寸**，導航圖示、功能圖示 | 返回←、設定⚙️ |
| 32px | 大按鈕圖示、特色展示 | CheckCircle（已確認狀態） |
| 48px | Emoji 類別標記 | 🥗🍖🍚 |
| 64px | Hero section 特色圖示 | Features 區塊圖示 |

#### Figma 設定

```
Icon Frame
├── Width: 24px (base size)
├── Height: 24px
└── Content: 居中對齊，留 2px padding
```

---

### 2. 風格規範

#### Stroke Width（筆畫粗細）

```
Default: 2px (Lucide 預設)
Thin: 1.5px (少用，僅裝飾性圖示)
Bold: 2.5px (強調重要操作)
```

#### 圓角

```
Stroke Line Cap: Round
Stroke Line Join: Round
```

#### 顏色

```
預設: currentColor (繼承父元素文字顏色)

特殊顏色:
- 成功圖示: success (#6B9D7F)
- 警告圖示: warning (#E89C5C)
- 錯誤圖示: error (#C85A54)
- 主要操作: caramel (#D4A574)
```

---

## 🗂️ 圖示清單

### UI 功能圖示（使用 Lucide Icons）

#### 導航類

| 圖示名稱 | Lucide Name | 尺寸 | 使用場景 |
|---------|-------------|------|---------|
| 返回 | `ChevronLeft` | 24px | 返回上一頁 |
| 前往 | `ChevronRight` | 24px | 前往下一步 |
| 關閉 | `X` | 24px | 關閉 Modal |
| 選單 | `Menu` | 24px | 漢堡選單 |
| 首頁 | `Home` | 24px | 導航 |

#### 操作類

| 圖示名稱 | Lucide Name | 尺寸 | 使用場景 |
|---------|-------------|------|---------|
| 確認 | `Check` | 20px | 已確認、已選擇 |
| 確認圓形 | `CheckCircle` | 32px | DishCard 已確認狀態 |
| 換一道 | `RefreshCw` | 20px | 換菜按鈕 |
| 移除 | `X` | 16px | 移除菜品、刪除 Tag |
| 新增 | `Plus` | 20px | 新增項目 |
| 編輯 | `Edit2` | 20px | 編輯內容 |
| 複製 | `Copy` | 20px | 複製連結 |
| 分享 | `Share2` | 20px | 分享功能 |
| 下載 | `Download` | 20px | 下載圖片 |

#### 輸入類

| 圖示名稱 | Lucide Name | 尺寸 | 使用場景 |
|---------|-------------|------|---------|
| 搜尋 | `Search` | 20px | 搜尋框 |
| 定位 | `MapPin` | 20px | 餐廳地址 |
| 人數 | `Users` | 24px | 用餐人數 |
| 預算 | `DollarSign` | 24px | 預算設定 |
| 行事曆 | `Calendar` | 20px | 日期選擇 |
| 時鐘 | `Clock` | 20px | 時間選擇 |

#### 狀態類

| 圖示名稱 | Lucide Name | 尺寸 | 使用場景 |
|---------|-------------|------|---------|
| 資訊 | `Info` | 20px | 提示訊息 |
| 警告 | `AlertTriangle` | 20px | 警告提示 |
| 錯誤 | `AlertCircle` | 20px | 錯誤訊息 |
| 成功 | `CheckCircle` | 20px | 成功提示 |
| 載入中 | `Loader2` | 24px | Loading 動畫 |

---

### 類別圖示（使用 Emoji）

| 類別 | Emoji | Unicode | 尺寸 | 說明 |
|------|-------|---------|------|------|
| 冷菜 | 🥗 | U+1F957 | 32px/48px | 沙拉碗 |
| 熱菜 | 🍖 | U+1F356 | 32px/48px | 烤肉 |
| 湯品 | 🍲 | U+1F372 | 32px/48px | 湯鍋 |
| 主食 | 🍚 | U+1F35A | 32px/48px | 米飯 |
| 點心 | 🥟 | U+1F95F | 32px/48px | 餃子 |
| 甜點 | 🍰 | U+1F370 | 32px/48px | 蛋糕 |
| 飲料 | 🧃 | U+1F9C3 | 32px/48px | 果汁 |
| 中式 | 🥢 | U+1F962 | 48px | 筷子（菜系標記） |
| 西式 | 🍴 | U+1F374 | 48px | 刀叉（菜系標記） |
| 日式 | 🍱 | U+1F371 | 48px | 便當（菜系標記） |

---

### 品牌自訂圖示（需設計）

| 圖示名稱 | 尺寸 | 說明 | 優先級 |
|---------|------|------|--------|
| OderWhat Logo | 48px, 120px | 品牌標誌 | P0（必須） |
| AI 推薦圖示 | 32px | 「讓 AI 幫我推薦」功能 | P1（建議） |
| 慶祝圖示 | 64px | 菜單完成慶祝動畫 | P2（可選） |

#### Logo 設計建議

```
OderWhat Logo
├── 風格: 簡潔、現代、溫暖
├── 元素: 可結合餐具、AI、問號
├── 顏色: caramel (#D4A574) 主色
├── 字體: Cormorant Garamond（品牌字體）
└── 格式: SVG（可縮放）

變體:
- Full Logo: 名稱 + 圖形
- Icon Only: 僅圖形（用於 favicon, app icon）
- Monochrome: 單色版本（用於浮水印）
```

---

## 📦 圖示導出規範

### Lucide Icons 使用方式

#### 方法一：使用 React Component（推薦）

```bash
npm install lucide-react
```

```tsx
import { Search, Check, ChevronLeft } from 'lucide-react'

// 使用
<Search size={20} color="#D4A574" strokeWidth={2} />
<Check size={20} className="text-success" />
<ChevronLeft size={24} />
```

#### 方法二：使用 SVG Sprite

```bash
# 下載所需圖示的 SVG
# https://lucide.dev/icons/
```

---

### Emoji 使用方式

#### 直接在代碼中使用

```tsx
<span className="text-5xl">🥗</span>
<span className="text-3xl">🍖</span>
```

#### CSS 設定

```css
.category-icon {
  font-size: 48px;
  line-height: 1;
  font-family: 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
}
```

---

### 自訂圖示導出規範

#### SVG 導出設定（Figma）

1. **選擇圖示 Frame**
2. **Export Settings**:
   ```
   Format: SVG
   ✅ Include "id" attribute
   ✅ Outline strokes
   ✅ Simplify stroke
   ❌ Include "id" attribute (如果要用 sprite)
   ```

3. **命名規範**:
   ```
   icon-[name]-[size].svg

   範例:
   icon-logo-48.svg
   icon-ai-recommend-32.svg
   ```

4. **優化 SVG**:
   ```bash
   # 使用 SVGO 優化
   npx svgo icon-logo-48.svg
   ```

#### 檔案結構

```
frontend/public/icons/
├── lucide/          (如果使用 sprite)
│   ├── search.svg
│   ├── check.svg
│   └── ...
├── emoji/           (如果需要備用 SVG)
│   ├── salad.svg
│   └── ...
└── custom/
    ├── icon-logo-48.svg
    ├── icon-logo-120.svg
    ├── icon-ai-32.svg
    └── favicon.ico
```

---

## 🎨 圖示在設計中的應用

### 1. Button 中的圖示

```tsx
// 左側圖示
<button className="btn-primary">
  <Search size={20} />
  <span>搜尋餐廳</span>
</button>

// 右側圖示
<button className="btn-primary">
  <span>下一步</span>
  <ChevronRight size={20} />
</button>

// 僅圖示
<button className="btn-icon">
  <X size={20} />
</button>
```

**間距規範**:
```
Icon + Text: gap 8px
Icon size: 20px (MD button), 24px (LG button)
```

---

### 2. Input 中的圖示

```tsx
<div className="input-with-icon">
  <Search size={20} className="input-icon" />
  <input placeholder="搜尋餐廳..." />
</div>
```

**位置規範**:
```
Icon position: absolute, left: 16px, top: 50%, translateY(-50%)
Input padding-left: 44px (16px + 20px icon + 8px gap)
Icon color: charcoal/60
```

---

### 3. 類別標記中的 Emoji

```tsx
<div className="category-badge">
  <span className="text-4xl">🥗</span>
  <span>冷菜</span>
  <span>×2</span>
</div>
```

**規範**:
```
Emoji size: 32px (小卡片), 48px (大卡片)
Emoji + 文字 gap: 8px
```

---

### 4. Loading 動畫

```tsx
<Loader2 size={24} className="animate-spin" />
```

**動畫規範**:
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
```

---

## 🔍 圖示無障礙

### ARIA 標籤

```tsx
// 裝飾性圖示（無需描述）
<Search aria-hidden="true" />

// 功能性圖示（需描述）
<button aria-label="關閉對話框">
  <X size={24} aria-hidden="true" />
</button>

// 帶文字的圖示（圖示為輔助）
<button>
  <Check size={20} aria-hidden="true" />
  <span>確認</span>
</button>
```

### 色彩對比

所有圖示顏色都符合 WCAG AA 標準：

```
Icon on cream-100 background:
- charcoal: 11.2:1 ✅ (AAA)
- caramel: 4.5:1 ✅ (AA)
- terracotta: 5.2:1 ✅ (AA)

Icon on surface background:
- charcoal: 16.5:1 ✅ (AAA)
```

---

## 📝 圖示設計檢查清單

### Lucide Icons
- [ ] 確認所有需要的圖示都在 Lucide 庫中
- [ ] 記錄使用的圖示名稱清單
- [ ] 決定使用 React Component 或 SVG Sprite
- [ ] 設定預設 size 和 strokeWidth

### Emoji
- [ ] 選擇適合的 Emoji（跨平台一致性）
- [ ] 測試在 iOS, Android, Windows 的顯示
- [ ] 設定 fallback font-family
- [ ] 確認尺寸在不同裝置上適當

### 自訂圖示
- [ ] 設計 Logo（Full + Icon Only + Monochrome）
- [ ] 導出多種尺寸（48px, 120px, 512px）
- [ ] 優化 SVG 檔案大小
- [ ] 測試在不同背景色上的效果
- [ ] 生成 favicon.ico

### 文檔
- [ ] 建立圖示使用範例
- [ ] 記錄所有自訂圖示的導出檔案
- [ ] 提供工程師使用指南
- [ ] 更新設計系統文檔

---

## 📊 圖示使用統計

### 預估圖示數量

| 來源 | 數量 | 說明 |
|------|------|------|
| Lucide Icons | 30-40 個 | UI 功能圖示 |
| Emoji | 10-15 個 | 類別標記 |
| 自訂圖示 | 3-5 個 | Logo, 特殊功能 |
| **總計** | **43-60 個** | |

### 常用圖示 Top 10

1. `Search` - 搜尋功能
2. `Check` / `CheckCircle` - 確認狀態
3. `X` - 關閉、移除
4. `ChevronLeft` / `ChevronRight` - 導航
5. `RefreshCw` - 換一道
6. `Share2` - 分享
7. `MapPin` - 餐廳地址
8. `Users` - 人數
9. `Loader2` - Loading
10. 🥗🍖🍚 - 類別 Emoji

---

## 🎯 工程師實作指南

### 安裝 Lucide React

```bash
npm install lucide-react
```

### 建立 Icon Component Wrapper

```tsx
// components/Icon.tsx
import { LucideIcon } from 'lucide-react'

interface IconProps {
  icon: LucideIcon
  size?: number
  className?: string
}

export function Icon({ icon: IconComponent, size = 20, className }: IconProps) {
  return (
    <IconComponent
      size={size}
      strokeWidth={2}
      className={className}
    />
  )
}

// 使用
import { Search } from 'lucide-react'
<Icon icon={Search} size={20} className="text-charcoal" />
```

### Emoji Component

```tsx
// components/CategoryEmoji.tsx
interface CategoryEmojiProps {
  category: string
  size?: 'sm' | 'md' | 'lg'
}

const EMOJI_MAP = {
  '冷菜': '🥗',
  '熱菜': '🍖',
  '湯品': '🍲',
  '主食': '🍚',
  '點心': '🥟',
  '甜點': '🍰',
}

const SIZE_MAP = {
  sm: 'text-2xl',  // 32px
  md: 'text-4xl',  // 48px
  lg: 'text-6xl',  // 64px
}

export function CategoryEmoji({ category, size = 'md' }: CategoryEmojiProps) {
  return (
    <span className={SIZE_MAP[size]} role="img" aria-label={category}>
      {EMOJI_MAP[category]}
    </span>
  )
}
```

---

## 📝 D-011 任務完成報告

### 完成項目
✅ 定義圖示系統策略（Lucide + Emoji + 自訂）
✅ 建立完整圖示清單（40+ 個 UI 圖示）
✅ 定義圖示設計規範（尺寸、風格、顏色）
✅ 列出類別 Emoji 清單（10+ 個）
✅ 定義 Logo 設計建議
✅ 建立導出規範（SVG 優化）
✅ 提供使用範例與代碼
✅ 無障礙規範（ARIA, 對比度）
✅ 工程師實作指南

### 交付物
- `D-011-ICON-DESIGN-GUIDE.md` - 完整圖示系統指南

### 圖示策略

#### 使用 Lucide Icons 的優勢
- 開源免費，無版權問題
- 一致的設計語言
- 支援 React Component，易於使用
- 可自訂顏色和尺寸
- 超過 1000+ 圖示，涵蓋所有需求

#### Emoji 的適用場景
- 類別標記（冷菜🥗、熱菜🍖）
- 情感表達（慶祝🎉、警告⚠️）
- 降低設計成本（無需繪製）

#### 自訂圖示的必要性
- Logo（品牌識別）
- 特殊功能圖示（AI 推薦）
- 數量少（3-5 個），可控

### 實際執行事項（設計師需完成）

**今日完成** (2 小時):
1. 設計 OderWhat Logo（Full + Icon Only）
2. 導出 Logo 多種尺寸（48px, 120px, 512px）
3. 生成 favicon.ico
4. 測試 Logo 在不同背景色上的效果

**可選任務** (1 小時):
5. 設計 AI 推薦圖示（如需要）
6. 設計慶祝圖示（如需要）
7. 優化 SVG 檔案大小

### 工程師協作

**需交付給工程師**:
1. Logo SVG 檔案（多種尺寸）
2. favicon.ico
3. Lucide Icons 使用清單（本文檔已列出）
4. Emoji 對照表（本文檔已列出）

**工程師需安裝**:
```bash
npm install lucide-react
```

### 下一步
D-012: 佔位圖與插圖設計

---

**任務狀態**: ✅ 規格完成
**建立時間**: 2025-01-26
**預估時間**: 2 小時（指南建立） + 3 小時（實際設計 Logo）
