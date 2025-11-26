# Carte AI - 智慧餐廳點餐助手

<div align="center">

![Carte AI](https://img.shields.io/badge/Carte-AI%20Dining%20Agent-D4A574?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-16.0-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?style=for-the-badge&logo=google-cloud)

**30 秒快速決定吃什麼 | AI 分析 Google 評論 | 智慧推薦菜色**

[🌐 線上體驗](https://dining-frontend-u33peegeaa-de.a.run.app) | [📖 文檔](./docs) | [🐛 回報問題](https://github.com/keweikao/oderwhat_carte/issues)

</div>

---

## ✨ 功能特色

- 🎯 **精準避雷**: 分析數千則 Google 評論，過濾地雷菜色
- 💰 **預算控制**: 精準控制每人預算，不超支
- 🍽️ **智慧推薦**: AI 根據用餐人數、預算、偏好推薦菜色
- 🔄 **即時換菜**: 不喜歡？一鍵換成其他推薦
- 📱 **分享菜單**: 生成精美分享卡片，發給朋友
- 🖨️ **列印友善**: 優化的列印樣式，方便點餐

## 🏗️ 技術架構

### 前端
- **框架**: Next.js 16 (React 19)
- **樣式**: Tailwind CSS 4
- **動畫**: Framer Motion
- **UI 組件**: Radix UI
- **認證**: NextAuth.js (Google OAuth)

### 後端
- **框架**: FastAPI (Python)
- **AI**: Google Gemini API
- **搜尋**: Google Places API
- **部署**: Google Cloud Run

## 🚀 快速開始

### 前置需求

- Node.js >= 18.x
- Python >= 3.11
- Google Cloud 帳號

### 本地開發

#### 1. 克隆專案

```bash
git clone https://github.com/keweikao/oderwhat_carte.git
cd oderwhat_carte
```

#### 2. 設置環境變數

```bash
# 從 Google Secret Manager 獲取環境變數
./setup_local_env.sh
```

#### 3. 啟動前端

```bash
cd frontend
npm install
npm run dev
```

前端將在 `http://localhost:3000` 啟動

#### 4. 啟動後端

```bash
cd ..
pip install -r requirements.txt
uvicorn main:app --reload
```

後端將在 `http://localhost:8000` 啟動

## 📁 專案結構

```
oderwhat_carte/
├── frontend/               # Next.js 前端應用
│   ├── src/
│   │   ├── app/           # App Router 頁面
│   │   ├── components/    # React 組件
│   │   ├── lib/           # 工具函數
│   │   └── types/         # TypeScript 類型
│   └── public/            # 靜態資源
├── main.py                # FastAPI 後端主程式
├── schemas/               # Pydantic 資料模型
├── services/              # 業務邏輯服務
├── docs/                  # 文檔
└── specs/                 # 規格文件
```

## 🎨 設計系統

Carte 使用雜誌風格的設計語言：

- **主色調**: Caramel (#D4A574) - 溫暖、親切
- **強調色**: Terracotta (#C85A54) - 熱情、活力
- **輔助色**: Sage (#8B9D83) - 自然、平衡
- **背景色**: Cream (#FFF8F0) - 柔和、舒適

## 📝 開發任務

查看 [DEVELOPMENT_TASKS.md](./frontend/DEVELOPMENT_TASKS.md) 了解開發進度和待辦事項。

## 🚢 部署

### 前端部署到 Cloud Run

```bash
cd frontend
gcloud run deploy dining-frontend \
  --source . \
  --region=asia-east1 \
  --allow-unauthenticated
```

### 後端部署到 Cloud Run

```bash
gcloud run deploy dining-backend \
  --source . \
  --region=asia-east1 \
  --allow-unauthenticated
```

詳細部署指南請參考 [deployment_guide.md](./docs/deployment_guide.md)

## 🤝 貢獻

歡迎提交 Pull Request 或開 Issue！

## 📄 授權

MIT License

## 👨‍💻 作者

**Kewei Kao** - [@keweikao](https://github.com/keweikao)

---

<div align="center">

**由 Carte AI 智慧推薦 • 祝您用餐愉快 🍽️**

Made with ❤️ in Taiwan

</div>
