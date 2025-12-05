# Carte AI 前端實作計畫

**基於**: CARTE_AI_COMPLETE_SPEC.md  
**開始日期**: 2025-12-05  
**預計完成**: 3 週

---

## 📋 實作策略

### 原則
1. ✅ **保留現有功能**: i18n, NextAuth, API 整合
2. ✅ **漸進式遷移**: 一次一個頁面,確保穩定
3. ✅ **測試優先**: 每個階段完成後測試
4. ✅ **文件同步**: 更新相關文件

### 不遷移的內容
- ❌ `/[locale]/menu` - 主專案獨有功能
- ❌ `/[locale]/not-found` - 保持現有實作
- ❌ 測試/展示頁面

---

## 🎯 第一週: 設計系統基礎

### Day 1: 設計 Tokens (2-3 小時)

#### 任務
1. 更新 `src/app/globals.css`
2. 整合 Carte AI 色彩系統
3. 加入字體、陰影、圓角變數

#### 檔案
- `src/app/globals.css`

#### 檢查清單
- [ ] 色彩變數 (charcoal, caramel, terracotta, cream)
- [ ] 字體變數 (serif, sans)
- [ ] 陰影系統 (subtle, medium, prominent, floating)
- [ ] 圓角系統 (sm, md, lg, xl, 2xl, full)
- [ ] 保留現有功能色 (success, warning, destructive)
- [ ] Dark mode 相容性

---

### Day 2: Google Fonts 設定 (1-2 小時)

#### 任務
1. 更新 `src/app/[locale]/layout.tsx`
2. 引入 Cormorant Garamond 和 Inter
3. 設定字體變數

#### 檔案
- `src/app/[locale]/layout.tsx`

#### 檢查清單
- [ ] 引入 Google Fonts
- [ ] 設定 CSS 變數
- [ ] 保留 i18n 功能
- [ ] 測試字體載入

---

### Day 3-4: 基礎元件 (8-10 小時)

#### 任務
建立 `src/components/carte/` 目錄並實作基礎元件

#### 元件清單

**優先 (Day 3)**:
1. `header.tsx` - 頂部導覽
   - Logo
   - Navigation links
   - CTA button
   - Responsive menu

2. `footer.tsx` - 頁尾
   - Copyright
   - Links
   - Social media

3. `progress-bar.tsx` - 步驟進度
   - Stepped variant
   - Continuous variant
   - Labels

**次要 (Day 4)**:
4. `empty-state.tsx` - 空狀態
   - Icon
   - Title
   - Description
   - Action button

5. `error-state.tsx` - 錯誤狀態
   - Error types (network, server, timeout, etc.)
   - Retry button
   - Back button

#### 檢查清單
- [ ] 所有元件使用 Carte AI 設計系統
- [ ] TypeScript 型別定義完整
- [ ] 支援 i18n (使用 next-intl)
- [ ] Responsive 設計
- [ ] 建立 Storybook 或測試頁面

---

### Day 5: 測試與文件 (3-4 小時)

#### 任務
1. 建立元件測試頁面
2. 驗證設計一致性
3. 更新文件

#### 檢查清單
- [ ] 所有元件正常運作
- [ ] 色彩使用正確
- [ ] 字體顯示正確
- [ ] Responsive 正常
- [ ] 更新 DESIGN_MIGRATION_PLAN.md

---

## 🎨 第二週: 核心頁面

### Day 1-2: Landing Page (10-12 小時)

#### 任務
重新設計 `src/app/[locale]/page.tsx`

#### 結構
```
[Header]
[Hero Section]
  - Tagline
  - Headline (Cormorant Garamond)
  - Subheadline
  - Primary CTA
  - Secondary link

[Features Section]
  - 3 feature cards (grid)

[How It Works Section]
  - 4 step cards (numbered)

[Testimonials Section]
  - User testimonials

[Final CTA Section]
[Footer]
```

#### 文案
參考 SPEC 的 3.1 Landing Page

#### 功能
- [ ] Header scroll effect (backdrop-blur)
- [ ] Smooth scroll navigation
- [ ] CTA 檢查 onboarding 狀態
- [ ] 保留 NextAuth 登入
- [ ] Responsive layout

---

### Day 3: Onboarding Page (4-5 小時)

#### 任務
建立 `src/app/[locale]/onboarding/page.tsx`

#### 結構
```
[Progress Dots] - 3 steps
[Step Content]
  - Icon
  - Title
  - Description
[Navigation]
  - Skip
  - Next/Start
```

#### 功能
- [ ] 3 步驟內容
- [ ] 進度指示
- [ ] localStorage 儲存狀態
- [ ] 完成後導向 /input

---

### Day 4-5: Input Page 重構 (12-14 小時)

#### 任務
重構 `src/app/[locale]/input/page.tsx`

#### 4 個步驟

**Step 1: 餐廳搜尋**
- [ ] 整合現有 RestaurantSearch 元件
- [ ] 最近搜尋 (localStorage)
- [ ] 熱門餐廳
- [ ] Google Maps URL 解析

**Step 2: 用餐模式**
- [ ] 6 個選項 (casual, date, business, family, celebration, solo)
- [ ] SelectionCard 元件
- [ ] 單選邏輯

**Step 3: 用餐人數**
- [ ] 數字選擇器 (+/-)
- [ ] 快速選擇 (1, 2, 4, 6, 8+)
- [ ] 自訂輸入

**Step 4: 偏好設定**
- [ ] 飲食限制 (多選)
- [ ] 過敏原 (多選)
- [ ] 口味偏好 (多選)
- [ ] 額外備註 (textarea)
- [ ] 互斥選項處理

#### 共用功能
- [ ] Progress bar (4 steps)
- [ ] Back/Next navigation
- [ ] 表單驗證
- [ ] sessionStorage 儲存
- [ ] 保留 prefetch API

---

## ⏳ 第三週: 推薦流程

### Day 1: Waiting Page (6-8 小時)

#### 任務
建立 `src/app/[locale]/waiting/page.tsx`

#### 功能
- [ ] 3 階段動畫 (exploring, analyzing, curating)
- [ ] Transparency Stream (SSE)
- [ ] 打字機效果
- [ ] 進度指示
- [ ] 超時處理
- [ ] 錯誤處理

#### 元件
建立 `src/components/carte/transparency-stream.tsx`

---

### Day 2-3: Recommendation Page (12-14 小時)

#### 任務
重構 `src/app/[locale]/recommendation/page.tsx`

#### 元件
1. `dish-card.tsx` - 菜色卡片
   - [ ] Image
   - [ ] Badges (AI pick, popular, signature)
   - [ ] Name, price, description
   - [ ] Expandable (AI reason, reviews)
   - [ ] Swap/Remove actions

2. `menu-summary.tsx` - 側邊摘要
   - [ ] Selected dishes list
   - [ ] Total calculation
   - [ ] Action buttons
   - [ ] Sticky on desktop
   - [ ] Bottom bar on mobile

#### 佈局
- [ ] Desktop: 2 columns (60/40)
- [ ] Mobile: Stack + floating action bar
- [ ] Restaurant info card
- [ ] Summary pills

#### 功能
- [ ] 移除菜色
- [ ] 更換菜色 (modal)
- [ ] 確認菜單
- [ ] 保留 API 整合

---

### Day 4: Final Menu Page (6-8 小時)

#### 任務
建立 `src/app/[locale]/final-menu/page.tsx`

#### 功能
- [ ] Success animation
- [ ] Menu card display
- [ ] 導航到餐廳 (Google Maps)
- [ ] 分享功能 (copy, LINE, Messenger)
- [ ] 儲存菜單 (localStorage)
- [ ] Quick actions

---

### Day 5: 整合測試與優化 (8 小時)

#### 任務
1. 端到端測試
2. 效能優化
3. Bug 修復
4. 文件更新

#### 測試清單
- [ ] 完整流程 (Landing → Final Menu)
- [ ] i18n 切換
- [ ] Responsive (Mobile/Desktop)
- [ ] API 整合
- [ ] 錯誤處理
- [ ] Loading states
- [ ] 動畫流暢度

#### 效能優化
- [ ] Image optimization
- [ ] Code splitting
- [ ] Lazy loading
- [ ] Bundle size check

---

## 📦 元件開發順序

### 第一批 (Week 1)
1. ✅ Design Tokens
2. ✅ Google Fonts
3. ✅ Header
4. ✅ Footer
5. ✅ Progress Bar
6. ✅ Empty State
7. ✅ Error State

### 第二批 (Week 2)
8. ✅ Selection Card
9. ✅ Onboarding
10. ✅ Input Steps

### 第三批 (Week 3)
11. ✅ Transparency Stream
12. ✅ Dish Card
13. ✅ Menu Summary
14. ✅ Share Modal

---

## 🎨 設計一致性檢查

### 每個頁面完成後檢查
- [ ] 使用 Cormorant Garamond 標題
- [ ] 使用 Inter 內文
- [ ] 主要 CTA 使用漸層 (caramel → terracotta)
- [ ] 背景使用 cream (#F9F6F0)
- [ ] 文字使用 charcoal (#2C2C2C)
- [ ] 卡片使用 white 或 cream-dark
- [ ] 陰影使用統一系統
- [ ] 圓角使用統一系統

---

## 🔧 技術要求

### 必須保留
- ✅ i18n (next-intl)
- ✅ NextAuth
- ✅ API 整合
- ✅ RestaurantSearch 元件
- ✅ Prefetch 機制

### 新增技術
- Framer Motion (動畫)
- Zustand 或 Context (狀態管理)
- SSE (Server-Sent Events)

---

## 📝 文件更新

### 需要更新的文件
1. `DESIGN_MIGRATION_PLAN.md` - 進度追蹤
2. `README.md` - 專案說明
3. `CHANGELOG.md` - 變更記錄
4. Component README - 元件使用說明

---

## ✅ Definition of Done

### 每個頁面
- [ ] 功能完整
- [ ] 設計一致
- [ ] Responsive
- [ ] i18n 支援
- [ ] 錯誤處理
- [ ] Loading states
- [ ] 測試通過
- [ ] 文件更新

### 整體專案
- [ ] 所有頁面完成
- [ ] 端到端測試通過
- [ ] 效能符合標準 (< 2s 載入)
- [ ] 無 console errors
- [ ] 無 TypeScript errors
- [ ] 無 ESLint errors
- [ ] 文件完整

---

## 🚀 開始執行

### 立即開始
1. 確認規格書理解正確
2. 設定開發環境
3. 建立 feature branch
4. 開始 Day 1 任務

### 需要確認
- [ ] 是否需要所有新頁面 (onboarding, waiting, final-menu)?
- [ ] 時程是否可接受 (3 週)?
- [ ] 是否需要先看設計稿?

---

**準備好開始了嗎?** 🎨✨

請確認:
1. 規格書內容是否清楚?
2. 實作計畫是否合理?
3. 是否有其他需求?

確認後我們立即開始 Day 1: 設計 Tokens!
