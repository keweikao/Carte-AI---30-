# E2E Testing Agent 實作計畫

## 目標
- 依據 `specs/e2e_agent.md`，建立可重現的端到端測試（UI + API），預設使用 mock 來源。
- 提供自動對齊能力：契約/selector 變更時可在受控條件下自動更新測試/快照並產出摘要。

## 範圍
- 前端流程：首頁（mock 登入）→ 輸入餐廳/偏好 → 送出 → 顯示推薦卡與摘要。
- 後端 API：`POST /v2/recommendations`、`GET /v2/recommendations/alternatives`（mock 模式）。
- 報告：JUnit XML + Playwright HTML/trace/截圖；變更摘要。

## 拆解任務
1. **Mock 開關與 fixtures**
   - 環境變數 `USE_MOCK_EXTERNAL=1` 支援，提供固定 LLM/評論/菜單回應。
   - 匯出 OpenAPI JSON 至 `tests/e2e/__fixtures__/openapi.json`（啟動本地後端時）。
2. **Playwright 設定**
   - 新增 `tests/e2e/playwright.config.ts`（trace、screenshot、reporter）。
   - npm script：`test:e2e:mock`（啟動 mock 前後端後執行）。
3. **Locator Map 與快照管理**
   - 建立 `tests/e2e/__fixtures__/locators.json`（主要元素 selector）。
   - 支援 `--accept` 重寫快照/locator 並產出變更摘要。
4. **測試腳本**
   - `flows.spec.ts`：UI 流程（mock 登入、填表、等待卡片、斷言與截圖）。
   - `api.spec.ts`：API schema 驗證（使用 openapi.json/Zod），涵蓋 recommendations/alternatives。
5. **CI 整合**
   - 新增 workflow：啟動 mock 後端/前端 → 跑 `test:e2e:mock` → 上傳報告/trace；預設不自動 accept 快照。
6. **文件**
   - 在 `docs/` 補操作指引（切換 mock/real、--accept 使用、故障排除）。

## 風險與應對
- UI 變動頻繁：集中管理 locators，快照更新需審核；允許受控 auto-accept。
- 外部依賴變動：預設 mock，真實冒煙手動或低頻執行。
- 非決定性：固定 fixtures、mock LLM，避免隨機性。
