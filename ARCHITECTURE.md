# Restaurant Data Pipeline - 架構規格

## 系統架構圖 (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Frontend (Next.js)                              │
│                        https://www.carte.tw                              │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTPS Request
                                 │ POST /v2/recommendations/async
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                     Cloud Run: dining-backend                            │
│                     (FastAPI, Python 3.11)                               │
│                     Memory: 2GB, Timeout: 300s                           │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              API Layer (main.py)                                 │   │
│  │  - /v2/recommendations/async                                     │   │
│  │  - /v2/recommendations/status/{job_id}                           │   │
│  │  - /v2/recommendations/{id}/finalize                             │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │                                              │
│  ┌────────────────────────▼────────────────────────────────────────┐   │
│  │         Recommendation Engine (api/v1/recommend_v2.py)           │   │
│  │  1. Check Firestore for existing profile                        │   │
│  │  2. If not found → Trigger Cold Start Pipeline                  │   │
│  │  3. Generate recommendations using DiningAgent                   │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │                                              │
│                           │ Cold Start Triggered                         │
│                           │                                              │
│  ┌────────────────────────▼────────────────────────────────────────┐   │
│  │         Restaurant Pipeline (services/pipeline/)                 │   │
│  │                                                                   │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │  Orchestrator (orchestrator.py)                           │  │   │
│  │  │  - Coordinates data flow                                  │  │   │
│  │  │  - Manages strategy execution                             │  │   │
│  │  │  - Assembles final RestaurantProfile                      │  │   │
│  │  └───────┬──────────────────────────────────────────────────┘  │   │
│  │          │                                                       │   │
│  │  ┌───────▼──────────────────────────────────────────────────┐  │   │
│  │  │  STEP 1: Data Acquisition (Parallel)                     │  │   │
│  │  │                                                            │  │   │
│  │  │  ┌─────────────────────┐  ┌──────────────────────────┐  │  │   │
│  │  │  │ UnifiedMapProvider  │  │ WebSearchProvider        │  │  │   │
│  │  │  │ (providers.py)      │  │ (providers.py)           │  │  │   │
│  │  │  │                     │  │                          │  │  │   │
│  │  │  │ → Apify Actor       │  │ → Serper.dev             │  │  │   │
│  │  │  │   (Google Maps)     │  │   (Web Search)           │  │  │   │
│  │  │  │                     │  │ → Jina Reader            │  │  │   │
│  │  │  │ Returns:            │  │                          │  │  │   │
│  │  │  │ - 10 images         │  │ Returns:                 │  │  │   │
│  │  │  │ - 50 reviews        │  │ - Menu URL               │  │  │   │
│  │  │  │ - Place ID          │  │ - Text content           │  │  │   │
│  │  │  │ - Address           │  │                          │  │  │   │
│  │  │  └─────────────────────┘  └──────────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │          │                                                       │   │
│  │  ┌───────▼──────────────────────────────────────────────────┐  │   │
│  │  │  STEP 2: Menu Extraction (Sequential Strategies)         │  │   │
│  │  │                                                            │  │   │
│  │  │  Strategy 1: Text Parsing (Highest Quality)              │  │   │
│  │  │  ┌────────────────────────────────────────────────────┐  │  │   │
│  │  │  │ MenuParser.parse_from_text()                       │  │  │   │
│  │  │  │ (intelligence.py)                                  │  │  │   │
│  │  │  │                                                     │  │  │   │
│  │  │  │ Input: Web content (if available)                  │  │  │   │
│  │  │  │ Model: Gemini 2.0 Flash                            │  │  │   │
│  │  │  │ Output: List[ParsedMenuItem]                       │  │  │   │
│  │  │  │ Trust Level: HIGH                                  │  │  │   │
│  │  │  └────────────────────────────────────────────────────┘  │  │   │
│  │  │          │ If failed or no web content                   │  │   │
│  │  │  ┌───────▼──────────────────────────────────────────┐  │  │   │
│  │  │  │ Strategy 2: Review Extraction (Cost-Effective)   │  │  │   │
│  │  │  │ MenuParser.extract_from_reviews()                │  │  │   │
│  │  │  │ (intelligence.py)                                │  │  │   │
│  │  │  │                                                   │  │  │   │
│  │  │  │ Input: 50 customer reviews                       │  │  │   │
│  │  │  │ Model: Gemini 2.0 Flash                          │  │  │   │
│  │  │  │ Output: 5-15 dishes with descriptions            │  │  │   │
│  │  │  │ Trust Level: MEDIUM                              │  │  │   │
│  │  │  └──────────────────────────────────────────────────┘  │  │   │
│  │  │          │ If failed                                     │  │   │
│  │  │  ┌───────▼──────────────────────────────────────────┐  │  │   │
│  │  │  │ Fallback: Minimal Profile                        │  │  │   │
│  │  │  │ - Single "招牌菜" item                            │  │  │   │
│  │  │  │ - Trust Level: LOW                               │  │  │   │
│  │  │  └──────────────────────────────────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │          │                                                       │   │
│  │  ┌───────▼──────────────────────────────────────────────────┐  │   │
│  │  │  STEP 3: Review Fusion                                   │  │   │
│  │  │  ┌────────────────────────────────────────────────────┐  │  │   │
│  │  │  │ InsightEngine.fuse_reviews()                       │  │  │   │
│  │  │  │ (intelligence.py)                                  │  │  │   │
│  │  │  │                                                     │  │  │   │
│  │  │  │ - Match reviews to menu items                      │  │  │   │
│  │  │  │ - Generate sentiment analysis                      │  │  │   │
│  │  │  │ - Create review summary                            │  │  │   │
│  │  │  │ Model: Gemini 2.5 Flash                            │  │  │   │
│  │  │  └────────────────────────────────────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │          │                                                       │   │
│  │  ┌───────▼──────────────────────────────────────────────────┐  │   │
│  │  │  STEP 3.5: Dish Attributes Generation                   │  │   │
│  │  │  ┌────────────────────────────────────────────────────┐  │  │   │
│  │  │  │ MenuIntelligence.analyze_dish_batch()              │  │  │   │
│  │  │  │ (intelligence.py)                                  │  │  │   │
│  │  │  │                                                     │  │  │   │
│  │  │  │ - Generate DishAttributes for each item            │  │  │   │
│  │  │  │ - Extract flavors, textures, cooking methods       │  │  │   │
│  │  │  │ - Identify signature dishes                        │  │  │   │
│  │  │  │ Model: Gemini 2.0 Flash                            │  │  │   │
│  │  │  └────────────────────────────────────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │          │                                                       │   │
│  │  ┌───────▼──────────────────────────────────────────────────┐  │   │
│  │  │  STEP 4: Profile Assembly                                │  │   │
│  │  │  - Create RestaurantProfile object                       │  │   │
│  │  │  - Save to Firestore                                     │  │   │
│  │  │  - Return to Recommendation Engine                       │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                           │                                              │
│  ┌────────────────────────▼────────────────────────────────────────┐   │
│  │         DiningAgent (agent/dining_agent.py)                      │   │
│  │  - Use RestaurantProfile + User Preferences                      │   │
│  │  - Generate personalized recommendations                         │   │
│  │  - Model: Gemini 2.5 Flash                                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
         ┌──────────▼──────────┐       ┌───────────▼──────────┐
         │   Firestore         │       │   External APIs      │
         │   (Database)        │       │                      │
         │                     │       │  - Apify             │
         │  - Restaurant       │       │  - Google Custom     │
         │    Profiles         │       │    Search            │
         │  - Recommendations  │       │  - Jina Reader       │
         │  - User Data        │       │  - Gemini API        │
         └─────────────────────┘       └──────────────────────┘
```

## 核心組件規格

### 1. API Layer

| 端點 | 方法 | 功能 | 輸入 | 輸出 |
|------|------|------|------|------|
| `/v2/recommendations/async` | POST | 啟動推薦任務 | UserInputV2 | JobResponse |
| `/v2/recommendations/status/{job_id}` | GET | 查詢任務狀態 | job_id | StatusResponse |
| `/v2/recommendations/{id}/finalize` | POST | 完成訂單 | FinalizeRequest | Success |

### 2. Data Acquisition Layer

#### UnifiedMapProvider
- **API**: Apify Actor (compass/crawler-google-places)
- **記憶體**: 512 MB
- **輸入**: restaurant_name, place_id (optional)
- **輸出**: MapData
  - images: List[str] (max 10)
  - reviews: List[RawReview] (max 50)
  - place_id: str
  - name: str
  - address: str
- **執行時間**: ~30 秒

#### WebSearchProvider
- **API**: Google Custom Search API (可選)
- **Fallback**: Jina Reader
- **輸入**: restaurant_name
- **輸出**: WebContent (optional)
  - source_url: str
  - text_content: str
- **執行時間**: ~5 秒
- **成本**: 免費 100 次/天，$5/1000 次

### 3. Intelligence Layer

#### MenuParser

| 方法 | 輸入 | 輸出 | Model | Trust Level |
|------|------|------|-------|-------------|
| `parse_from_text()` | Web content | List[ParsedMenuItem] | Gemini 2.0 Flash | HIGH |
| `extract_from_reviews()` | 50 reviews | List[ParsedMenuItem] | Gemini 2.0 Flash | MEDIUM |

**ParsedMenuItem Schema**:
```python
{
    "name": str,
    "price": Optional[int],
    "category": str,
    "description": Optional[str]
}
```

#### InsightEngine
- **方法**: `fuse_reviews()`
- **功能**: 將評論與菜品匹配，生成情感分析
- **Model**: Gemini 2.5 Flash
- **輸出**: Enhanced menu items + review summary

#### MenuIntelligence
- **方法**: `analyze_dish_batch()`
- **功能**: 生成 DishAttributes
- **Model**: Gemini 2.0 Flash
- **輸出**: MenuItem with DishAttributes

**DishAttributes Schema**:
```python
{
    "dish_type": str,  # "main", "side", "soup", etc.
    "main_protein": str,
    "flavors": List[str],
    "textures": List[str],
    "temperature": "hot" | "cold" | "room",
    "cooking_method": str,
    "suitable_occasions": List[str],
    "is_signature": bool,
    "sentiment_score": float
}
```

### 4. Recommendation Engine

#### DiningAgent
- **輸入**: RestaurantProfile + UserPreferences
- **Model**: Gemini 2.5 Flash
- **輸出**: Personalized recommendations
- **執行時間**: ~10 秒

## 資料流程

### Cold Start Flow (新餐廳)
```
1. User Request → API
2. API → Check Firestore (Not Found)
3. API → Trigger Pipeline
4. Pipeline → Fetch Data (Apify + Google Search)
5. Pipeline → Extract Menu (Strategy 1 or 2)
6. Pipeline → Fuse Reviews
7. Pipeline → Generate Attributes
8. Pipeline → Save to Firestore
9. API → Generate Recommendations
10. API → Return to User
```
**總時間**: ~60-90 秒

### Warm Start Flow (已有 Profile)
```
1. User Request → API
2. API → Check Firestore (Found)
3. API → Generate Recommendations
4. API → Return to User
```
**總時間**: ~10-15 秒

## 環境變數

| 變數名 | 用途 | 必要性 | 來源 |
|--------|------|--------|------|
| `APIFY_API_TOKEN` | Google Maps 資料抓取 | ✅ 必要 | Secret Manager |
| `GEMINI_API_KEY` | AI 分析和推薦 | ✅ 必要 | Secret Manager |
| `GOOGLE_API_KEY` | Google APIs | ✅ 必要 | Secret Manager |
| `SEARCH_ENGINE_ID` | Google Custom Search | ⚠️ 可選 | Secret Manager |
| `JINA_API_KEY` | 網頁內容抓取 | ⚠️ 可選 | Secret Manager |

## 成本分析 (每 1000 次請求)

| 項目 | 單價 | 用量 | 成本 |
|------|------|------|------|
| **Apify** | $0.25/GB-hour | 512MB × 1min × 1000 | $2.00 |
| **Google Custom Search** | $5/1000 | 500 次 (50% 使用) | $2.50 |
| **Gemini API** | 免費 | 3-4 requests × 1000 | $0.00 |
| **Cloud Run** | $0.00002400/vCPU-s | 2 vCPU × 60s × 1000 | $2.88 |
| **Firestore** | $0.06/100K | 1 read × 1000 | $0.0006 |
| **總計** | | | **~$7.38** |

**有快取 (50% 命中率)**:
- Cold Start (500 次): $3.69
- Cache Hit (500 次): $0.03
- **總計**: **~$3.72**

## 性能指標

| 指標 | Cold Start | Warm Start |
|------|------------|------------|
| **平均執行時間** | 60-90 秒 | 10-15 秒 |
| **P95 執行時間** | 120 秒 | 20 秒 |
| **成功率** | >95% | >99% |
| **菜品數量** | 5-15 個 | N/A |
| **Trust Level** | MEDIUM | N/A |

## 並發限制

| 資源 | 配額 | 單次消耗 | 最大並發 |
|------|------|----------|----------|
| Apify Memory | 32 GB | 512 MB | ~60 |
| Gemini API | 15 RPM | 3 requests | ~5/min |
| Cloud Run | 100 instances | 1 | 100 |

**建議最大並發**: 5-7 個用戶/分鐘

## 優化建議

### 已實作 ✅
- [x] 移除 Serper API（成本優化）
- [x] 移除 Vision API（速度優化）
- [x] Review Extraction 優先（品質優化）
- [x] 批次處理（quota 優化）
- [x] 降低 Apify 記憶體（成本優化）

### 待實作 🔄
- [ ] Firestore 快取檢查
- [ ] 任務隊列（Cloud Tasks）
- [ ] 限流機制
- [ ] 預先抓取熱門餐廳
- [ ] Tabelog 整合（日本餐廳）

---

**文件版本**: 1.0
**最後更新**: 2025-12-04
**維護者**: AI Team
