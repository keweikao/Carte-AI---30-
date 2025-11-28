# E2E Agent (MVP)

## 如何執行
- 預設為 mock 模式，需自行啟動前端/後端（含 `USE_MOCK_EXTERNAL=1`）。
- 設定環境：
  - `E2E_BASE_URL`：前端位址（預設 `http://localhost:3000`）
  - `E2E_WEB_COMMAND`：可選，讓 Playwright 自啟服務（例如 `npm run dev`）
  - `E2E_RUN_UI=1`：啟用 UI 流程測試
  - `E2E_RUN_API=1`：啟用 API 冒煙測試
  - `E2E_AUTH_HEADER`：後端授權標頭，預設 `Bearer fake-token`
- 指令範例（於專案根目錄）：
```bash
E2E_RUN_UI=1 E2E_RUN_API=1 E2E_BASE_URL=http://localhost:3000 npx playwright test -c tests/e2e/playwright.config.ts
```
  - 若 Playwright 安裝在 frontend，可使用：`cd frontend && E2E_RUN_UI=1 E2E_RUN_API=1 E2E_BASE_URL=http://localhost:3000 npx playwright test -c ../tests/e2e/playwright.config.ts`
  - 先啟後端（mock 模式）：`USE_MOCK_EXTERNAL=1 uvicorn main:app --reload --port 8000`
  - 先啟前端：`cd frontend && npm run dev`
  - 若後端位址不同，設定 `E2E_API_URL`（例如 `http://localhost:8000`）供 API 冒煙使用。

### 匯出 OpenAPI 契約（供 API 測試與自動對齊）
```bash
python tests/e2e/export_openapi.py
```
產物會覆寫 `tests/e2e/__fixtures__/openapi.json`。

## 檔案結構
- `playwright.config.ts`：E2E 設定，支援 trace/screenshot/JUnit。
- `api.spec.ts`：後端 API 冒煙（mock 友善，預設跳過除非設 `E2E_RUN_API=1`）。
- `flows.spec.ts`：UI 推薦流程（預設跳過除非設 `E2E_RUN_UI=1`）。
- `__fixtures__/locators.json`：集中管理 UI 選取器。
- `__fixtures__/openapi.json`：契約占位，可在啟動後端時輸出覆蓋。

## 快照/對齊策略
- 目前為骨架版，未啟用快照；可依 `specs/e2e_agent.md` 擴充 auto-accept 流程與變更摘要。

## GitHub Actions
- Workflow: `.github/workflows/e2e-mock.yml`
- 預設使用 `USE_MOCK_EXTERNAL=1`，啟後端/前端，再跑 Playwright UI+API 煙測，並上傳報告 artifact。
