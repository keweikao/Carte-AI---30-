# Optimization Implementation Plan (架構優化實作計畫)

## 1. 已完成變更 (Completed Changes)

### 1.1 架構簡化 (Architecture Simplification)
- [x] **移除 Vision API**: 停止使用圖片 OCR，節省成本與時間。
- [x] **策略調整**: 
  - Strategy 1: Web Search (Serper + Jina)
  - Strategy 2: Review Extraction (Gemini 2.0 Flash)
  - Fallback: Minimal Profile

### 1.2 搜尋引擎優化 (Search Engine Optimization)
- [x] **恢復 Serper API**: 替換 Google Custom Search，以應對高流量成本 ($1/1000 vs $5/1000)。
- [x] **跨國平台支援**:
  - **台灣**: `ichef`, `inline`, `ubereats`, `foodpanda`
  - **日本**: `tabelog`, `gnavi`, `hotpepper`, `retty`
  - **韓國**: `naver`, `catchtable`, `mangoplate`
- [x] **多語言關鍵字**: 加入 `menu`, `メニュー`, `메뉴`。
- [x] **移除地區限制**: 移除 `gl: tw`，支援全球搜尋。

### 1.3 部署配置 (Deployment)
- [x] **Secrets 更新**: 恢復 `SERPER_API_KEY`，移除 `SEARCH_ENGINE_ID`。

## 2. 待驗證項目 (Validation Required)

### 2.1 功能驗證
- [x] **跨國搜尋測試**: 找一家日本餐廳 (如: Afuri Ramen) 和韓國餐廳測試搜尋結果。
- [x] **Serper 403 修復**: 確認 API Key 是否有效，以及 403 錯誤是否解決。
- [ ] **Review Extraction 品質**: 確認 50 則評論是否能穩定提取出高品質菜單。

### 2.2 部署驗證
- [ ] **Production Deployment**: 部署中 (修正 Secret 配置後重試)...
- [ ] **Cold Start 速度**: 確認是否達到預期的 50-60 秒目標。

## 3. 後續優化規劃 (Future Improvements)

### 3.1 穩定性提升 (Stability)
- [x] **Gemini 結構化輸出**: 使用 `response_schema` 強制 Gemini 輸出 Pydantic 物件，解決 JSON 解析錯誤。
- [x] **Firestore 快取**: 實作 Web Search 結果的快取，避免重複搜尋 (節省 Serper 費用)。
- [x] **模型升級**: 全面升級至 `gemini-2.5-flash`，兼顧速度與穩定性。

### 3.2 使用者體驗 (UX)
- [x] **Polling 機制**: 後端已實作非同步 API 和 Job Manager。
- [x] **等待畫面**: 前端已開發 `WaitingScreen` 組件。

### 3.3 成本控制 (Cost)
- [ ] **監控 Serper 用量**: 設定預算警報，避免意外高額費用。
- [ ] **預取熱門餐廳**: 針對熱門榜單進行預熱，減少 Cold Start 發生率。

## 4. 執行時間表 (Timeline)

- **Phase 1 (Now)**: 部署並驗證當前變更。
- **Phase 2 (Next)**: 實作 Gemini 結構化輸出。
- **Phase 3 (Later)**: 實作 Firestore 快取和 Polling 機制。
