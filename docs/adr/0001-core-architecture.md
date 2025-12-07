# ADR 0001: 核心架構與開發原則

- 狀態：已採納
- 日期：2025-11-28

## 背景
- 專案採用「先規格、再計畫、再任務」的 Spec-Driven Development 流程，並強制使用繁體中文。
- 為降低成本，已內建兩層優化：`api_cache_minimal.py`（API 快取）與 `token_optimizer_minimal.py`（Token 優化）。
- 主要資料流：使用 Google Places API 抓評論（最多 5 則）與 Google Custom Search 摘要作為菜單線索，Gemini 生成推薦，Firestore 作為快取層。

## 決策
- **可解釋性優先**：所有核心邏輯需有規格文件與計畫文件，並維持小檔案、明確型別（Pydantic/TS）。
- **上下文邊界**：使用簡潔的目錄/檔案樹與 ADR 記錄，幫助 LLM 與人類快速定位模組。
- **成本優化**：預設啟用 API 快取與 Token 優化，避免重複呼叫與過長上下文。
- **資料來源透明**：沿用 Google Places 5 則評論與 Custom Search snippet，避免虛構數量；擴充前需新增規格。

## 影響
- 新功能須先補 `specs/`、`implementation_plan.md`、`task.md`，再實作。
- 變更資料來源或推薦邏輯時，需新增 ADR 記錄決策理由與替代方案。
- 任何自動化審查或摘要工具（例如 Repomix/PR Agent）需遵守資料邊界與隱私，不得外送敏感資訊。
