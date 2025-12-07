# 規格文件：UI 改進、強制登入與資料整合

**建立日期**: 2025-11-21
**狀態**: Draft
**類型**: Feature Enhancement

---

## 1. 概述 (Overview)

本規格定義三項關鍵改進需求：
1. 移除首頁，直接進入點餐流程
2. 強制 Google 登入才能輸入餐廳名稱
3. 整合真實餐廳資料，移除測試資料

---

## 2. 問題陳述 (Problem Statement)

### 當前狀況
根據截圖分析：
- **截圖 1** (首頁)：顯示 "Don't think. Just eat." 的 Landing Page，有 "Start Dining" 按鈕
- **截圖 2** (推薦頁面)：顯示測試資料（招牌A餐、配菜B、湯品C 等模擬項目）

### 存在問題
1. **多餘的首頁**：使用者需要額外點擊才能開始使用，增加摩擦
2. **缺乏驗證**：未登入即可輸入餐廳，造成潛在的濫用風險
3. **測試資料混淆**：顯示模擬資料（括號標註「模擬」），影響使用者信任度

---

## 3. 使用者故事 (User Stories)

### US-1: 直接進入點餐流程
**作為** 使用者
**我想要** 開啟網站時直接看到餐廳輸入介面
**以便** 快速開始點餐，不需要額外點擊

**驗收標準**:
- [ ] 訪問根路徑 (`/`) 時，直接顯示餐廳名稱輸入介面
- [ ] 移除 "Don't think. Just eat." 的 Landing Page
- [ ] 如果未登入，顯示登入提示

---

### US-2: 強制 Google 登入
**作為** 系統管理者
**我想要** 使用者必須登入 Google 才能輸入餐廳名稱
**以便** 追蹤使用者行為、防止濫用、並提供個人化體驗

**驗收標準**:
- [ ] 未登入時，餐廳名稱輸入框應為停用狀態（disabled）或隱藏
- [ ] 顯示明確的 "使用 Google 登入" 按鈕
- [ ] 登入成功後，自動啟用餐廳名稱輸入功能
- [ ] 登入狀態應在頁面重新整理後保持

**非功能需求**:
- 登入流程應在 2 秒內完成（Google OAuth 回應時間）
- 登入失敗時，顯示清楚的錯誤訊息

---

### US-3: 整合真實資料
**作為** 使用者
**我想要** 看到真實的餐廳菜單和價格
**以便** 做出實際的點餐決策

**驗收標準**:
- [ ] 移除所有包含「模擬」、「測試」字樣的資料
- [ ] 顯示從後端 API 取得的真實餐廳資料
- [ ] 若餐廳無資料，顯示友善的「查無此餐廳」訊息
- [ ] 價格、評分、菜名應為實際資料

**資料來源**:
- 後端 API Endpoint: `/api/restaurant/{name}`
- 資料格式應符合現有的 Restaurant Schema

---

## 4. 功能邊界 (Scope)

### 包含 (In Scope)
- 路由重新配置（根路徑行為變更）
- 驗證流程整合（NextAuth Google Provider）
- 前端 UI 調整（條件渲染登入狀態）
- 真實資料 API 整合

### 不包含 (Out of Scope)
- 其他登入方式（Facebook、Apple 等）
- 使用者個人資料編輯功能
- 歷史訂單記錄
- 餐廳資料後端爬蟲開發（假設已有資料源）

---

## 5. 限制與假設 (Constraints & Assumptions)

### 技術限制
- 使用 NextAuth.js 進行驗證
- Google OAuth 需要有效的 Client ID/Secret
- 前端使用 Next.js 14+ App Router

### 假設
1. 後端 API 已經準備好提供真實餐廳資料
2. Google OAuth 憑證已配置在 `.env` 檔案中
3. 使用者已同意使用 Google 帳號登入

---

## 6. 安全考量 (Security Considerations)

- Google OAuth Token 應妥善儲存（httpOnly cookies）
- 不應在前端暴露 API Keys
- 驗證中介軟體應檢查每個需要驗證的請求
- 防止 CSRF 攻擊（NextAuth 內建保護）

---

## 7. 效能需求 (Performance Requirements)

- 首次載入時間：< 2 秒（含驗證檢查）
- API 回應時間：< 500ms（餐廳資料查詢）
- 登入流程：< 3 秒（含 Google OAuth 往返）

---

## 8. 成功指標 (Success Metrics)

- 使用者完成登入的比例 > 80%
- 餐廳資料載入錯誤率 < 5%
- 頁面跳出率降低（移除首頁後）

---

## 9. 參考資料 (References)

- [NextAuth.js Documentation](https://next-auth.js.org/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- 現有專案結構：`frontend/src/app/`

---

**下一步**: 建立 `implementation_plan.md` 定義技術實作細節
