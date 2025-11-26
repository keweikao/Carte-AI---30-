# 技術實作計畫 (v1.1 - 無 OCR 版)

本文件定義了「AI 點餐經紀人」MVP 的後端技術實作方法，是對 `specification.md` (v1.1) 的具體化。

## 1\. 技術堆疊 (Tech Stack)

*   **Backend Framework:** Python (FastAPI)
*   **AI Model (Reasoning):** Google Gemini 1.5 Flash
*   **Data APIs:**
    *   Google Places API (New)
    *   Google Custom Search JSON API
*   **Data Validation:** Pydantic
*   **Caching (Optional):** Redis

## 2\. 專案結構 (Backend)

```
/
├── main.py                 # FastAPI 應用主入口
├── agent/
│   ├── __init__.py
│   ├── dining_agent.py     # 核心 AI Agent 邏輯
│   ├── data_fetcher.py     # 負責呼叫外部 API (Google Maps/Search)
│   └── prompt_builder.py   # 負責根據規則動態生成 Prompt
├── schemas/
│   ├── __init__.py
│   └── recommendation.py   # 定義 API Request Body 和 Response Body 的 Pydantic 模型
├── .env                    # 存放 API Keys
└── requirements.txt        # 專案依賴
```

## 3\. 核心模組詳解

### `schemas/recommendation.py`

*   **目的:** 使用 Pydantic 定義嚴格的資料結構，確保 API 的輸入和輸出都符合 `specification.md` 的定義。
*   **主要模型:**
    *   `RecommendationRequest`: 定義前端發送請求的 Body 格式 (餐廳, 模式, 人數, 預算等)。
    *   `RecommendationItem`: 定義單個推薦菜色的結構 (id, name, price, reason 等)。
    *   `RecommendationGroup`: 定義菜色分組的結構，包含 `selected_item` 和 `alternatives` 列表。
    *   `FullRecommendationResponse`: 定義最終回傳給前端的完整 JSON 結構。

### `agent/data_fetcher.py`

*   **目的:** 封裝所有與外部 API 的互動，使其與核心商業邏輯分離。
*   **主要函式:**
    *   `fetch_place_details(place_id: str) -> dict`: 呼叫 Google Places API，獲取評論和餐廳基本資訊。
    *   `fetch_menu_from_search(restaurant_name: str) -> str`: 呼叫 Google Search API，搜尋食記或菜單，並回傳網頁純文字內容。

### `agent/prompt_builder.py`

*   **目的:** 根據使用者的輸入（模式、預算、禁忌）和獲取的資料（評論、菜單文字），動態生成一個高品質、結構化的 Prompt，供 Gemini 模型使用。
*   **主要函式:**
    *   `create_prompt_for_gemini(request: RecommendationRequest, reviews_text: str, menu_text: str) -> str`:
        1.  設定 System Role (專業點餐顧問)。
        2.  注入從 `data_fetcher` 獲取的評論和菜單內容作為 RAG 的上下文。
        3.  根據 `request.mode` (sharing/individual) 插入對應的邏輯分支規則。
        4.  明確指示 AI 必須輸出符合 `FullRecommendationResponse` Pydantic schema 的 JSON。

### `agent/dining_agent.py`

*   **目的:** 這是整個系統的大腦，負責協調各模組完成一次推薦任務。
*   **`class DiningAgent:`**
    *   `async def get_recommendations(self, request: RecommendationRequest) -> FullRecommendationResponse:`
        1.  **[Fetch]** 呼叫 `data_fetcher` 中的函式，非同步地獲取評論和菜單文字。
        2.  **[Build Prompt]** 呼叫 `prompt_builder`，將獲取的資料和使用者請求組合成最終的 Prompt。
        3.  **[Call AI]** 將 Prompt 發送給 Gemini 1.5 Flash 模型，並要求其回傳 JSON 格式的字串。
        4.  **[Parse & Validate]** 解析 AI 回傳的 JSON 字串，並使用 `FullRecommendationResponse` Pydantic 模型進行驗證。如果驗證失敗，可以進行重試或回傳錯誤。
        5.  **[Return]** 回傳驗證通過的 Pydantic 物件，FastAPI 會自動將其序列化為 JSON。

### `main.py`

*   **目的:** 建立 FastAPI 應用，並定義 API 端點 (Endpoint)。
*   **主要端點:**
    *   `POST /recommendations`:
        *   接收符合 `RecommendationRequest` 格式的請求。
        *   實例化 `DiningAgent`。
        *   呼叫 `agent.get_recommendations()` 並等待結果。
        *   回傳 `FullRecommendationResponse` 格式的 JSON。

## 4\. 開發步驟

1.  **環境設定:** 建立 FastAPI 專案結構，安裝 `fastapi`, `uvicorn`, `pydantic`, `google-api-python-client`, `python-dotenv`。
2.  **Schema 定義:** 在 `schemas/` 中完整定義 Pydantic 模型。
3.  **API 串接:** 在 `agent/data_fetcher.py` 中完成 Google Places 和 Search API 的串接與測試。
4.  **Prompt 設計:** 在 `agent/prompt_builder.py` 中精心設計 Prompt 模板。
5.  **Agent 核心邏輯:** 在 `agent/dining_agent.py` 中整合所有模組，完成 AI 呼叫與資料驗證。
6.  **端點建立:** 在 `main.py` 中設定 API 端點，並進行本地測試。
7.  **部署 (Optional):** 將應用程式部署到雲端平台 (如 Google Cloud Run)。