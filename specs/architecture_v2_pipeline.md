# Project Specification: OderWhat (Menu-First Architecture)

## 1. 系統概述 (System Overview)

本專案為 AI 智慧點餐代理。核心目標是透過 **「菜單優先 (Menu-First)」** 與 **「預計算 (Pre-computation)」** 策略，解決傳統 LLM Agent 響應過慢與資訊不精準的問題。

### 核心變更

  * **從**: `Agentic Workflow` (LLM 負責搜尋、閱讀、推理衝突、決策)。
  * **到**: `Pipeline Workflow` (Apify 批量獲取 -> OCR 確立骨架 -> Python 統計標籤 -> 預計算存儲 -> 即時檢索)。

-----

## 2. 技術堆疊 (Tech Stack)

| 元件 | 技術選型 | 用途說明 |
| :--- | :--- | :--- |
| **Backend Framework** | **Python (FastAPI)** | 高效能非同步處理，適合整合 AI Pipeline。 |
| **Data Scraper** | **Apify (google-maps-scraper)** | 批量抓取餐廳圖片 (Menu) 與評論 (Reviews)。 |
| **OCR / Vision** | **Gemini 1.5 Pro** | **Ground Truth Source**。將菜單圖片轉為結構化 JSON。 |
| **Filtering / Tagging** | **Gemini 1.5 Flash** | 低成本模型。用於過濾非菜單圖片、標記評論標籤。 |
| **Logic Processing** | **Python (Pandas/Native)** | 統計評論數據、計算價格與營養均衡 (取代 LLM 推理)。 |
| **Database** | **Google Firestore** | 儲存 `Golden Profile`、預計算套餐與使用者記錄。 |
| **Infrastructure** | **GCP Cloud Run / Functions** | 託管 API 與背景 Worker。 |

-----

## 3. 資料流架構 (Data Flow Architecture)

### 3.1 總體流程圖 (Mermaid)

```mermaid
graph TD
    %% 使用者互動層
    User[Client / Frontend] -->|POST /recommend| API[FastAPI Orchestrator]
    
    %% 決策與讀取層 (Warm Start)
    subgraph ReadLayer [Orchestrator Stage]
        API -->|Query| DB[(Firestore)]
        DB -->|Check Cache| CacheHit{Status == Indexed?}
        
        CacheHit -- Yes --> Retriever[Scenario Retriever]
        Retriever -->|JSON| Generator[Response Generator (Flash)]
        Generator -->|Stream| User
    end

    %% 資料寫入層 (Cold Start)
    subgraph WriteLayer [Profiler Pipeline]
        CacheHit -- No --> Manager[Async Task Manager]
        Manager -->|Trigger| Scraper[Apify: Google Maps Scraper]
        
        %% 圖片處理流水線
        Scraper -->|Images| Filter[Image Filter (Flash)]
        Filter -->|Is Menu?| OCR[Menu Extractor (Pro)]
        OCR -->|Structured Menu| Builder[Menu Architect]
        
        %% 評論處理流水線
        Scraper -->|Reviews| Stats[Python Stats Aggregator]
        Stats -->|Tags & Scores| Builder
        
        %% 整合與存檔
        Builder -->|Generate Scenarios| Precompute[Pre-computation Engine]
        Precompute -->|Save Profile| DB
    end
```

-----

## 4. 核心模組規格 (Component Specifications)

### 4.1 Orchestrator (API Layer)

負責處理使用者請求，決定是「讀取快取」還是「觸發爬蟲」。

  * **Endpoint**: `POST /api/v1/recommend`
  * **Logic**:
    1.  檢查 Firestore 是否有該餐廳且 `status == "indexed"`。
    2.  **IF Indexed (Warm Start)**:
          * 將使用者 Query 轉換為篩選條件 (e.g., `budget < 500`, `people = 2`)。
          * 從 Firestore 直接讀取 `precomputed_sets` 中最匹配的組合。
          * 使用 Gemini Flash 將 JSON 轉為對話文字回傳。
          * **Latency Target**: < 3s.
    3.  **IF Not Indexed (Cold Start)**:
          * 回傳 `HTTP 202 Accepted` 或 SSE 事件，帶上基本資訊 (Google Places Basic Info)。
          * 背景觸發 `Profiler Pipeline`。
          * 前端顯示進度條，等待 Pipeline 完成後推送通知。

### 4.2 Profiler Pipeline (Worker Layer)

負責將非結構化數據轉換為黃金檔案 (Golden Profile)。

#### Step 1: Ingestion (Apify)

  * **Action**: 呼叫 `google-maps-scraper`。
  * **Params**: `maxImages: 5`, `maxReviews: 5`, `language: "zh-TW"`.

#### Step 2: Image Processing (OCR)

  * **Filter (Gemini Flash)**:
      * Prompt: "Is this image a restaurant menu? Answer YES or NO."
      * Input: 50 張圖片 URL。
  * **OCR (Gemini Pro)**:
      * Input: 過濾後的菜單圖片。
      * Output Schema: List of Dishes.
      * **Constraint**: 必須回傳 `source_image_url` 作為證據 (Evidence)。

#### Step 3: Review Analysis (Python + Flash)

  * **Python**: 計算關鍵字頻率 (Count Vectorizer), 平均星等。
  * **Flash**: 根據統計數據為每道菜打標籤 (e.g., `["spicy", "must-try", "big-portion"]`).

#### Step 4: Pre-computation (Menu Architect)

  * **Action**: 根據 OCR 菜單與標籤，預先組合常見場景的套餐。
  * **Scenarios**:
    1.  `dating_2` (2人, 高單價, 氣氛)
    2.  `family_4` (4人, 分食, 高CP)
    3.  `solo_1` (1人, 主食+湯)
    4.  `budget_low` (低價位組合)

-----

## 5. 資料庫設計 (Firestore Schema)

這是新架構的核心合約，所有的 Agent 都必須遵守此結構。

**Collection**: `restaurants`
**Document ID**: `{google_place_id}`

```json
{
  "meta": {
    "name": "鼎泰豐 信義店",
    "place_id": "ChIJ...",
    "address": "...",
    "status": "indexed", // "pending", "error"
    "last_updated": "2023-10-27T10:00:00Z"
  },
  
  // 1. 菜單庫 (Ground Truth) - 來自 OCR
  "menu_items": [
    {
      "id": "d_01",
      "name": "排骨蛋炒飯",
      "price": 280,
      "category": "米食",
      "description": "...",
      "tags": ["必點", "人氣top3", "不辣"], // 來自 Review Analysis
      "evidence": {
        "image_url": "https://lh3.googleusercontent.com/...", // 來自 Apify 原始圖
        "ocr_confidence": 0.95
      }
    },
    { "id": "d_02", "name": "酸辣湯", "price": 110, "tags": ["微辣"] }
  ],

  // 2. 預計算場景 (Cache for Speed) - 來自 Menu Architect
  "precomputed_sets": {
    "dating_2_people": {
      "title": "精緻雙人饗宴",
      "total_price": 850,
      "items": ["d_01", "d_02", "d_05"], // 參照 menu_items 的 id
      "reasoning": "包含了網友激推的排骨炒飯，搭配清爽的小菜..."
    },
    "solo_worker": {
      "title": "快速獨享餐",
      "total_price": 300,
      "items": ["d_01", "d_08"],
      "reasoning": "一份主食配一碗湯，快速又滿足..."
    }
  }
}
```

-----

## 6. 開發提示 (Development Prompts for LLM)

若您使用 Cursor 或 ChatGPT 開發，可使用以下 Prompts：

  * **實作 OCR Agent 時**:

    > "Create a Python function using Gemini 1.5 Pro Vision. It takes a list of image URLs, identifies which ones are menus, and extracts dish names, prices, and categories into a strict JSON format. It must include the source image URL for each extracted dish."

  * **實作 Pre-computation 時**:

    > "Create a `MenuArchitect` logic. It takes a structured list of dishes (with tags and prices). It should programmatically generate 3 set menus: for a couple (budget optimized), for a group of 4 (sharing optimized), and for a solo diner. Store these as a dictionary keyed by scenario name."

  * **實作 Cold Start API 時**:

    > "Implement a FastAPI endpoint `/recommend` that checks Firestore first. If data is missing, it should kick off a background task (using Celery or FastAPI BackgroundTasks) to run the Apify scraper, and immediately return a 'processing' status to the client."
