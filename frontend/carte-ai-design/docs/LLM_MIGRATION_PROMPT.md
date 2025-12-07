# Carte AI 設計遷移指令

> 直接複製以下內容到你的 IDE LLM (Cursor, Copilot, Windsurf)

---

## 快速開始指令

\`\`\`
我要將 Carte AI 的設計系統遷移到這個專案中。

## 設計系統規格

### 色彩 (必須)
- Charcoal: #2C2C2C (主要文字)
- Caramel: #D4A574 (主要 CTA、強調色)
- Terracotta: #C77B5F (次要強調、漸層終點)
- Cream: #F9F6F0 (背景)
- Cream Dark: #EDE8E0 (卡片背景)

### 字體 (必須)
- 標題: Cormorant Garamond (serif)
- 內文: Inter (sans-serif)

### 關鍵 UI 元素

1. Primary Button (漸層圓角按鈕):
className="bg-gradient-to-br from-[#D4A574] to-[#C77B5F] text-white rounded-full px-8 py-3 font-medium hover:brightness-105 hover:-translate-y-0.5 transition-all shadow-lg"

2. Selection Card (選擇卡片):
- Default: border-transparent bg-white shadow-sm
- Hover: border-[#D4A574]/30
- Selected: border-[#D4A574] bg-[#D4A574]/5

3. Page Background:
className="min-h-screen bg-[#F9F6F0]"

### 需要建立的頁面

1. `/` - Landing Page (Hero + Features + CTA)
2. `/input` - 4 步驟輸入表單 (餐廳搜尋 → 用餐模式 → 人數 → 偏好)
3. `/waiting` - AI 處理等待畫面 (3 階段動畫)
4. `/recommendation` - 菜色推薦結果 (卡片列表 + 側邊摘要)
5. `/final-menu` - 最終菜單確認 (分享功能)

### 需要建立的元件 (放在 components/carte/)

- header.tsx - 頂部導覽
- footer.tsx - 頁尾
- progress-bar.tsx - 步驟進度指示器
- dish-card.tsx - 菜色卡片
- menu-summary.tsx - 已選菜色摘要 (sticky sidebar)
- empty-state.tsx - 空狀態
- error-state.tsx - 錯誤狀態

### 響應式規則
- Mobile first
- md: 768px 開始顯示 sidebar
- 手機版使用 bottom fixed bar

請先更新 globals.css 加入設計 tokens，然後建立 Landing Page。
\`\`\`

---

## 分步驟指令

### Step 1: 設定設計系統

\`\`\`
請更新 globals.css 加入 Carte AI 設計 tokens：

色彩變數:
--charcoal: #2C2C2C
--caramel: #D4A574  
--terracotta: #C77B5F
--cream: #F9F6F0
--cream-dark: #EDE8E0

字體:
--font-serif: 'Cormorant Garamond'
--font-sans: 'Inter'

陰影:
--shadow-subtle: 0 2px 8px rgba(44, 44, 44, 0.06)
--shadow-medium: 0 4px 20px rgba(44, 44, 44, 0.1)
--shadow-floating: 0 20px 60px -10px rgba(212, 165, 116, 0.3)

同時更新 layout.tsx 引入 Google Fonts。
\`\`\`

### Step 2: 建立 Landing Page

\`\`\`
建立 Carte AI Landing Page (app/page.tsx)：

結構:
1. Hero Section
   - H1: "讓 AI 為您規劃完美的用餐體驗" (font-serif)
   - Subtitle: 描述 AI 如何幫助選擇菜色
   - CTA: 漸層按鈕 "開始探索" → /input

2. Features Section (3 cards)
   - 智慧分析菜單
   - 個人化推薦
   - 即時更新

3. How It Works (3 steps)
   - 選擇餐廳
   - 輸入偏好
   - 獲得推薦

使用 Carte AI 色彩系統，背景 cream，文字 charcoal。
\`\`\`

### Step 3: 建立 Input Page

\`\`\`
建立 4 步驟輸入頁面 (app/input/page.tsx)：

Step 1 - 餐廳搜尋:
- 搜尋輸入框
- 搜尋結果列表

Step 2 - 用餐模式:
- 3 個選項卡片: 單人用餐 / 朋友聚餐 / 商務餐敘
- 點擊選擇，顯示 checkmark

Step 3 - 用餐人數:
- 數字選擇器 (1-10 人)
- +/- 按鈕

Step 4 - 飲食偏好:
- Pill 多選: 不吃辣 / 素食 / 海鮮過敏 / 無麩質...

頂部顯示進度條 (4 步驟)。
底部顯示 上一步/下一步 按鈕。
最後一步按鈕為 "生成推薦" → /waiting
\`\`\`

### Step 4: 建立 Waiting Screen

\`\`\`
建立 AI 處理等待畫面 (app/waiting/page.tsx)：

3 階段動畫，每階段 2-3 秒：

Phase 1 - 探索:
- Icon: 搜尋動畫
- 文字: "正在探索菜單..."

Phase 2 - 分析:
- Icon: 處理動畫  
- 文字: "分析您的偏好..."

Phase 3 - 生成:
- Icon: 閃爍動畫
- 文字: "生成推薦菜單..."

每個階段下方顯示 "Transparency Stream"：
- 模擬 AI 思考過程的文字串流
- 例如: "發現 12 道符合條件的菜色..."

完成後自動跳轉 /recommendation
\`\`\`

### Step 5: 建立 Recommendation Page

\`\`\`
建立推薦結果頁 (app/recommendation/page.tsx)：

Desktop 佈局 (md 以上):
- 左側 2/3: 菜色卡片列表
- 右側 1/3: Sticky 摘要 sidebar

Mobile 佈局:
- 全寬卡片列表
- Bottom fixed bar (已選 X 道 + 確認按鈕)

Dish Card 元件:
- 菜色圖片 (aspect-video)
- 菜名 (font-serif)
- 價格
- AI 推薦理由 (text-sm)
- Tags (招牌/素食/辣...)
- 選擇 checkbox

Menu Summary Sidebar:
- 已選菜色列表
- 可移除項目
- 預估總價
- "確認菜單" 按鈕 → /final-menu
\`\`\`

### Step 6: 建立 Final Menu Page

\`\`\`
建立最終確認頁 (app/final-menu/page.tsx)：

1. Success Header
   - Checkmark 動畫
   - "您的菜單已準備好！"

2. Menu Card
   - 餐廳名稱 + 地址
   - 已選菜色列表 (圖片 + 名稱 + 價格)
   - 總價

3. Action Buttons
   - 分享到 LINE
   - 複製連結
   - 在 Google Maps 開啟
   - 重新選擇 → /input

4. 底部 CTA
   - "開始新的推薦" → /
\`\`\`

---

## 元件建立指令

### Header 元件

\`\`\`
建立 components/carte/header.tsx：

- Logo: "Carte" (font-serif, text-2xl)
- Desktop: 導覽連結 (首頁 / 關於 / 聯絡)
- Mobile: 漢堡選單
- 背景: transparent 或 cream
- Sticky top
\`\`\`

### Progress Bar 元件

\`\`\`
建立 components/carte/progress-bar.tsx：

Props: { currentStep: number, totalSteps: number }

- 4 個圓形步驟指示器
- 已完成: 填滿 caramel + checkmark
- 當前: 外框 caramel + pulse 動畫
- 未完成: 外框 gray
- 步驟之間用線連接
\`\`\`

### Dish Card 元件

\`\`\`
建立 components/carte/dish-card.tsx：

Props: {
  id: string
  name: string
  price: number
  image: string
  aiReason: string
  tags: string[]
  selected: boolean
  onSelect: (id: string) => void
}

- 卡片容器: rounded-2xl, shadow-subtle, hover:shadow-medium
- 圖片: aspect-video, object-cover
- 選中狀態: border-caramel, 右上角 checkmark
\`\`\`

### Empty State 元件

\`\`\`
建立 components/carte/empty-state.tsx：

Props: {
  type: 'no-restaurant' | 'no-reviews' | 'no-selection' | 'no-results'
  action?: { label: string, onClick: () => void }
}

- 居中佈局
- 插圖/圖標
- 標題 + 描述
- 可選 CTA 按鈕
\`\`\`

---

## 疑難排解

### 如果 LLM 忘記色彩

\`\`\`
提醒：請使用 Carte AI 色彩系統：
- Primary (CTA): bg-gradient-to-br from-[#D4A574] to-[#C77B5F]
- 背景: bg-[#F9F6F0]
- 文字: text-[#2C2C2C]
- 標題字體: font-serif (Cormorant Garamond)
\`\`\`

### 如果樣式不一致

\`\`\`
請確保所有按鈕和卡片遵循以下規範：

Primary Button:
- 漸層: from-caramel to-terracotta
- 圓角: rounded-full
- Hover: brightness-105 + -translate-y-0.5
- Active: scale-[0.98]

Cards:
- 圓角: rounded-2xl
- 陰影: shadow-subtle → hover:shadow-medium
- 選中邊框: border-caramel
\`\`\`

---

*將此文件保存在專案中，方便隨時參考*
