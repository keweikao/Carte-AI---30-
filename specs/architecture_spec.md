# Architecture Specification (架構規格)

## 1. 系統概述
Dining Agent 是一個基於 AI 的餐廳推薦系統，利用 Google Maps 資料、網頁搜尋和 AI 分析來生成個性化的餐廳推薦。

## 2. 核心組件

### 2.1 Backend (Cloud Run)
- **Framework**: FastAPI (Python 3.11)
- **Resources**: 2GB Memory, 300s Timeout
- **Endpoints**:
  - POST `/v2/recommendations/async`: 啟動推薦任務
  - GET `/v2/recommendations/status/{job_id}`: 查詢狀態

### 2.2 Data Pipeline
- **Orchestrator**: 協調資料獲取和處理流程
- **Providers**:
  - `UnifiedMapProvider`: 使用 Apify 抓取 Google Maps 資料 (Images, Reviews)
  - `WebSearchProvider`: 使用 Google Custom Search + Jina Reader 抓取網頁內容
- **Intelligence**:
  - `MenuParser`: 使用 Gemini 2.0 Flash 解析菜單 (Text or Review Extraction)
  - `InsightEngine`: 使用 Gemini 2.5 Flash 融合評論和菜單
  - `MenuIntelligence`: 使用 Gemini 2.0 Flash 生成菜品屬性

### 2.3 Recommendation Engine
- **DiningAgent**: 基於用戶偏好和餐廳 Profile 生成推薦

## 3. 資料流程 (Pipeline Strategies)

### Strategy 1: Web Content Parsing (Highest Quality)
- **Source**: Google Custom Search -> Jina Reader
- **Method**: `MenuParser.parse_from_text()`
- **Model**: Gemini 2.0 Flash

### Strategy 2: Review Extraction (High Quality, Low Cost)
- **Source**: Google Maps Reviews (via Apify)
- **Method**: `MenuParser.extract_from_reviews()`
- **Model**: Gemini 2.0 Flash
- **Fallback**: 如果 Strategy 1 失敗或未配置

### Fallback: Minimal Profile
- **Method**: Create default "招牌菜" item
- **Condition**: 如果所有策略都失敗

## 4. 外部依賴
- **Apify**: Google Maps Crawler
- **Google Custom Search API**: Web Search
- **Gemini API**: AI Analysis
- **Firestore**: Database & Cache

## 5. 優化策略
- **Token Optimization**: 使用檔案參考處理大型資料
- **API Cache**: 快取 API 回應以節省成本
- **Batch Processing**: 批次處理 AI 請求
