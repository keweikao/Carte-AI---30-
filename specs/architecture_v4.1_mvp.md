# Carte AI - MVP 開發規格書 (v4.1)

**核心開發哲學 (MVP Philosophy):**
1.  **聚焦核心價值**: 首要任務是實現「在菜單上看到精準的避雷標示」。
2.  **善用 LLM 解決問題**: 在打造複雜演算法前，優先利用 Gemini 的語意理解能力解決諸如「菜名模糊匹配」等問題，以加速開發。
3.  **驗證先於開發**: 在投入資源開發備案前，先用最簡單的方式（冒煙測試）驗證主要方案（如 Jina）的可行性。
4.  **夠用就好**: 對於次要功能（如快取策略），採用簡單有效的方案（7 天 TTL），滿足 MVP 需求即可。

## 1\. 核心流程邏輯 (MVP Cold Start Flow)

此流程專為「冷啟動」設計，旨在用最低的開發複雜度，實現最高的數據精準度。

**觸發條件**：Firestore 無此餐廳資料，或資料已超過 7 天。

**流程**：

1.  **Initiate (啟動)**: API 層接收到請求，啟動背景任務 `HybridRestaurantService`。

2.  **Parallel Ingestion (並行資料獲取)**:
    *   **任務 A (抓取評論)**: **Apify** 啟動，抓取最新 30 則評論文本。
    *   **任務 B (搜尋菜單)**: **Serper** 啟動，搜尋官方菜單 URL (優先官網，次之 UberEats 等)。

3.  **Menu Extraction (菜單提取)**:
    *   等待 `任務 B` 完成。使用 **Jina Reader** 讀取搜尋到的最佳 URL。
    *   將讀取到的文本交給 **Gemini**，提取並生成一份 `standard_menu_list` (標準菜單列表)，包含菜品名、價格、分類和 `source_type`。
    *   **[MVP Fallback]**: 若 Jina 讀取失敗或 Serper 找不到合適的 URL，則立即切換至備援方案：**抓取 Google Maps 圖片，並使用 Vision API (OCR) 進行辨識**。最終產出的 `trust_level` 會被標記為 `medium`。

4.  **Review Analysis & Fusion (評論分析與融合 - 核心步驟)**:
    *   等待 `任務 A` 與 `步驟 3` 全部完成。
    *   將「評論列表」(來自 Apify) 和 「標準菜單列表」(來自步驟 3) **同時**餵給 **Gemini**。
    *   **Prompt 關鍵指令**:
        > 「這是一份標準菜單：`{standard_menu_list}`。請分析以下評論：`{reviews_list}`。你的任務是：
        > 1.  對每一則評論，提取其中提到的菜品名稱。
        > 2.  將提取出的菜品名稱，**模糊匹配並歸戶到標準菜單中的一個項目**。
        > 3.  總結每道被提到菜品的情感（正面/負面/中性）和一句話摘要（例如 '肉質鮮嫩多汁' 或 '份量有點少')。
        > 4.  識別評論中是否有明確的『踩雷』關鍵字，並標記對應的菜品。
        > 5.  以 JSON 格式回傳每道標準菜品的分析結果。」
    *   此步驟直接產出 `MenuItem` 中的 `ai_insight` 和 `is_risky` 欄位，巧妙地避開了複雜的模糊匹配演算法開發。

5.  **Final Aggregation & Persist (最終聚合與儲存)**:
    *   將 `步驟 4` 產出的分析結果，合併回 `步驟 3` 的標準菜單列表中。
    *   設定整份資料的 `trust_level` (`high` 代表來自官方 URL，`medium` 代表來自 OCR)。
    *   將完整的 `RestaurantProfile` 寫入 Firestore，並設定 **7 天**的有效期。
    *   回傳最新資料給使用者。

## 2\. 資料結構 (Schema Design v4.1)

*此處保留 v4.0 的優秀設計，無需變更。*

```python
# In: schemas/restaurant_profile.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class MenuItemAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(..., description="網友評價摘要，如'肉太柴'")
    mention_count: int = 0

class MenuItem(BaseModel):
    name: str
    price: Optional[int]
    category: str = "其他"
    description: Optional[str] = None
    source_type: Literal["dine_in", "delivery", "estimated", "unknown"] = "unknown"
    is_popular: bool = False
    is_risky: bool = False
    ai_insight: Optional[MenuItemAnalysis] = None

class RestaurantProfile(BaseModel):
    place_id: str
    name: str
    address: str
    updated_at: datetime
    trust_level: Literal["high", "medium", "low"]
    menu_source_url: Optional[str]
    menu_items: List[MenuItem]
    review_summary: str # 整體評價摘要
```

## 3\. MVP 開發任務清單 (MVP Task List)

### Phase 1: MVP 核心功能 (Menu & Review Fusion)

-   [x] **Task 1.1: 基礎設定**
    *   在 `.env` 中新增 `SERPER_API_KEY`, `APIFY_API_TOKEN`, `JINA_API_KEY`。
    *   更新 `requirements.txt`，確保 `apify-client`, `google-search-results`, `jina` 已被加入。
    *   根據 v4.1 規格，更新 `schemas/restaurant_profile.py`。
-   [x] **Task 1.2: Jina 可行性驗證 (Smoke Test)**
    *   建立一個一次性的 `scripts/test_jina.py` 腳本。
    *   **目標**：測試 Jina Reader 對目標網站（如 inline.app, ubereats.com）的抓取能力。
    *   **產出**：一份關於 Jina 是否能處理動態網站的評估報告，以決定 Fallback (Vision API) 的優先級。
-   [x] **Task 1.3: 實作菜單爬蟲 (`services/menu_scraper.py`)**
    *   實作 `Serper -> Jina -> Gemini` 的鏈路，以產出 `standard_menu_list`。
    *   在此模組中建立好 Fallback 邏輯：若前述鏈路失敗，則呼叫 Vision API。
-   [x] **Task 1.4: 實作評論分析與融合 (`services/review_analyzer.py`) - (最高優先級)**
    *   實作 `fetch_reviews_apify(place_id)`。
    *   實作 `analyze_and_fuse_reviews(reviews, standard_menu_list)`，在此函數中**建構並呼叫前述的 Gemini "二合一" Prompt**，完成情感分析與菜名歸戶。
-   [x] **Task 1.5: 實作協調器 (`services/restaurant_aggregator.py`)**
    *   實作 `get_restaurant_data(place_id, name)`。
    *   加入 Warm/Cold 判斷邏輯 (7 天 TTL)。
    *   在 Cold Start 路徑中，依序呼叫 Task 1.3 和 1.4，並將結果合併。
    *   呼叫 Firestore Service 進行儲存。

### Phase 2: 整合與部署 (Integration)

-   [x] **Task 2.1: 升級 Firestore Service (`services/firestore_service.py`)**
    *   確保 `save_restaurant` 和 `get_restaurant` 能處理新的 v4.1 `RestaurantProfile` 結構。
-   [x] **Task 2.2: 建立 API 端點 (`api/v1/restaurant.py`)**
    *   建立 `GET /api/v1/restaurant/{place_id}`。
    *   將請求傳遞給 `services/restaurant_aggregator.py` 並回傳結果。
-   [ ] **Task 2.3: 端到端測試** `(已阻擋 - by startup error)`
    *   手動觸發一個全新的 `place_id`，觀察 Firestore 中的數據是否符合預期，以及 API 回傳是否正確。

### Phase 3: MVP 後優化 (Post-MVP)

*以下任務在 MVP 階段不予考慮*
-   [ ] **(擱置)** Playwright 整合：用於處理 Jina 無法解析的複雜網站。
-   [ ] **(擱置)** 動態快取更新：基於評論關鍵字觸發的智慧快取失效機制。

---

## 附錄 A：除錯日誌 (Appendix A: Debugging Log)

### 2025-12-01: Jina Client 可行性驗證

-   **問題**: 在實作 `Task 1.2` 時，嘗試安裝 Jina Reader 的 Python 客戶端時遇到困難。
-   **嘗試**:
    1.  `pip install jina-ai`: 失敗，PyPI 無此套件。
    2.  `pip install jina`: 成功安裝，但 `from jina import Jina` 導入失敗，且 `docarray` 版本衝突。
    3.  `pip install jina-reader`: 再次失敗，PyPI 無此套件。
-   **結論**: Jina Reader 的 Python 客戶端安裝路徑不明確且不穩定，不適合 MVP 快速開發。
-   **解決方案**: 放棄使用其 Python 客戶端，改為在 `scripts/test_jina.py` 中直接使用 `httpx` 發送 HTTP 請求至 Jina Reader API (`https://r.jina.ai/{URL}`)。此方法成功驗證了 Jina API 的基本功能。

### 2025-12-01: API 金鑰有效性問題

-   **問題**: 在測試 `menu_scraper.py` 時，即使 API 金鑰已在 `.env` 中設定，API 呼叫仍然失敗。
-   **分析**:
    1.  **Serper**: 透過在腳本中印出原始 API 回應，發現 Serper API 回傳 `{"error": "Invalid API key."}`。這證實了 `.env` 中最初設定的 `SERPER_API_KEY` 是無效的預留位置。
    2.  **Gemini**: 在修復 Serper 金鑰後，Gemini API 呼叫失敗，顯示 `API key not valid`。日誌中有一條關鍵訊息 `Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.`，暗示函式庫可能優先使用了無效的 `GOOGLE_API_KEY`。
-   **解決方案**:
    1.  **Serper**: 請使用者提供正確的 `SERPER_API_KEY` 並更新 `.env` 檔案。
    2.  **Gemini**: 為避免金鑰選擇的模糊性，修改程式碼，不再使用全域的 `genai.configure()`，而是在呼叫時明確地將 `api_key=GEMINI_API_KEY` 傳遞給 `Client` 的建構函數。此方法成功解決了金鑰驗證問題。

### 2025-12-01: Cloud Run 部署失敗循環

-   **問題**: 在完成 `Phase 1` 和 `Phase 2` 的初步整合後，向 Cloud Run 部署應用程式時，容器反覆因 `Container failed to start` 而失敗。
-   **分析**:
    1.  **錯誤類型**: 每次部署失敗後，透過 `gcloud logging read` 讀取特定修訂版本的日誌，都發現了不同的 `ImportError` 或 `IndentationError`。
    2.  **根本原因**: 對程式碼進行了大規模重構（例如，重寫 `firestore_service.py`，新增 `restaurant_aggregator.py`），但沒有在本地進行啟動測試。每次部署都只暴露一個啟動時的致命錯誤，導致了「修復一個、出現下一個」的低效率循環。
-   **解決方案 (新策略)**:
    1.  **停止部署**: 暫停向 Cloud Run 進行任何新的部署。
    2.  **本地優先**: 將除錯的重心轉移到本地環境。
    3.  **執行 `python3 main.py`**: 直接在本地運行主程式，這將一次性暴露所有因導入錯誤、語法錯誤或縮排錯誤導致的啟動失敗問題。
    4.  **修復 -> 重新部署**: 只有在確認 `main.py` 可以在本地成功啟動（Uvicorn 正常運行）後，才再次嘗試部署到 Cloud Run。
