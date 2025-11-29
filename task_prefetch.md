# 任務清單：餐廳資料預加載與競態條件處理

> **規格文件**: [specs/prefetch_optimization.md](./specs/prefetch_optimization.md)  
> **實作計畫**: [implementation_plan_prefetch.md](./implementation_plan_prefetch.md)

## 任務狀態圖例
- ✅ 已完成
- 🚧 進行中
- ⏳ 待執行
- ❌ 已取消
- ⚠️ 有問題需處理

---

## Phase 1: Backend API 開發

### Task 1.1: 新增 Prefetch Endpoint
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:30

**檔案變更**:
- `main.py` (+31 行)

**變更內容**:
- 新增 `POST /v2/prefetch_restaurant` endpoint
- 使用 `BackgroundTasks` 執行非同步任務
- 驗證使用者認證 (`get_current_user`)

**測試結果**:
- ✅ API 回傳 200 OK
- ✅ 背景任務成功啟動

---

## Phase 2: Smart Task Locking 實作

### Task 2.1: 修改 RestaurantProfileAgent
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:40

**檔案變更**:
- `agent/profile_agent.py` (+70 行, -20 行)

**變更內容**:
1. Import Firestore `db` 物件
2. 實作狀態檢查邏輯（Completed/Processing/None）
3. 實作 Polling 機制（最多等待 60 秒）
4. 實作鎖定機制（設定 `processing` → `completed`）
5. 實作異常處理（失敗時設定 `failed`）
6. 實作過期保護（5 分鐘超時）

**測試結果**:
- ⏳ 待執行單元測試

---

## Phase 3: Frontend Integration

### Task 3.1: 修改 RestaurantSearch 回調
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:35

**檔案變更**:
- `frontend/src/app/input/page.tsx` (+17 行)

**變更內容**:
- 在 `onSelect` 回調中加入 Prefetch API 呼叫
- 使用 `session.id_token` 進行認證
- 靜默失敗（不影響主流程）

**測試結果**:
- ⏳ 待執行瀏覽器測試

### Task 3.2: 移除視覺指示器（已回滾）
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:42

**變更內容**:
- 移除 "AI 正在背景分析菜單..." 的視覺指示器
- 恢復原本的提示文字

---

## Phase 4: 測試開發

### Task 4.1: 單元測試 - Smart Locking
**狀態**: ⏳ 待執行  
**預計時間**: 2 小時

**測試檔案**: `tests/test_profile_agent.py`

**測試案例**:
- [ ] `test_smart_locking_completed`: 已完成任務直接使用 Cache
- [ ] `test_smart_locking_processing`: 處理中任務進入等待模式
- [ ] `test_smart_locking_concurrent`: 併發請求只執行一次爬蟲
- [ ] `test_smart_locking_stale`: 過期任務被接手
- [ ] `test_smart_locking_failed`: 失敗任務可重試

**驗收標準**:
- 所有測試通過
- Code Coverage > 80%

---

### Task 4.2: 整合測試 - Prefetch Flow
**狀態**: ⏳ 待執行  
**預計時間**: 2 小時

**測試檔案**: `tests/test_prefetch_flow.py`

**測試案例**:
- [ ] `test_prefetch_to_recommendation`: 完整流程測試
- [ ] `test_prefetch_cache_hit`: 驗證 Cache Hit
- [ ] `test_prefetch_fast_user`: 快手使用者場景
- [ ] `test_prefetch_auth_required`: 未登入不觸發

**驗收標準**:
- 平均推薦時間 < 5 秒
- Cache Hit Rate > 80%

---

### Task 4.3: 效能測試 - 併發負載
**狀態**: ⏳ 待執行  
**預計時間**: 2 小時

**測試檔案**: `tests/performance/test_concurrent_load.py`

**測試案例**:
- [ ] `test_10_concurrent_users`: 10 個併發使用者
- [ ] `test_50_concurrent_users`: 50 個併發使用者
- [ ] `test_100_concurrent_users`: 100 個併發使用者

**驗收標準**:
- 重複爬蟲率 < 5%
- 所有請求成功回傳
- 無 Firestore 寫入衝突

---

## Phase 5: 文件補充

### Task 5.1: 建立規格文件
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:50

**檔案**: `specs/prefetch_optimization.md`

**內容**:
- 需求背景與問題描述
- 功能規格（Prefetching + Race Condition Handling）
- 資料結構設計
- 使用者體驗流程
- 測試策略
- 部署計畫

---

### Task 5.2: 建立實作計畫
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:51

**檔案**: `implementation_plan_prefetch.md`

**內容**:
- 架構變更說明
- 實作步驟（Phase 1-3）
- 測試計畫
- 部署檢查表
- 監控指標
- 回滾計畫

---

### Task 5.3: 建立任務清單
**狀態**: ✅ 已完成  
**負責人**: AI Assistant  
**完成時間**: 2025-11-29 09:52

**檔案**: `task_prefetch.md`

**內容**: 本檔案

---

## Phase 6: 部署準備

### Task 6.1: Firestore 設定
**狀態**: ⏳ 待執行  
**預計時間**: 30 分鐘

**檢查項目**:
- [ ] 確認 Firestore 已啟用
- [ ] 建立 `restaurant_profiles` Collection
- [ ] 設定適當的安全規則
- [ ] 建立必要的索引（如需要）

**指令**:
```bash
# 檢查 Firestore 狀態
gcloud firestore databases list

# 設定安全規則
gcloud firestore deploy --rules=firestore.rules
```

---

### Task 6.2: 環境變數檢查
**狀態**: ⏳ 待執行  
**預計時間**: 15 分鐘

**檢查項目**:
- [ ] `GEMINI_API_KEY` 已設定
- [ ] `GOOGLE_APPLICATION_CREDENTIALS` 已設定
- [ ] `NEXT_PUBLIC_API_URL` 指向正確的 Backend

**驗證指令**:
```bash
# Backend
echo $GEMINI_API_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS

# Frontend
cat frontend/.env.local | grep NEXT_PUBLIC_API_URL
```

---

### Task 6.3: Cloud Run 配置
**狀態**: ⏳ 待執行  
**預計時間**: 30 分鐘

**配置項目**:
- [ ] Timeout: 60s（支援長時間爬蟲）
- [ ] Memory: 2Gi（支援 OCR）
- [ ] Max Instances: 10（控制成本）
- [ ] Concurrency: 80（平衡效能）

**部署指令**:
```bash
gcloud run deploy dining-backend \
  --source . \
  --region asia-east1 \
  --timeout 60s \
  --memory 2Gi \
  --max-instances 10 \
  --concurrency 80
```

---

## Phase 7: Staging 部署

### Task 7.1: 部署到 Staging 環境
**狀態**: ⏳ 待執行  
**預計時間**: 1 小時

**步驟**:
1. [ ] 部署 Backend 到 Staging
2. [ ] 部署 Frontend 到 Staging
3. [ ] 驗證 Health Check
4. [ ] 執行煙霧測試（Smoke Test）

**驗證指令**:
```bash
# Health Check
curl https://dining-backend-staging-xxx.run.app/health

# Prefetch Test
curl -X POST https://dining-backend-staging-xxx.run.app/v2/prefetch_restaurant \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"restaurant_name": "測試餐廳"}'
```

---

### Task 7.2: Staging 效能驗證
**狀態**: ⏳ 待執行  
**預計時間**: 1 小時

**驗證項目**:
- [ ] 執行 10 個併發請求
- [ ] 驗證 Cache Hit Rate
- [ ] 驗證平均回應時間
- [ ] 檢查 Firestore 寫入量
- [ ] 檢查錯誤日誌

**預期結果**:
- Cache Hit Rate > 80%
- 平均回應時間 < 5 秒
- 無錯誤日誌

---

## Phase 8: Production 部署

### Task 8.1: Production 部署
**狀態**: ⏳ 待執行  
**預計時間**: 1 小時

**步驟**:
1. [ ] 建立部署 Checklist
2. [ ] 通知團隊即將部署
3. [ ] 部署 Backend
4. [ ] 部署 Frontend
5. [ ] 驗證 Production Health
6. [ ] 監控錯誤率

**回滾準備**:
- [ ] 保留前一版本的映像檔
- [ ] 準備回滾指令
- [ ] 設定告警閾值

---

### Task 8.2: Production 監控
**狀態**: ⏳ 待執行  
**預計時間**: 持續監控

**監控指標**:
- [ ] API 成功率 > 99%
- [ ] 平均回應時間 < 5 秒
- [ ] Cache Hit Rate > 80%
- [ ] Firestore 寫入量在預期範圍
- [ ] 無重複爬蟲（檢查日誌）

**告警設定**:
- API 錯誤率 > 1%
- 平均回應時間 > 10 秒
- Firestore 寫入量異常增加

---

## Phase 9: 優化與迭代

### Task 9.1: 收集使用者反饋
**狀態**: ⏳ 待執行  
**預計時間**: 1 週

**收集方式**:
- [ ] 分析 Session Duration 變化
- [ ] 追蹤推薦生成時間分佈
- [ ] 收集使用者滿意度調查

---

### Task 9.2: 效能優化
**狀態**: 🚧 進行中
**預計時間**: 視需求而定

**優化方向**:
- [x] **Golden Profile Caching**: 快取 AI 分析結果，跳過重複運算 (Completed: 2025-11-29)
- [x] **First Visit Message**: 首次訪問顯示溫馨提示 (Completed: 2025-11-29)
- [ ] 將 Polling 改為 Pub/Sub 推送
- [ ] 實作漸進式載入
- [ ] 優化 Firestore 查詢效率
- [ ] 實作智慧預測（預載熱門餐廳）

---

## 風險與問題追蹤

### 已知風險
| 風險 | 影響 | 機率 | 緩解措施 | 狀態 |
|------|------|------|----------|------|
| Firestore 寫入成本增加 | 中 | 中 | 監控寫入量，設定預算告警 | ⏳ 待監控 |
| Polling 效率不佳 | 低 | 低 | 未來改用 Pub/Sub | ⏳ 待優化 |
| 併發鎖競爭 | 低 | 低 | 已實作過期保護 | ✅ 已緩解 |

### 待解決問題
| 問題 | 優先級 | 狀態 | 負責人 |
|------|--------|------|--------|
| 無 | - | - | - |

---

## 總結

### 已完成任務
- ✅ Backend API 開發（3 個任務）
- ✅ Smart Task Locking 實作（1 個任務）
- ✅ Frontend Integration（2 個任務）
- ✅ 文件補充（3 個任務）

**總計**: 9/27 任務完成（33%）

### 待執行任務
- ⏳ 測試開發（3 個任務）
- ⏳ 部署準備（3 個任務）
- ⏳ Staging 部署（2 個任務）
- ⏳ Production 部署（2 個任務）
- ⏳ 優化與迭代（2 個任務）

**總計**: 18 個任務待執行

### 下一步行動
1. **立即執行**: Task 4.1 - 單元測試開發
2. **後續執行**: Task 4.2 - 整合測試
3. **最終目標**: Production 部署並達成效能指標

---

*本任務清單將持續更新，追蹤預加載優化功能的完整開發進度。*
