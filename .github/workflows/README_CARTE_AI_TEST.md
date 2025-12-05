# GitHub Actions - Carte AI 設計遷移測試

## 📋 概述

此 GitHub Actions workflow 會自動執行 Carte AI 設計遷移完整性測試,確保所有開發內容符合 `LLM_MIGRATION_PROMPT.md` 的規格。

## 🚀 觸發條件

### 自動觸發
- **Push** 到 `main` 或 `develop` 分支
  - 當 `frontend/carte-ai-design/` 目錄有變更時
- **Pull Request** 到 `main` 或 `develop` 分支
  - 當 `frontend/carte-ai-design/` 目錄有變更時

### 手動觸發
- 在 GitHub Actions 頁面點擊 "Run workflow"

## 🔄 工作流程

```
1. 📥 Checkout 程式碼
   ↓
2. 🐍 設定 Python 3.11
   ↓
3. 📋 執行完整性測試
   ↓
4. 📊 顯示測試摘要
   ↓
5. 📄 上傳測試報告 (Artifacts)
   ↓
6. 💬 建立 PR 註解 (僅 PR)
   ↓
7. ✅ 檢查測試結果
```

## 📊 測試內容

### 設計系統 (12 項)
- 色彩變數 (charcoal, caramel, terracotta, cream, cream-dark)
- 字體系統 (Cormorant Garamond, Inter)
- 陰影系統 (subtle, medium, floating)

### 頁面結構 (17 項)
- 5 個必要頁面
- 各頁面關鍵區塊
- 元件整合

### 元件系統 (9 項)
- 7 個核心元件
- Props 定義

### UI 樣式 (11 項)
- 按鈕樣式
- 卡片樣式
- 響應式設計

### 功能實作 (8 項)
- 頁面導航
- React Hooks

**總計**: 57 個測試項目

## 📄 測試報告

### Artifacts
每次執行後會上傳以下檔案 (保留 30 天):
- `test_migration_report.json` - JSON 格式詳細報告
- `MIGRATION_TEST_REPORT.md` - Markdown 完整報告

### PR 註解
Pull Request 會自動收到測試結果註解,包含:
- 完成度百分比
- 通過/失敗/警告統計
- 失敗項目詳情
- 警告項目詳情

範例:
```markdown
## 🎉 Carte AI 設計遷移測試報告

**完成度**: 100.0% (57/57)

| 狀態 | 數量 |
|------|------|
| ✅ 通過 | 57 |
| ❌ 失敗 | 0 |
| ⚠️ 警告 | 1 |

📄 詳細報告請查看 Artifacts 中的 `migration-test-report`
```

## ✅ 成功條件

測試通過條件:
- 所有測試項目通過 (failed = 0)
- 完成度 = 100%

如果有任何失敗項目,workflow 會標記為失敗 ❌

## 🔧 本地測試

在提交前,可以在本地執行測試:

```bash
cd frontend/carte-ai-design

# 快速驗證
./verify_migration.sh

# 或手動執行
python3 test_migration_completeness.py
python3 show_test_summary.py
```

## 📈 查看結果

### GitHub Actions 頁面
1. 前往 Repository → Actions
2. 選擇 "Carte AI Design - Migration Test"
3. 查看最新執行結果

### Pull Request
- PR 頁面會自動顯示測試結果註解
- 點擊 "Details" 查看完整 log

### Artifacts
1. 進入 workflow 執行頁面
2. 下載 "migration-test-report" artifact
3. 解壓縮查看報告

## 🎯 最佳實踐

### 開發流程
1. 在本地開發並測試
2. 執行 `./verify_migration.sh` 確保通過
3. 提交並推送到 feature branch
4. 建立 Pull Request
5. 等待 GitHub Actions 測試結果
6. 根據測試報告修復問題
7. 合併到 main/develop

### 修復失敗
如果測試失敗:
1. 查看 PR 註解或 Actions log
2. 找出失敗的測試項目
3. 對照 `LLM_MIGRATION_PROMPT.md` 規格
4. 修復問題
5. 重新推送 (自動觸發測試)

## 🔍 疑難排解

### 測試一直失敗
- 檢查 `test_migration_completeness.py` 是否存在
- 確認 Python 版本 (需要 3.11+)
- 查看詳細 log 找出錯誤原因

### 找不到測試報告
- 確認測試有執行完成
- 檢查 Artifacts 是否正確上傳
- 查看 workflow log

### PR 沒有收到註解
- 確認是 Pull Request 觸發
- 檢查 GitHub token 權限
- 查看 workflow log 中的錯誤訊息

## 📝 維護

### 更新測試項目
編輯 `frontend/carte-ai-design/test_migration_completeness.py`

### 更新 workflow
編輯 `.github/workflows/carte-ai-design-test.yml`

### 更新觸發條件
修改 workflow 中的 `on` 區塊

## 🔗 相關連結

- 測試腳本: `frontend/carte-ai-design/test_migration_completeness.py`
- 測試說明: `frontend/carte-ai-design/TESTING_README.md`
- 設計規格: `frontend/carte-ai-design/docs/LLM_MIGRATION_PROMPT.md`
- 測試報告: `frontend/carte-ai-design/docs/MIGRATION_TEST_REPORT.md`

## 📊 Badge

在 README 中加入測試狀態 badge:

```markdown
[![Carte AI Design Test](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/carte-ai-design-test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/carte-ai-design-test.yml)
```

---

**最後更新**: 2025-12-05  
**Workflow 版本**: v1.0
