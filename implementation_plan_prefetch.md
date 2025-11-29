# 實作計畫：餐廳資料預加載與競態條件處理

> **規格文件**: [specs/prefetch_optimization.md](./specs/prefetch_optimization.md)

## 1. 實作概覽

### 目標
實作餐廳資料的預加載機制與智慧型任務鎖，將推薦生成時間從 15 秒縮短至 5 秒以內。

### 核心策略
1. **時間平移 (Time Shifting)**: 利用使用者填寫表單的時間執行爬蟲
2. **請求合併 (Request Coalescing)**: 避免重複執行相同的爬蟲任務
3. **分散式鎖 (Distributed Lock)**: 使用 Firestore 協調多個 Worker

---

## 2. 架構變更

### 2.1 新增元件

```
Backend (main.py)
├── /v2/prefetch_restaurant [NEW]
│   └── 觸發背景任務
│
Agent (profile_agent.py)
├── RestaurantProfileAgent.analyze() [MODIFIED]
│   ├── Smart Task Locking [NEW]
│   ├── Status Check [NEW]
│   └── Polling Logic [NEW]
│
Frontend (input/page.tsx)
└── RestaurantSearch.onSelect [MODIFIED]
    └── 呼叫 Prefetch API [NEW]
```

### 2.2 資料流

```
[使用者選餐廳]
    ↓
[前端] onSelect 觸發
    ↓
[API] POST /v2/prefetch_restaurant
    ↓
[BackgroundTask] 啟動 ProfileAgent
    ↓
[Firestore] 寫入 status=processing
    ↓
[爬蟲] 並行執行 Visual/Review/Search
    ↓
[Firestore] 更新 status=completed + 存 Cache
    ↓
[使用者提交推薦請求]
    ↓
[ProfileAgent] 檢查 Firestore 狀態
    ↓
[Cache Hit] 直接使用結果（秒回）
```

---

## 3. 實作步驟

### Phase 1: Backend API (已完成 ✅)

#### 3.1 新增 Prefetch Endpoint
**檔案**: `main.py`

**變更內容**:
```python
@app.post("/v2/prefetch_restaurant")
async def prefetch_restaurant(
    request: dict,
    background_tasks: BackgroundTasks,
    user_info: dict = Depends(get_current_user)
):
    # 立即回傳，任務在背景執行
    background_tasks.add_task(run_prefetch)
    return {"status": "prefetching"}
```

**測試**:
```bash
curl -X POST http://localhost:8000/v2/prefetch_restaurant \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"restaurant_name": "鼎泰豐", "place_id": "ChIJxxx"}'
```

---

### Phase 2: Smart Task Locking (已完成 ✅)

#### 3.2 修改 RestaurantProfileAgent
**檔案**: `agent/profile_agent.py`

**變更內容**:

1. **Import Firestore DB**:
```python
from services.firestore_service import get_cached_data, save_restaurant_data, db
```

2. **實作狀態檢查邏輯**:
```python
# 1. 檢查 Firestore 狀態
doc_ref = db.collection("restaurant_profiles").document(lock_key)
doc = doc_ref.get()

if doc.exists:
    status = doc.to_dict().get("status")
    
    # Case A: 已完成
    if status == "completed":
        # 繼續使用 Cache
        
    # Case B: 處理中
    elif status == "processing":
        # 進入 Polling 模式
        for _ in range(60):
            await asyncio.sleep(1)
            if doc.get("status") == "completed":
                break
```

3. **實作鎖定機制**:
```python
# 設定 Processing 狀態
doc_ref.set({
    "status": "processing",
    "timestamp": datetime.now(timezone.utc),
    "restaurant_name": restaurant_name
}, merge=True)

# 執行爬蟲...

# 完成後更新狀態
doc_ref.set({"status": "completed"}, merge=True)
```

4. **異常處理**:
```python
except Exception as e:
    # 失敗時釋放鎖
    doc_ref.set({"status": "failed"}, merge=True)
    raise e
```

**測試**:
```python
# 測試併發請求
import asyncio

async def test_concurrent():
    tasks = [
        profiler.analyze("鼎泰豐", "place_123"),
        profiler.analyze("鼎泰豐", "place_123"),
        profiler.analyze("鼎泰豐", "place_123")
    ]
    results = await asyncio.gather(*tasks)
    # 驗證只有一個爬蟲執行
```

---

### Phase 3: Frontend Integration (已完成 ✅)

#### 3.3 修改 RestaurantSearch 回調
**檔案**: `frontend/src/app/input/page.tsx`

**變更內容**:
```typescript
onSelect={({ name, place_id }) => {
    // 原有邏輯...
    
    // 新增：觸發 Prefetch
    const token = session?.id_token;
    if (token) {
        fetch(`${API_URL}/v2/prefetch_restaurant`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ restaurant_name: name, place_id })
        }).catch(err => console.error("Prefetch failed:", err));
    }
    
    setStep(2); // 繼續到下一步
}}
```

**測試**:
- 開啟 Network DevTools
- 選擇餐廳
- 驗證 `/v2/prefetch_restaurant` 被呼叫
- 驗證回應為 200 OK

---

## 4. 測試計畫

### 4.1 單元測試

**檔案**: `tests/test_profile_agent.py`

```python
import pytest
from agent.profile_agent import RestaurantProfileAgent

@pytest.mark.asyncio
async def test_smart_locking_completed():
    """測試：已完成的任務直接使用 Cache"""
    # Setup: 預先寫入 completed 狀態
    # Act: 呼叫 analyze
    # Assert: 不執行爬蟲，直接回傳

@pytest.mark.asyncio
async def test_smart_locking_processing():
    """測試：處理中的任務進入等待模式"""
    # Setup: 預先寫入 processing 狀態
    # Act: 呼叫 analyze
    # Assert: 進入 Polling，等待完成

@pytest.mark.asyncio
async def test_smart_locking_concurrent():
    """測試：併發請求只執行一次爬蟲"""
    # Act: 同時發起 3 個請求
    # Assert: 只有 1 個爬蟲執行
```

### 4.2 整合測試

**檔案**: `tests/test_prefetch_flow.py`

```python
@pytest.mark.asyncio
async def test_prefetch_to_recommendation():
    """測試：完整的 Prefetch → Recommendation 流程"""
    # 1. 呼叫 Prefetch API
    # 2. 等待 2 秒（模擬使用者填表單）
    # 3. 呼叫 Recommendation API
    # 4. 驗證回應時間 < 5 秒
```

### 4.3 效能測試

**檔案**: `tests/performance/test_concurrent_load.py`

```python
async def test_100_concurrent_users():
    """測試：100 個使用者同時查詢同一餐廳"""
    # 模擬 100 個併發請求
    # 驗證：
    # - 只有 1 個爬蟲執行
    # - 所有請求都成功回傳
    # - 平均回應時間 < 10 秒
```

---

## 5. 部署檢查表

### 5.1 環境變數檢查
- [ ] `GEMINI_API_KEY` 已設定
- [ ] `GOOGLE_APPLICATION_CREDENTIALS` 已設定（Firestore）
- [ ] Firestore 規則允許 `restaurant_profiles` 寫入

### 5.2 Firestore 設定
```bash
# 建立 Collection
gcloud firestore databases create --location=asia-east1

# 建立索引（如需要）
gcloud firestore indexes create \
  --collection-group=restaurant_profiles \
  --field-config field-path=status,order=ascending \
  --field-config field-path=timestamp,order=descending
```

### 5.3 Cloud Run 設定
```yaml
# 確保 Timeout 足夠長（爬蟲可能需要 20 秒）
timeout: 60s

# 確保 Memory 足夠（OCR 需要較多記憶體）
memory: 2Gi

# 併發設定
max-instances: 10
concurrency: 80
```

### 5.4 部署步驟
```bash
# 1. 部署後端
cd /Users/stephen/Desktop/OderWhat
gcloud run deploy dining-backend \
  --source . \
  --region asia-east1

# 2. 部署前端
cd frontend
npm run build
gcloud run deploy dining-frontend \
  --source . \
  --region asia-east1

# 3. 驗證
curl https://dining-backend-xxx.run.app/health
```

---

## 6. 監控指標

### 6.1 Firestore Metrics
- **寫入次數**: 每次 Prefetch 會寫入 2 次（processing + completed）
- **讀取次數**: 每次 Recommendation 會讀取 1-60 次（Polling）

### 6.2 API Metrics
- **Prefetch 成功率**: 目標 > 95%
- **Cache Hit Rate**: 目標 > 80%
- **平均回應時間**: 目標 < 5 秒

### 6.3 成本追蹤
- **Google Places API 呼叫次數**: 應減少 > 50%
- **Gemini API Token 使用量**: 應減少 > 30%

---

## 7. 回滾計畫

如果發現問題，可以快速回滾：

### 7.1 前端回滾
```typescript
// 移除 Prefetch 呼叫
onSelect={({ name, place_id }) => {
    updateData("restaurant_name", name);
    // 移除 fetch() 呼叫
    setStep(2);
}}
```

### 7.2 後端降級
```python
# 在 profile_agent.py 中加入 Feature Flag
USE_SMART_LOCKING = os.getenv("USE_SMART_LOCKING", "false").lower() == "true"

if not USE_SMART_LOCKING:
    # 使用舊邏輯（直接執行爬蟲）
```

---

## 8. 已知限制與未來優化

### 8.1 已知限制
- **Polling 效率**: 目前使用 `sleep(1)` 輪詢，可改用 Pub/Sub 推送
- **鎖粒度**: 目前以餐廳為單位，未來可考慮以 `place_id + date` 為單位

### 8.2 未來優化
- **WebSocket 推送**: 即時通知前端爬蟲進度
- **漸進式載入**: 先回傳部分結果，再補充完整資料
- **智慧預測**: 根據使用者歷史，預先載入可能查詢的餐廳

---

## 9. 時程規劃

| 階段 | 任務 | 狀態 | 預計時間 |
|------|------|------|----------|
| Phase 1 | Backend API | ✅ 已完成 | - |
| Phase 2 | Smart Locking | ✅ 已完成 | - |
| Phase 3 | Frontend Integration | ✅ 已完成 | - |
| Phase 4 | 單元測試 | ⏳ 待執行 | 2 小時 |
| Phase 5 | 整合測試 | ⏳ 待執行 | 2 小時 |
| Phase 6 | 部署到 Staging | ⏳ 待執行 | 1 小時 |
| Phase 7 | 效能驗證 | ⏳ 待執行 | 1 小時 |
| Phase 8 | 部署到 Production | ⏳ 待執行 | 1 小時 |

---

## 10. 成功標準

- ✅ 所有單元測試通過
- ✅ 整合測試通過
- ✅ 併發測試驗證無重複爬蟲
- ✅ 平均推薦時間 < 5 秒
- ✅ Cache Hit Rate > 80%
- ✅ 無 Production 錯誤

---

*本實作計畫定義了預加載優化的完整執行步驟，確保按部就班完成高品質的功能交付。*
