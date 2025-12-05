# UI/UX 設計對接 - 快速清單

## 📦 必要元素（給其他模型）

### 1. **專案文件** ⭐⭐⭐⭐⭐
提供這些檔案：
- [ ] `design_brief.md` - 完整設計簡報（這份文件）
- [ ] `color_system_guide.md` - 色彩系統詳細規範
- [ ] `walkthrough.md` - 當前實作記錄
- [ ] 設計系統視覺圖（已生成）

### 2. **當前程式碼** ⭐⭐⭐⭐
關鍵檔案路徑：
```
frontend/
├── tailwind.config.ts          # 色彩、字體配置
├── src/app/[locale]/input/
│   └── page.tsx                 # Input Page V2.4 主檔案
├── src/components/
│   ├── transparency-stream.tsx  # Waiting Screen
│   └── restaurant-search.tsx    # 搜尋組件
└── messages/zh-TW.json          # 翻譯文件
```

### 3. **視覺參考** ⭐⭐⭐⭐
截圖或描述：
- [ ] Input Page 4 個步驟的螢幕截圖
- [ ] Waiting Screen 動畫效果
- [ ] Recommendation Page 佈局
- [ ] 當前色彩使用範例

### 4. **用戶流程圖** ⭐⭐⭐
```
Landing → Input (4 steps) → Waiting → Recommendation → Final Menu
```

### 5. **技術限制** ⭐⭐⭐
- Next.js 14 + Tailwind CSS 3.x
- 必須支援手機版（優先）
- 必須符合 WCAG AA 對比度
- 不使用第三方 UI 框架（如 Material-UI）

---

## 💬 給 AI 模型的 Prompt 模板

### 基礎版本
```
我需要為 Carte AI 餐廳推薦助手設計 UI/UX。

**專案背景**：
- AI 驅動的點餐推薦
- 目標用戶：中高級餐廳用餐者
- 品牌風格：Modern Bistro Editorial

**設計系統**：
- 色彩：Charcoal (#2C2C2C), Caramel (#D4A574), Terracotta (#C77B5F), Cream (#F9F6F0)
- 字體：Cormorant Garamond (標題) + Inter (內文)
- 風格：高級、溫暖、專業但平易近人

**技術限制**：
- Next.js + Tailwind CSS
- 必須響應式（手機優先）
- WCAG AA 無障礙標準

請為 [具體頁面/功能] 設計 UI，需包含：
1. 桌面版與手機版佈局
2. 互動狀態（Hover/Active/Disabled）
3. 使用既有色彩系統
4. Tailwind class 命名建議
```

### 進階版本（含上下文）
```
你是一位專業的 UI/UX 設計師，需要為 Carte AI 設計新功能。

**完整脈絡**：
[附上 design_brief.md 的內容]

**當前狀態**：
- Input Page V2.4: 4 步驟漸進式表單（已完成）
- Waiting Screen V2: Transparency Stream 動畫（已完成）
- Recommendation Page: 需要優化

**設計任務**：
請為 [具體任務，如「推薦頁面的菜色卡片」] 提供：

1. **視覺設計**
   - 佈局結構（wireframe 或描述）
   - 色彩運用（必須使用 Modern Bistro 色系）
   - 字體大小與層次
   - 間距與對齊

2. **互動設計**
   - Hover/Active/Disabled 狀態
   - 過渡動畫（duration, easing）
   - 錯誤處理

3. **響應式**
   - Mobile (320-767px)
   - Tablet (768-1023px)
   - Desktop (1024px+)

4. **程式碼建議**
   - Tailwind class 組合
   - React 組件結構（如適用）
   - 無障礙屬性（ARIA labels）

**參考**：
[附上設計系統視覺圖]
```

---

## 🎯 針對不同任務的提示

### 任務 1: 設計新頁面
```
請為 Carte AI 設計 [頁面名稱]。

**背景**：[brief 摘要]
**色系**：Charcoal, Caramel, Terracotta, Cream
**風格**：Modern Bistro Editorial
**參考**：類似 Input Page V2.4 的漸進式設計

需要：
- 完整佈局（手機+桌面）
- 組件設計
- Tailwind classes
```

### 任務 2: 優化現有組件
```
當前的 [組件名稱] 有以下問題：[列出問題]

請提供優化方案：
- 保持 Modern Bistro 風格
- 提升可讀性/互動性
- 符合無障礙標準
- 提供 Tailwind 實作建議
```

### 任務 3: 設計系統擴展
```
需要為 Carte AI 設計系統新增 [元素類型，如 Toast/Modal/Dropdown]。

**必須符合**：
- Modern Bistro 色系
- 與現有組件一致的風格
- 響應式支援
- 無障礙友善

請提供：
- 各種狀態的設計
- 動畫規範
- Tailwind 實作
```

---

## 📋 檢查清單（提供資料前）

設計對接前，確保準備好：

**必備資料**：
- [x] Design Brief 文件
- [x] 色彩系統指南
- [x] 設計系統視覺圖
- [ ] 當前頁面截圖（如有需要）
- [ ] Figma/Sketch 原始檔（如有）

**清楚說明**：
- [ ] 設計目標（要解決什麼問題）
- [ ] 優先級（哪些功能最重要）
- [ ] 限制條件（技術/時間/資源）
- [ ] 成功指標（如何評估設計好壞）

**避免遺漏**：
- [ ] 品牌語氣（專業/友善/高級）
- [ ] 目標用戶（年齡/使用場景）
- [ ] 競品參考（喜歡/不喜歡的點）
- [ ] 文案範例（實際會顯示的文字）

---

## 🔄 迭代流程建議

1. **Initial Brief** (第一輪)
   - 提供：Design Brief + 色彩系統 + 任務描述
   - 獲得：概念設計（Wireframe/Mockup）

2. **Feedback Round** (第二輪)
   - 提供：詳細反饋 + 調整方向
   - 獲得：精細化設計 + 多種方案

3. **Implementation** (第三輪)
   - 提供：技術限制 + Tailwind 配置
   - 獲得：可直接使用的程式碼

4. **Refinement** (最終輪)
   - 提供：實際使用反饋
   - 獲得：優化調整

---

## 🎨 範例對話（給模型）

### 範例 1: 請求卡片設計
```
USER:
請為 Carte AI 的推薦菜色設計一個卡片組件。

需要顯示：
- 菜名（中文）
- 價格 + 建議人數
- AI 推薦理由（1-2 句）
- 「替換」和「移除」按鈕

使用 Modern Bistro 色系，手機優先設計。

AI RESPONSE:
[應提供詳細的設計規範 + Tailwind classes + 互動狀態]
```

### 範例 2: 請求流程優化
```
USER:
當前 Input Page 的 Step 4 太擁擠，
包含「場合選擇」和「飲食偏好」兩個區塊。

請建議如何優化佈局，讓手機上更易讀。

AI RESPONSE:
[應提供重新佈局建議 + 視覺層次優化 + 間距調整]
```

---

## 📚 附件（應一併提供）

1. **design_brief.md** - 完整設計簡報
2. **color_system_guide.md** - 色彩系統詳細規範
3. **design_system_overview.png** - 視覺化設計系統
4. **當前 page.tsx** - Input Page 程式碼（如需要）
5. **tailwind.config.ts** - Tailwind 配置（如需要）

---

**使用建議**：
將這份清單與 Design Brief 一起提供給 AI 模型，
可大幅提升設計輸出的準確度與可用性！
