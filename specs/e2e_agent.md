# E2E Testing Agent 規格（自動對齊版本）

## 目標
- 提供可重現的端到端驗證（前端 UI → API → 後端邏輯），預設使用 mock 來源避免外部依賴。
- 具備「自動對齊」能力：當契約或 UI 變更時，自動更新測試內容/快照（需審核）。
- 成本與穩定性優先，避免依賴真實外部 API。

## 範圍
- 前端：首頁登入流程（mock OAuth）、輸入餐廳/偏好、等待推薦結果呈現（卡片/摘要）。
- 後端 API：`POST /v2/recommendations`、`GET /v2/recommendations/alternatives`，以 mock LLM/資料為主；選配少量真實冒煙。
- 報告產出：JUnit XML + HTML/trace，截圖/DOM snapshot。
- 自動更新：schema/selector/snapshot 可在特定條件下自動重寫，並產生變更摘要。

## 不在範圍
- 真實外部 API 大量流量（僅可選「手動觸發的冒煙」）。
- 覆蓋率量測、壓力測試。

## 資料與 Mock 策略
- 環境變數：`USE_MOCK_EXTERNAL=1` 時，後端改用內建 fixtures（假評論/菜單/LLM 回應）；禁用真 Google/Gemini。
- Fixture 位置：`tests/e2e/__fixtures__/*`（LLM 回應、reviews/menu、API 輸入樣本）。
- 真實冒煙（選配）：`USE_SMOKE_REAL=1` 時啟用，標記為非阻塞。

## 測試場景（MVP）
1. UI-推薦流程（Playwright）：mock 登入 → 填餐廳/偏好 → 送出 → 等待卡片/摘要 → 截圖 + DOM 斷言。
2. API-推薦（Playwright APIClient）：POST `/v2/recommendations`（mock），驗證 schema/必填欄位/items 數量 >0。
3. API-備選菜（alternatives）：GET `/v2/recommendations/alternatives`，驗證 200/404 分支。

## 自動對齊機制
- 契約來源：
  - 後端：啟動前導出 OpenAPI JSON；從 `schemas/recommendation.py` 生成 schema 驗證（如 Zod/JSON schema）。
  - 前端：維護 Locator Map（主要元素 selector）於 `tests/e2e/__fixtures__/locators.json`。
- 變更偵測：
  - 讀取 git diff/最新 OpenAPI/TS props，找出欄位或路由變動。
  - 在 mock 模式下重新發請求取得最新回應，對齊快照。
  - UI 變更時更新 Locator Map 與 DOM snapshot（需審核）。
- 接受更新：
  - `--accept`/`AUTO_ACCEPT=true` 開關允許重寫快照/locators/schema 測試檔，並產生「變更摘要」。
  - 預設需人審（CI 不自動合併除非標記）。

## 報告與產物
- 測試結果：JUnit XML、Playwright HTML report、trace、截圖。
- 變更摘要：列出自動更新的檔案（快照/locators/schema）與差異摘要。

## 實作步驟
1) 後端提供 mock 開關與 fixtures，並暴露 OpenAPI JSON（本地啟動時輸出到 `tests/e2e/__fixtures__/openapi.json`）。  
2) 建立 Playwright 設定 `tests/e2e/playwright.config.ts`（含 trace/screenshot）。  
3) 撰寫場景：
   - `flows.spec.ts`（UI 流程，使用 locators.json）。  
   - `api.spec.ts`（API schema 驗證，使用 openapi.json/生成的 Zod）。  
4) Locator Map 與快照管理：建立 `locators.json`、DOM snapshot，支援 `--accept` 重寫。  
5) CI：新增 job 啟動 mock 後端/前端 → 執行 `npm run test:e2e:mock` → 上傳報告/trace；禁止未標記時自動接受快照。  
6) 文件：在 `docs/` 補操作指引與常見問題（如何切換 mock/real、如何審核 auto-accept）。

## 風險與緩解
- UI 結構頻繁變動 → 使用集中 Locator Map，允許 auto-accept 但需審核摘要。
- 外部 API 變動 → 預設 mock；真實冒煙頻率低且非阻塞。
- Snapshots 漂移 → 審核機制 + 變更摘要；關聯規格/ADR 更新缺失時拒收。 
