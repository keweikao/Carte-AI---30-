# Implementation Plan: 架構文件重構

## 目標
根據最新的系統狀態（移除 Serper/Vision API），重新建立 ASCII 架構圖和規格表，並清理專案結構。

## 步驟

### Phase 1: 清理與準備
- [x] 移除舊的測試檔案 (已完成)
- [x] 建立規格文件 `specs/architecture_spec.md` (已完成)

### Phase 2: 建立架構文件
- [ ] 更新 `ARCHITECTURE.md`
  - [ ] 根據 `specs/architecture_spec.md` 更新內容
  - [ ] 確保 ASCII 圖反映最新的 Pipeline 流程
  - [ ] 更新成本分析（反映 Google Custom Search 的價格）

### Phase 3: 驗證
- [ ] 確認所有舊的測試檔案已移除
- [ ] 確認 `ARCHITECTURE.md` 準確反映代碼現狀

## 參考資料
- `quick_start_for_ai.md`: 開發規範
- `services/pipeline/`: 核心代碼邏輯
