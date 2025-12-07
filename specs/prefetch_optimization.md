# 規格文件：餐廳資料預加載與競態條件處理

## 1. 需求背景

### 問題描述
在現有架構中，使用者提交推薦請求後，系統需要執行以下步驟：
1. 爬取餐廳資料（Google Reviews、菜單照片 OCR、食記搜尋）- **耗時 10-20 秒**
2. 執行 Multi-Agent 推薦邏輯（選菜、預算優化、品質檢查）- **耗時 3-5 秒**

總等待時間：**13-25 秒**，使用者體驗不佳。

### 核心洞察
使用者在「選擇餐廳」後到「提交推薦請求」之間，通常需要填寫：
- 用餐人數
- 預算
- 飲食偏好
- 用餐情境

這個過程平均需要 **15-30 秒**，這段時間是「黃金空窗期」。

### 優化目標
**將「客觀資料蒐集」與「主觀決策邏輯」解耦**，利用使用者填寫表單的時間，提前執行爬蟲任務。

---

## 2. 功能規格

### 2.1 預加載機制 (Prefetching)

#### 觸發點
- **時機**：使用者在 `RestaurantSearch` 元件中選定餐廳（`onSelect` 事件）
- **條件**：必須有有效的 `id_token`（已登入）

#### API 設計

**Endpoint**: `POST /v2/prefetch_restaurant`

**Request Body**:
```json
{
  "restaurant_name": "鼎泰豐",
  "place_id": "ChIJxxxxx" // Optional
}
```

**Response**:
```json
{
  "status": "prefetching",
  "restaurant": "鼎泰豐"
}
```

**行為**:
- 立即回傳 200 OK（不阻塞前端）
- 在背景啟動 `RestaurantProfileAgent.analyze()`
- 結果存入 Firestore Cache

### 2.2 競態條件處理 (Race Condition Handling)

#### 問題場景
1. **快手使用者**：2 秒填完表單，此時背景爬蟲還在跑（需 10 秒）
2. **併發請求**：多個使用者同時查詢同一家餐廳

#### 解決方案：Smart Task Locking

使用 Firestore 作為分散式鎖，確保同一餐廳的分析任務在全系統中只執行一次。

**狀態機設計**:

```
[None/Failed/Expired] 
    ↓ (搶鎖成功)
[Processing] 
    ↓ (分析完成)
[Completed]
```

**狀態定義**:

| 狀態 | 說明 | 行為 |
|------|------|------|
| `None` | 無記錄 | 搶鎖並執行 |
| `Processing` | 正在執行中 | 進入等待模式（Polling） |
| `Completed` | 已完成 | 直接讀取 Cache |
| `Failed` | 執行失敗 | 視為過期，重新執行 |

**過期保護**:
- 如果 `Processing` 狀態超過 **5 分鐘**，視為 Stale（可能是 Worker 當機）
- 允許新的 Worker 強制接手

---

## 3. 資料結構

### 3.1 Firestore Collection: `restaurant_profiles`

**Document ID**: `place_id` 或 `name_{restaurant_name}`

**Schema**:
```json
{
  "status": "processing" | "completed" | "failed",
  "timestamp": "2025-11-29T09:00:00Z",
  "restaurant_name": "鼎泰豐",
  "result": {
    // 僅在 status=completed 時存在
    "golden_profile": [...],
    "candidates": [...],
    "reviews_data": {...}
  }
}
```

---

## 4. 使用者體驗流程

### 4.1 理想情境（預加載成功）

```
使用者選擇餐廳 (0s)
    ↓ [觸發 Prefetch]
    ↓ (背景爬蟲開始)
使用者填寫表單 (15s)
    ↓ (背景爬蟲完成，存入 Cache)
使用者按下「生成推薦」(15s)
    ↓ [檢查 Cache]
    ↓ [Cache Hit!]
立即回傳推薦結果 (2s)
---
總等待時間：2 秒（vs 原本 15 秒）
```

### 4.2 快手情境（等待模式）

```
使用者選擇餐廳 (0s)
    ↓ [觸發 Prefetch]
    ↓ (背景爬蟲開始)
使用者快速填完表單 (2s)
    ↓ (背景爬蟲還在跑，已完成 20%)
使用者按下「生成推薦」(2s)
    ↓ [檢查狀態：Processing]
    ↓ [進入 Polling 模式]
等待背景任務完成 (8s)
    ↓ [Cache 完成]
回傳推薦結果 (2s)
---
總等待時間：10 秒（vs 原本 15 秒）
```

---

## 5. 非功能需求

### 5.1 效能指標
- **Cache Hit Rate**: 目標 > 80%
- **平均等待時間縮減**: 目標 > 50%
- **重複爬蟲率**: 目標 < 5%

### 5.2 可靠性
- **鎖過期時間**: 5 分鐘
- **Polling 超時**: 60 秒
- **失敗重試**: 自動釋放鎖，允許後續請求重試

### 5.3 成本優化
- **避免重複 API 呼叫**: Google Places API、Gemini API
- **節省運算資源**: Cloud Run 執行時間

---

## 6. 邊界條件與異常處理

| 情境 | 處理方式 |
|------|----------|
| Prefetch API 失敗 | 前端靜默失敗（不影響主流程） |
| 背景爬蟲失敗 | 設定 `status=failed`，主請求重試 |
| Polling 超時 | 放棄等待，重新執行爬蟲 |
| Firestore 連線失敗 | 降級為直接執行（無鎖保護） |
| 使用者未登入 | 不觸發 Prefetch |

---

## 7. 安全性考量

### 7.1 認證
- 所有 API 必須驗證 `id_token`
- 防止未授權的預加載請求

### 7.2 濫用防護
- 同一使用者對同一餐廳的 Prefetch 請求，1 分鐘內只執行一次
- 使用 Firestore 的 `timestamp` 檢查

---

## 8. 測試策略

### 8.1 單元測試
- `RestaurantProfileAgent.analyze()` 的狀態機邏輯
- Polling 機制的超時處理

### 8.2 整合測試
- Prefetch → Main Request 的完整流程
- 併發請求的鎖競爭測試

### 8.3 效能測試
- 模擬 100 個併發使用者查詢同一餐廳
- 驗證只有 1 個爬蟲任務執行

---

## 9. 部署計畫

### 9.1 階段一：Backend Only
- 部署 `/v2/prefetch_restaurant` API
- 部署 Smart Task Locking 邏輯
- 監控 Firestore 寫入量

### 9.2 階段二：Frontend Integration
- 前端整合 Prefetch 呼叫
- A/B Testing 驗證效果

### 9.3 階段三：監控與優化
- 追蹤 Cache Hit Rate
- 調整鎖過期時間
- 優化 Polling 策略

---

## 10. 成功指標

- ✅ 平均推薦生成時間 < 5 秒（原本 15 秒）
- ✅ 重複爬蟲率 < 5%
- ✅ API 成本降低 > 30%
- ✅ 使用者滿意度提升（透過 Session Duration 追蹤）

---

*本規格文件定義了預加載優化的完整設計，確保系統在提升效能的同時保持穩定性與成本效益。*
