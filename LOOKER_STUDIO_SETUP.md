# Looker Studio 快速設定指南

恭喜！您的 BigQuery 數據倉庫已經準備就緒。現在，我們來建立一個專業的 Dashboard。

## 1. 連接數據源

請點擊以下連結，分別建立兩個數據源 (Data Source)：

### 數據源 A: 每日漏斗 (Funnel)
1.  [點擊這裡建立數據源](https://lookerstudio.google.com/datasources/create?connectorId=bigQuery)
2.  選擇 **My Projects** -> **gen-lang-client-0415289079** -> **carte_analytics**。
3.  選擇表：**`view_dashboard_funnel`**。
4.  點擊右上角 **Connect**。
5.  將數據源命名為 **"Carte AI - Funnel Stats"**。

### 數據源 B: 使用者回饋 (Feedback)
1.  重複上述步驟，但這次選擇表：**`view_dashboard_feedback`**。
2.  將數據源命名為 **"Carte AI - Feedback Details"**。

---

## 2. 建立報表 (Report)

在建立好數據源後，點擊右上角的 **Create Report**。

### 頁面 1: 營運概況 (Overview)

**圖表 1: 每日流量趨勢 (Time Series Chart)**
*   **Data Source**: Carte AI - Funnel Stats
*   **Dimension**: `date`
*   **Metrics**: 
    *   `search_count` (搜尋量)
    *   `recommendation_count` (推薦量)
    *   `order_count` (完成訂單量)

**圖表 2: 轉換率漏斗 (Scorecard)**
*   **Data Source**: Carte AI - Funnel Stats
*   **Metric**: `conversion_search_to_rec` (平均搜尋->推薦轉化率)
    *   *設定格式為百分比 (%)*
*   **Metric**: `conversion_rec_to_order` (平均推薦->訂單轉化率)
    *   *設定格式為百分比 (%)*

### 頁面 2: 使用者回饋 (Feedback)

**圖表 3: 評分分佈 (Bar Chart)**
*   **Data Source**: Carte AI - Feedback Details
*   **Dimension**: `rating`
*   **Metric**: `Record Count`

**圖表 4: 產品許願池 (Table)**
*   **Data Source**: Carte AI - Feedback Details
*   **Filter**: 建立一個篩選器 `product_feedback Is Not Null`
*   **Dimensions**:
    *   `session_time`
    *   `rating`
    *   `product_feedback` (許願內容)
    *   `comment` (其他評論)

**圖表 5: 餐廳滿意度排行 (Table)**
*   **Data Source**: Carte AI - Feedback Details
*   **Dimension**: `restaurant_name`
*   **Metric**: `rating` (Aggregation: Average)
*   **Sort**: `rating` (Ascending) -> 查看哪些餐廳評分最低

---

## 自動更新
您的數據目前是透過 `scripts/sync_to_bq.py` 手動同步的。
若要自動更新，建議設定一個 Cron Job (例如使用 GitHub Actions Schedule 或 Cloud Scheduler) 每天執行一次該腳本。
