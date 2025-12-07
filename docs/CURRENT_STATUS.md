# OderWhat v2.0 - 當前開發狀態

**最後更新**: 2025-12-03 10:50 UTC+8
**當前 Revision**: `oderwhat-staging-00031-9bk`

---

## 🎯 專案目標

建立混合式智慧菜單管線：
- **離線預處理**: Apify + Gemini 進行菜色屬性標註
- **即時推薦**: 兩階段過濾（Hard Filter + LLM Ranking）

---

## ✅ 已完成功能

### 1. 資料獲取層 (100%)

**檔案**: `services/pipeline/providers.py`

- ✅ `UnifiedMapProvider`: 單次 Apify 呼叫獲取所有資料
  - 圖片（前 10 張）
  - 評論（前 20 則）
  - 地址、電話、評分
  - 使用 `searchStringsArray` (正確方式)

- ✅ `WebSearchProvider`: Serper + Jina 抓取菜單
  - 使用 HTTP 直接呼叫 Serper.dev (非 SerpApi 庫)
  - Jina Reader 轉換為 Markdown

### 2. AI 處理層 (70%)

**檔案**: `services/pipeline/intelligence.py`

- ✅ `MenuParser.parse_from_text()`: Gemini 文字解析
- ✅ `MenuParser.parse_from_images()`: Gemini Vision OCR
  - 使用 `gemini-1.5-flash` (正確版本)
  - 圖片 Base64 編碼
- ✅ `InsightEngine.fuse_reviews()`: 評論融合

**缺少**:
- ❌ `MenuIntelligence.analyze_dish_batch()`: AI 屬性標註

### 3. 管線協調層 (80%)

**檔案**: `services/pipeline/orchestrator.py`

- ✅ `RestaurantPipeline.process()`: 完整流程
  - 平行執行 Map + Web providers
  - Text → Vision → Fallback 邏輯
  - 評論融合

**缺少**:
- ❌ 屬性標註整合（需在 STEP 3 加入）

### 4. 資料結構 (100%)

**檔案**: `schemas/restaurant_profile.py`

- ✅ `DishAttributes`: 完整屬性定義
  - 硬過濾: `is_spicy`, `contains_beef` 等
  - 軟排序: `flavors`, `textures` 等
  - 價值: `is_signature`, `sentiment_score` 等

- ✅ `MenuItem`: 已更新
  - 新增 `analysis: DishAttributes`
  - 新增 `id: str`
  - 新增 `image_url: str`

### 5. 部署 (100%)

- ✅ Cloud Run 部署成功
- ✅ Build ID: `d87e9984-7d8a-409c-9ae0-5e7ae2e45a26`
- ✅ Revision: `oderwhat-staging-00031-9bk`

---

## ❌ 待開發功能

### Phase 1: AI 屬性標註

1. **Task 3**: 實作 `MenuIntelligence.analyze_dish_batch()`
   - 使用 `gemini-2.0-flash-exp` 進行批次分析
   - 輸出 `List[DishAttributes]`

2. **Task 4**: 整合到 Pipeline
   - 在 `orchestrator.py` 的 STEP 3 呼叫
   - 將屬性綁定到 `MenuItem.analysis`

### Phase 2: 推薦系統

3. **Task 5**: 建立 `UserInputV2` schema
4. **Task 6-7**: 實作 `RecommendationService`
   - Hard Filter (Python)
   - Soft Ranking (LLM)
5. **Task 8**: 建立 `/api/v1/recommend` 端點

### Phase 3: 測試

6. **Task 11-13**: 單元測試 + 整合測試 + 效能測試

---

## ⚠️ 當前問題

### ✅ 已解決：API 超時問題 (2025-12-03 11:28 UTC+8)

**症狀**:
- API 請求無回應（超過 60 秒）
- 所有餐廳返回 "Fallback Dish"

**根本原因（已修復）**:
1. ✅ **環境變數缺失**: SERPER_API_KEY, JINA_API_KEY, GOOGLE_API_KEY 未設定在 Cloud Run
2. ✅ **Gemini Vision 模型錯誤**: 使用 `gemini-1.5-flash` 但 v1beta API 不支援

**修復措施**:
1. ✅ 已添加所有缺失的環境變數到 Cloud Run (revision: oderwhat-staging-00032-t2g)
2. ✅ 已將 Vision 模型改為 `gemini-1.5-flash-001`

### 🔴 剩餘問題

**1. SERPER_API_KEY 無效**
- 狀態: 403 Forbidden - "Unauthorized. Sign up for a free account."
- 影響: WebSearch 功能無法使用，只能依賴 Vision API
- 解決方案: 需要更新有效的 Serper.dev API Key

**2. Vision API 測試中**
- 部署新版本中 (revision: oderwhat-staging-00033-xxx)
- 待測試 `gemini-1.5-flash-001` 是否能正常工作

---

## 📊 開發進度

```
總體進度: ████████░░ 75%

Phase 0: 基礎架構   ████████████ 100%
Phase 1: AI 屬性標註 ████░░░░░░░░  30%
Phase 2: 推薦系統    ░░░░░░░░░░░░   0%
Phase 3: 測試優化    ░░░░░░░░░░░░   0%
```

---

## 🔧 技術棧

### 已使用
- **後端**: FastAPI, Python 3.11
- **AI**: Google Gemini (2.0-flash-exp, 1.5-flash)
- **資料**: Apify, Serper.dev, Jina Reader
- **資料庫**: Firestore
- **部署**: Cloud Run

### 環境變數需求
```bash
GEMINI_API_KEY=AIza...
APIFY_API_TOKEN=apify_...
SERPER_API_KEY=...
PROJECT_ID=gen-lang-client-0415289079
```

---

## 📁 檔案結構

```
OderWhat/
├── api/v1/
│   ├── restaurant.py          # ✅ 現有端點
│   └── recommend.py           # ❌ 待建立
├── schemas/
│   ├── pipeline.py            # ✅ 中間資料結構
│   ├── restaurant_profile.py  # ✅ 最終資料結構（含 DishAttributes）
│   └── recommendation.py      # ❌ 待建立（UserInputV2）
├── services/
│   ├── firestore_service.py   # ✅ DB 層
│   ├── restaurant_aggregator.py  # ✅ 主要協調器
│   └── pipeline/              # ✅ 新管線
│       ├── providers.py       # ✅ 資料獲取
│       ├── intelligence.py    # ⚠️  70% 完成（缺 MenuIntelligence）
│       └── orchestrator.py    # ⚠️  80% 完成（缺屬性整合）
└── agent/
    └── recommendation.py      # ❌ 待建立
```

---

## 🎯 下一步行動

### 優先級 1（緊急）
1. ✅ 查看 Cloud Run 日誌找出當前 API 問題
2. ✅ 修復部署錯誤

### 優先級 2（核心功能）
3. 實作 Task 3: `MenuIntelligence.analyze_dish_batch()`
4. 實作 Task 4: 整合到 Pipeline
5. 測試屬性標註是否正常運作

### 優先級 3（新功能）
6. 實作 Tasks 5-8: 完整推薦系統

---

## 📝 已知限制

1. **Gemini Vision API**:
   - 每次最多處理 5 張圖片
   - 必須使用 `gemini-1.5-flash`（不能用 2.5）

2. **Apify 成本**:
   - 每次 Cold Start 消耗 1 次 Apify 請求
   - 建議實作 Firestore 快取（已實作）

3. **效能瓶頸**:
   - Vision OCR 需要 10-15 秒
   - Gemini 文字解析需要 3-5 秒
   - 總 Cold Start 時間: 30-60 秒

---

## 💡 優化建議

1. **快取策略**:
   - ✅ 已實作 Firestore 快取
   - 考慮加入 Redis 快取（熱門餐廳）

2. **並行優化**:
   - ✅ 已實作 Map + Web 並行獲取
   - 可考慮 Vision + Text 並行處理

3. **成本優化**:
   - 使用 `gemini-1.5-flash` 取代 2.0（更便宜）
   - 限制 Apify 圖片數量（10 張已是最佳值）

---

## 📞 聯絡資訊

- **專案**: OderWhat
- **環境**: Staging
- **GCP Project**: gen-lang-client-0415289079
- **Region**: asia-east1

**Cloud Run URL**:
```
https://oderwhat-staging-u33peegeaa-de.a.run.app
```

**Logs URL**:
```
https://console.cloud.google.com/run/detail/asia-east1/oderwhat-staging/logs?project=gen-lang-client-0415289079
```
