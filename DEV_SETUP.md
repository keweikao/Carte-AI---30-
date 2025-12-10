# OderWhat 開發環境設定指南

本指南將幫助你建立 OderWhat 專案的本地開發環境。

## 📋 系統需求

- **Python**: 3.11+ (已安裝: Python 3.11.2)
- **Node.js**: 22.17.0+ (推薦使用 nvm)
- **npm**: 來自 Node.js
- **Google Cloud SDK**: (可選，用於部署和存取 secrets)

## 🚀 快速開始

### 1. 後端設定 (FastAPI + Python)

#### 1.1 建立並啟動 Python 虛擬環境

```bash
# 建立虛擬環境 (如果尚未建立)
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

#### 1.2 安裝 Python 依賴套件

```bash
pip install -r requirements.txt
```

#### 1.3 設定後端環境變數

確認 `.env` 檔案存在於專案根目錄，包含以下必要的 API keys：

```bash
# Google APIs
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
SEARCH_ENGINE_ID=YOUR_GOOGLE_CUSTOM_SEARCH_CX_ID_HERE

# Serper API for Google Search
SERPER_API_KEY=YOUR_SERPER_API_KEY

# Apify API for Scrapers
APIFY_API_TOKEN=YOUR_APIFY_API_TOKEN

# Gemini API Key
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

#### 1.4 啟動後端服務器

```bash
# 確保虛擬環境已啟動
source venv/bin/activate

# 啟動 FastAPI 開發服務器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

後端服務器將運行在 `http://localhost:8000`

查看 API 文檔：`http://localhost:8000/docs`

---

### 2. 前端設定 (Next.js 16 + React 19)

#### 2.1 安裝前端依賴

```bash
cd frontend
npm install
```

#### 2.2 設定前端環境變數

確認 `frontend/.env.local` 檔案存在，包含以下變數：

```bash
# NextAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional configurations
# NEXT_PUBLIC_GOOGLE_PLACES_API_KEY=your_google_places_api_key
# NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

#### 2.3 啟動前端開發服務器

```bash
cd frontend
npm run dev
```

前端應用將運行在 `http://localhost:3000`

---

## 🔧 開發工具與腳本

### 後端常用命令

```bash
# 運行測試
python3 test_cold_start_timing.py

# 查看 Firestore 中快取的餐廳
python3 list_cached_restaurants.py

# 強制重新分析特定餐廳
python3 force_refresh_restaurant.py
```

### 前端常用命令

```bash
cd frontend

# 開發模式
npm run dev

# 生產構建
npm run build

# 運行生產版本
npm start

# Linting
npm run lint

# 運行測試
npm test
npm run test:watch
npm run test:coverage

# E2E 測試 (Playwright)
npm run test:e2e
npm run test:e2e:ui
npm run test:e2e:headed
```

---

## 📁 專案結構

```
OderWhat/
├── agent/              # AI 代理邏輯 (Profiler, Orchestrator)
├── api/                # API 路由定義
├── auth/               # 認證相關
├── frontend/           # Next.js 前端應用
│   ├── src/
│   │   ├── app/       # Next.js App Router
│   │   ├── components/
│   │   └── lib/
│   └── messages/      # i18n 翻譯檔案
├── pipeline/           # 資料處理 pipeline
├── schemas/            # Pydantic schemas
├── services/           # 業務邏輯服務
├── main.py            # FastAPI 應用進入點
├── requirements.txt   # Python 依賴
└── .env               # 後端環境變數
```

---

## 🔐 取得 API Keys

### Google APIs

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用以下 APIs：
   - Gemini API (Google Generative AI)
   - Custom Search API
   - Places API (可選)
4. 在「憑證」頁面建立 API keys

### Serper API

1. 註冊 [Serper.dev](https://serper.dev/)
2. 取得 API key

### Apify API

1. 註冊 [Apify](https://apify.com/)
2. 取得 API token

### NextAuth (Google OAuth)

1. 在 Google Cloud Console 中建立 OAuth 2.0 憑證
2. 設定授權重定向 URI: `http://localhost:3000/api/auth/callback/google`
3. 取得 Client ID 和 Client Secret

---

## 🐛 常見問題排除

### 後端問題

**問題**: `ImportError: No module named 'xxx'`
- **解決**: 確保虛擬環境已啟動並執行 `pip install -r requirements.txt`

**問題**: API keys 錯誤
- **解決**: 檢查 `.env` 檔案中的 API keys 是否正確設定

**問題**: Firestore 連線錯誤
- **解決**: 確保已設定 Google Cloud 專案並有適當的權限

### 前端問題

**問題**: `Module not found` 錯誤
- **解決**: 執行 `npm install` 重新安裝依賴

**問題**: NextAuth 認證失敗
- **解決**: 檢查 `NEXTAUTH_SECRET` 和 Google OAuth 憑證設定

**問題**: API 請求失敗
- **解決**: 確認後端服務器正在運行且 `NEXT_PUBLIC_API_URL` 設定正確

---

## 📚 進階設定

### 使用 Google Cloud Secrets (生產環境)

```bash
# 列出可用的 secrets
gcloud secrets list

# 取得特定 secret
gcloud secrets versions access latest --secret="SECRET_NAME"
```

### Docker 本地開發 (可選)

```bash
# 構建 Docker 映像
docker build -t oderwhat-backend .

# 運行容器
docker run -p 8000:8000 --env-file .env oderwhat-backend
```

---

## 🚢 部署

詳細的部署指南請參考：
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- [cloudbuild-prod-backend.yaml](./cloudbuild-prod-backend.yaml)
- [cloudbuild-prod-frontend.yaml](./cloudbuild-prod-frontend.yaml)

---

## 📊 效能測試

運行效能測試以評估系統回應時間：

```bash
python3 test_cold_start_timing.py
```

這將測試：
- 冷啟動 (Cold Start): ~104 秒
- 暖啟動 (Warm Start): ~52 秒

---

## 📞 需要幫助？

- 查看專案文檔: [README.md](./README.md)
- 架構說明: [ARCHITECTURE.md](./ARCHITECTURE.md)
- 優化計劃: [OPTIMIZATION_PLAN.md](./OPTIMIZATION_PLAN.md)

---

## ✅ 驗證安裝

運行以下命令驗證環境設定：

### 後端驗證

```bash
source venv/bin/activate
python -c "import fastapi; import google.generativeai; print('Backend OK')"
```

### 前端驗證

```bash
cd frontend
npm run build
```

如果以上命令都成功執行，恭喜你完成了開發環境設定！
