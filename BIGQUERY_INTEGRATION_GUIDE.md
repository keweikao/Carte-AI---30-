# Carte AI 數據分析平台建置指南 (BigQuery + Looker Studio)

本指南將協助您建立一個自動化的數據分析 Dashboard，用於監控使用者成長、轉換漏斗 (Funnel) 和滿意度。

## 架構概觀

1.  **資料來源**: Google Cloud Firestore (您的資料庫)
2.  **資料同步**: Firebase Extension (Stream Firestore to BigQuery)
3.  **資料倉儲**: Google BigQuery (儲存與查詢)
4.  **視覺化**: Looker Studio (原 Google Data Studio)

---

## 第一步：設定 BigQuery 同步

最簡單且官方推薦的方法是使用 Firebase Extension。即使您主要使用 GCP Firestore，這個 Extension 依然適用。

### 1. 安裝 Extension
1.  前往 [Firebase Console](https://console.firebase.google.com/) 並選擇您的專案 (`gen-lang-client-0415289079`)。
    *   *如果尚未連結 Firebase，請先將 GCP 專案加入 Firebase。*
2.  在左側選單找到 **Extensions**。
3.  搜尋並安裝 **"Stream Firestore to BigQuery"** (由 Firebase 官方發布)。

### 2. 配置 Users Collection 同步
您需要為每個 Collection 安裝一個 Extension 實例（或配置多個）。建議先同步 `users`。

*   **Collection path**: `users`
*   **Dataset ID**: `firestore_export` (或自訂名稱)
*   **Table ID**: `users`
*   **Wildcard**: 啟用 (以便同步 subcollections，如 `sessions` 和 `activities`)
    *   *注意*：Extension 通常只能同步頂層或指定層級。如果 Wildcard 設定複雜，建議安裝多個實例分別同步：
        1.  Instance 1: Collection path = `users` (同步使用者基本資料與 feedback_history)
        2.  Instance 2: Collection path = `users/{userId}/sessions` (同步推薦 Session)
        3.  Instance 3: Collection path = `users/{userId}/activities` (同步搜尋行為)

*建議配置方式（安裝 3 次 Extension）：*
1.  **Users Sync**: Path=`users`, Table=`users_raw`
2.  **Sessions Sync**: Path=`users/{userId}/sessions`, Table=`sessions_raw`
3.  **Activities Sync**: Path=`users/{userId}/activities`, Table=`activities_raw`

---

## 第二步：BigQuery 視圖 (Views) 建立

同步後的原始資料 (Raw Data) 會包含很多 JSON 字串和 metadata。我們需要建立 SQL Views 來清理資料，方便 Looker Studio 使用。

在 [BigQuery Console](https://console.cloud.google.com/bigquery) 執行以下 SQL 建立視圖：

### 1. 搜尋行為視圖 (Search Activity)
```sql
CREATE OR REPLACE VIEW `firestore_export.view_searches` AS
SELECT
  document_id as activity_id,
  path_params.userId as user_id,
  JSON_EXTRACT_SCALAR(data, '$.query') as search_query,
  TIMESTAMP(JSON_EXTRACT_SCALAR(data, '$.timestamp')) as created_at
FROM
  `firestore_export.activities_raw_latest` -- Extension 會自動建立 _latest 視圖
WHERE
  JSON_EXTRACT_SCALAR(data, '$.type') = 'search';
```

### 2. 推薦 Session 視圖 (Sessions)
```sql
CREATE OR REPLACE VIEW `firestore_export.view_sessions` AS
SELECT
  document_id as recommendation_id,
  path_params.userId as user_id,
  JSON_EXTRACT_SCALAR(data, '$.restaurant_name') as restaurant_name,
  JSON_EXTRACT_SCALAR(data, '$.restaurant_cuisine_type') as cuisine_type,
  CAST(JSON_EXTRACT_SCALAR(data, '$.initial_total_price') AS INT64) as initial_price,
  CAST(JSON_EXTRACT_SCALAR(data, '$.final_total_price') AS INT64) as final_price,
  TIMESTAMP(JSON_EXTRACT_SCALAR(data, '$.created_at')) as created_at,
  TIMESTAMP(JSON_EXTRACT_SCALAR(data, '$.finalized_at')) as finalized_at,
  -- 判斷是否完成點餐
  (JSON_EXTRACT_SCALAR(data, '$.finalized_at') IS NOT NULL) as is_converted
FROM
  `firestore_export.sessions_raw_latest`;
```

### 3. 使用者與回饋視圖 (Users & Feedback)
由於 Feedback 是陣列，我們需要展開 (UNNEST)。

```sql
CREATE OR REPLACE VIEW `firestore_export.view_feedback` AS
SELECT
  document_id as user_id,
  f.rating,
  f.comment,
  f.product_feedback,
  f.recommendation_id
FROM
  `firestore_export.users_raw_latest`,
  UNNEST(JSON_EXTRACT_ARRAY(data, '$.feedback_history')) as feedback_json,
  UNNEST([STRUCT(
    CAST(JSON_EXTRACT_SCALAR(feedback_json, '$.rating') AS INT64) as rating,
    JSON_EXTRACT_SCALAR(feedback_json, '$.comment') as comment,
    JSON_EXTRACT_SCALAR(feedback_json, '$.product_feedback') as product_feedback,
    JSON_EXTRACT_SCALAR(feedback_json, '$.recommendation_id') as recommendation_id
  )]) as f;
```

---

## 第三步：Looker Studio 儀表板製作

1.  前往 [Looker Studio](https://lookerstudio.google.com/)。
2.  建立 **Blank Report**。
3.  選擇 **BigQuery** 作為資料來源。
4.  選擇您的專案 -> Dataset (`firestore_export`) -> 選擇剛剛建立的 Views (`view_searches`, `view_sessions`, `view_feedback`)。

### 建議圖表配置

#### 1. 使用者成長 (User Growth)
*   **資料來源**: `view_sessions` (以 user_id 去重) 或 `view_searches`
*   **圖表**: 時間序列圖 (Time Series)
*   **維度**: Date (created_at)
*   **指標**: Count Distinct User ID (DAU)

#### 2. 轉換漏斗 (Conversion Funnel)
*   **資料來源**: 混合 `view_searches` 和 `view_sessions` (需要 Data Blend)
*   **指標**:
    1.  **Searches**: Count of `view_searches`
    2.  **Recommendations**: Count of `view_sessions`
    3.  **Orders**: Count of `view_sessions` where `is_converted` = true
*   **計算**:
    *   Search -> Rec. Rate = (Recommendations / Searches) %
    *   Rec. -> Order Rate = (Orders / Recommendations) %

#### 3. 滿意度監控 (Satisfaction)
*   **資料來源**: `view_feedback`
*   **圖表**: 記分卡 (Scorecard) & 長條圖
*   **指標**: Average Rating
*   **維度**: Rating 分佈 (1-5分)

#### 4. 產品許願池 (Feature Requests)
*   **資料來源**: `view_feedback`
*   **圖表**: 表格 (Table)
*   **篩選**: `product_feedback` is not null
*   **欄位**: `product_feedback`, `rating`, `comment`

---

## 常見問題

### Q: 為什麼不直接用 Firestore 查詢？
A: Firestore 是 NoSQL 資料庫，擅長讀寫單一文件，但不擅長「計算總數」或「跨表聚合」。每次計算 `count(*)` 都需要讀取所有文件，費用昂貴且速度慢。BigQuery 是專為分析設計的，處理百萬級資料只需幾秒且成本極低。

### Q: 資料同步有延遲嗎？
A: 使用 Firebase Extension 幾乎是即時的 (Near Real-time)，通常延遲在幾秒到一分鐘內。

### Q: 費用如何？
1.  **Firebase Extension**: 每月少量費用（Cloud Functions 執行費），低流量下幾乎免費。
2.  **BigQuery**: 儲存費 + 查詢費。每月前 10GB 儲存免費，前 1TB 查詢免費。對於目前的規模，**幾乎是 0 元**。
3.  **Looker Studio**: 免費。
