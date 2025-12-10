# 🚀 OderWhat 快速開始

## 一鍵啟動開發環境

```bash
./start_dev.sh
```

這個腳本會：
1. 自動檢查並建立 Python 虛擬環境
2. 安裝所有必要的依賴套件
3. 同時啟動前端和後端服務器

## 分別啟動前端或後端

```bash
# 只啟動後端 (FastAPI)
./start_dev.sh backend

# 只啟動前端 (Next.js)
./start_dev.sh frontend

# 同時啟動兩者
./start_dev.sh both
```

## 訪問應用

- **前端**: http://localhost:3000
- **後端**: http://localhost:8000
- **API 文檔**: http://localhost:8000/docs

## 手動啟動

### 後端

```bash
# 啟動虛擬環境
source venv/bin/activate

# 啟動服務器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
npm run dev
```

## 國際化 (i18n) 管理

專案使用改進的 i18n 工作流程，提供自動化工具來管理多語言翻譯：

```bash
# 檢查所有語言檔案的一致性
npm run i18n:check

# 同步所有語言檔案的結構
npm run i18n:sync

# 列出所有待翻譯項目
npm run i18n:todos

# 初始化新語言（例如：日文）
npm run i18n:init ja
```

詳細使用方式請參考 [frontend/I18N_WORKFLOW_GUIDE.md](./frontend/I18N_WORKFLOW_GUIDE.md)

## 完整設定指南

詳細的環境設定說明請參考 [DEV_SETUP.md](./DEV_SETUP.md)

## 需要協助？

- 專案說明: [README.md](./README.md)
- 架構文檔: [ARCHITECTURE.md](./ARCHITECTURE.md)
- 部署指南: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- i18n 工作流程: [frontend/I18N_WORKFLOW_GUIDE.md](./frontend/I18N_WORKFLOW_GUIDE.md)
