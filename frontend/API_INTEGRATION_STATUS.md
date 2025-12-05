# 前後端 API 整合狀態檢查

**檢查日期**: 2025-12-05  
**檢查範圍**: CARTE_AI_COMPLETE_SPEC.md 要求的 API vs 現有後端實作

---

## 📊 API 需求 vs 實作對照表

### ✅ 已實作且可用

#### 1. 餐廳搜尋 API

**規格要求**:
```typescript
GET /api/restaurants/search?q={query}&limit={limit}
```

**後端實作**:
```python
GET /places/autocomplete?input={input}
# 位置: main.py line 67-76
```

**狀態**: ✅ **已實作**
- 使用 Google Places Autocomplete API
- 支援 Mock 模式測試
- 需要 Google API Key

**前端使用**:
```typescript
// frontend/src/components/restaurant-search.tsx
const searchRestaurants = async (query: string) => {
  const res = await fetch(`/places/autocomplete?input=${query}`)
  return res.json()
}
```

**差異**: 
- 路徑不同: `/places/autocomplete` vs `/api/restaurants/search`
- 參數名稱: `input` vs `q`

**建議**: 保持現有實作,前端調整即可

---

#### 2. 推薦生成 API (同步)

**規格要求**:
```typescript
POST /api/recommendations
Body: { restaurant_id, dining_mode, party_size, preferences }
```

**後端實作**:
```python
POST /api/v1/recommend/v2
# 位置: api/v1/recommend_v2.py line 78-87
```

**狀態**: ✅ **已實作**
- 支援同步推薦
- 使用 V2 兩階段推薦 (Hard Filter + Soft Ranking)
- 返回完整推薦結果

**Schema**:
```python
class UserInputV2:
    restaurant_name: str
    place_id: Optional[str]
    party_size: int
    dietary_restrictions: List[str]
    # ... 其他欄位
```

---

#### 3. 推薦生成 API (非同步)

**規格要求**:
```typescript
POST /api/recommendations/async
返回: { job_id }
```

**後端實作**:
```python
POST /api/v1/recommend/v2/async
# 位置: api/v1/recommend_v2.py line 89-103
```

**狀態**: ✅ **已實作**
- 使用 BackgroundTasks
- 返回 job_id
- 支援狀態查詢

---

#### 4. 推薦狀態查詢

**規格要求**:
```typescript
GET /api/recommendations/status/{job_id}
```

**後端實作**:
```python
GET /api/v1/recommend/v2/status/{job_id}
# 位置: api/v1/recommend_v2.py line 105-112
```

**狀態**: ✅ **已實作**
- 使用 JobManager
- 返回 status, progress, result

---

#### 5. 替換菜色建議

**規格要求**:
```typescript
GET /api/dishes/:dishId/alternatives
```

**後端實作**:
```python
GET /api/v1/recommend/v2/alternatives?recommendation_id={id}&category={cat}&exclude={ids}
# 位置: api/v1/recommend_v2.py line 114-147
```

**狀態**: ✅ **已實作**
- 根據 category 返回替代菜色
- 支援排除已選菜色

**差異**:
- 使用 query parameters 而非 path parameter
- 需要 recommendation_id 和 category

---

#### 6. Prefetch API

**規格要求**: ❌ 規格未提及

**後端實作**:
```python
POST /api/v1/recommend/v2/prefetch?restaurant_name={name}&place_id={id}
# 位置: api/v1/recommend_v2.py line 168-208
```

**狀態**: ✅ **已實作 (額外功能)**
- 背景預載餐廳資料
- 加速後續推薦
- 前端已在使用

---

#### 7. 最終訂單確認

**規格要求**: ❌ 規格未提及

**後端實作**:
```python
POST /api/v1/recommend/v2/{recommendation_id}/finalize
# 位置: api/v1/recommend_v2.py line 214-231
```

**狀態**: ✅ **已實作 (額外功能)**
- 記錄最終選擇
- 返回 order_id

---

### ❌ 規格要求但未實作

#### 1. Google Maps URL 解析

**規格要求**:
```typescript
POST /api/restaurants/parse-url
Body: { url: string }
返回: { restaurant: Restaurant }
```

**後端實作**: ❌ **未實作**

**影響**: 
- 前端無法直接貼上 Google Maps 連結
- 需要手動輸入餐廳名稱

**建議**: 
- 可以在前端解析 Google Maps URL
- 提取 place_id 或餐廳名稱
- 或後端新增此 API

---

#### 2. SSE (Server-Sent Events) 推薦串流

**規格要求**:
```typescript
GET /api/recommendations/stream
返回: SSE events (stage, message, complete)
```

**後端實作**: ❌ **未實作**

**現有替代方案**:
- 使用非同步 API + 輪詢狀態
- JobManager 支援 progress 更新

**影響**:
- Waiting Page 無法顯示即時 AI 思考過程
- 需要輪詢而非推送

**建議**:
- 短期: 使用輪詢 (每 1-2 秒查詢一次狀態)
- 長期: 實作 SSE 或 WebSocket

---

#### 3. 分享菜單 API

**規格要求**:
```typescript
POST /api/menus/share
Body: { restaurant, dishes }
返回: { share_id, share_url }

GET /api/menus/shared/:shareId
返回: { menu, created_at, expires_at }
```

**後端實作**: ❌ **未實作**

**影響**:
- Final Menu Page 無法分享菜單
- 無法生成分享連結

**建議**:
- 可以先使用前端 localStorage
- 或生成 URL query parameters
- 長期實作後端分享功能

---

## 🔄 需要調整的部分

### 1. 路徑統一

**建議**: 統一使用 `/api/v1/` 前綴

| 規格 | 現有 | 建議 |
|------|------|------|
| `/api/restaurants/search` | `/places/autocomplete` | 保持現有或新增 alias |
| `/api/recommendations` | `/api/v1/recommend/v2` | 保持現有 |

### 2. Schema 對應

**規格的 `dining_mode`**:
```typescript
type DiningMode = 'casual' | 'date' | 'business' | 'family' | 'celebration' | 'solo'
```

**後端 Schema**: 需要確認是否支援所有模式

### 3. 錯誤碼統一

**規格要求的錯誤碼**:
- `network_error`
- `server_error`
- `timeout`
- `restaurant_not_found`
- `no_menu_data`
- `invalid_input`
- `rate_limited`

**後端**: 需要確認錯誤回應格式

---

## 📋 前端開發建議

### 立即可用的功能

1. ✅ **餐廳搜尋** - 使用 `/places/autocomplete`
2. ✅ **推薦生成** - 使用 `/api/v1/recommend/v2/async`
3. ✅ **狀態查詢** - 使用 `/api/v1/recommend/v2/status/{job_id}`
4. ✅ **替換菜色** - 使用 `/api/v1/recommend/v2/alternatives`
5. ✅ **Prefetch** - 使用 `/api/v1/recommend/v2/prefetch`

### 需要前端實作的功能

1. **Google Maps URL 解析** - 前端解析
   ```typescript
   const parseGoogleMapsUrl = (url: string) => {
     const placeIdMatch = url.match(/place_id=([^&]+)/);
     if (placeIdMatch) return placeIdMatch[1];
     // 其他解析邏輯
   }
   ```

2. **Waiting Page 進度** - 輪詢狀態
   ```typescript
   const pollStatus = async (jobId: string) => {
     const interval = setInterval(async () => {
       const status = await fetch(`/api/v1/recommend/v2/status/${jobId}`);
       // 更新 UI
     }, 1500); // 每 1.5 秒
   }
   ```

3. **分享菜單** - 使用 URL 或 localStorage
   ```typescript
   const shareMenu = (menu) => {
     const shareData = btoa(JSON.stringify(menu));
     const shareUrl = `${window.location.origin}/shared?data=${shareData}`;
     // 或使用 localStorage
   }
   ```

---

## 🎯 建議的開發順序

### Week 2: Landing Page + Onboarding + Input
- ✅ 使用現有 `/places/autocomplete`
- ✅ 使用現有 `/api/v1/recommend/v2/prefetch`
- ✅ 前端實作 Google Maps URL 解析

### Week 3: Waiting + Recommendation + Final Menu
- ✅ 使用現有 `/api/v1/recommend/v2/async`
- ✅ 輪詢 `/api/v1/recommend/v2/status/{job_id}`
- ✅ 使用現有 `/api/v1/recommend/v2/alternatives`
- ⚠️ 分享功能使用前端方案

### 未來優化 (可選)
- 實作 SSE 推薦串流
- 實作後端分享 API
- 統一 API 路徑

---

## ✅ 結論

**好消息**: 
- 🎉 **核心功能 100% 已實作**
- 🎉 **可以立即開始前端開發**
- 🎉 **後端 API 穩定且經過測試**

**需要注意**:
- ⚠️ Waiting Page 使用輪詢而非 SSE
- ⚠️ 分享功能需要前端實作
- ⚠️ API 路徑與規格略有差異

**建議**:
1. 按照現有 API 開發前端
2. 規格中的 SSE 和分享功能使用替代方案
3. 未來有需要再實作後端分享 API

---

**狀態**: ✅ **可以繼續開發**  
**阻礙**: ❌ **無**  
**下一步**: 開始 Week 2 Landing Page 開發
