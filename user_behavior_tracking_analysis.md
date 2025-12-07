# 使用者行為追蹤分析：現況與 RAG 應用規劃

## 📊 目前已記錄的使用者行為

### 1. Firestore 資料庫結構

#### Collection: `users`
**Document ID**: `user_id` (Google OAuth sub)

**儲存內容**:
```json
{
  "feedback_history": [
    {
      "recommendation_id": "rec_abc123",
      "selected_items": ["小籠包", "排骨蛋炒飯", "酸辣湯"],
      "rating": 5,
      "comment": "很好吃，份量剛好"
    }
  ],
  "last_updated": "2024-11-25T12:00:00Z"
}
```

**資料來源**: `POST /feedback` API 端點
**更新機制**: `services/firestore_service.py:update_user_profile()`
- 使用 `firestore.ArrayUnion()` 追加新的 feedback
- 保留完整的歷史記錄

---

#### Collection: `restaurants`
**Document ID**: `md5(restaurant_name.lower().strip())`

**儲存內容**:
```json
{
  "name": "鼎泰豐",
  "reviews_data": {
    // Google Places API 原始評論資料
  },
  "menu_text": "小籠包 NT$200\n排骨蛋炒飯 NT$280\n...",
  "updated_at": "2024-11-25T12:00:00Z"
}
```

**資料來源**: `agent/data_fetcher.py` 自動抓取
**更新機制**: `services/firestore_service.py:save_restaurant_data()`
- 30 天快取機制
- 用於減少 Google Places API 呼叫

---

## ❌ 目前**未記錄**的使用者行為

### 1. 推薦頁面互動行為
- ❌ 使用者點選「我要點這道」的菜品
- ❌ 使用者點選「換一道」的次數
- ❌ 每道菜被換掉的原因（隱式：可能不喜歡）
- ❌ 使用者在推薦頁面停留的時間
- ❌ 使用者查看每道菜的詳細資訊次數

### 2. 換菜行為模式
- ❌ 換菜前的菜品名稱、類別、價格
- ❌ 換菜後的菜品名稱、類別、價格
- ❌ 換菜的時間戳記
- ❌ 是否多次換同一道菜

### 3. 最終點餐決策
- ❌ 使用者最終確認的完整菜單
- ❌ 最終總價 vs 系統初始建議總價的差異
- ❌ 是否遵循系統建議的類別平衡

### 4. 搜尋與瀏覽行為
- ❌ 使用者搜尋的餐廳列表
- ❌ 使用者的搜尋偏好（地點、菜系、預算範圍）
- ❌ 使用者放棄推薦的情況（未完成點餐就離開）

---

## 🎯 建議新增的追蹤機制（針對 RAG 應用）

### 優先級 1：核心互動行為 🔴

#### A. 換菜行為追蹤
**目的**: 學習使用者的菜品偏好，改善推薦準確度

**建議新增 API 端點**:
```python
POST /v2/recommendations/{recommendation_id}/swap

Request:
{
  "original_dish": {
    "dish_name": "宮保雞丁",
    "category": "熱菜",
    "price": 280
  },
  "new_dish": {
    "dish_name": "糖醋魚",
    "category": "熱菜",
    "price": 320
  },
  "timestamp": "2024-11-25T12:00:00Z"
}
```

**Firestore 結構**:
```json
{
  "users/{user_id}/sessions/{recommendation_id}": {
    "restaurant_name": "鼎泰豐",
    "initial_recommendations": [...],
    "swap_history": [
      {
        "swap_index": 1,
        "original_dish": {"dish_name": "宮保雞丁", "category": "熱菜", "price": 280},
        "new_dish": {"dish_name": "糖醋魚", "category": "熱菜", "price": 320},
        "timestamp": "2024-11-25T12:00:00Z"
      }
    ],
    "final_selections": [...],
    "created_at": "2024-11-25T11:50:00Z",
    "finalized_at": "2024-11-25T12:05:00Z"
  }
}
```

---

#### B. 最終點餐確認追蹤
**目的**: 了解使用者的真實選擇，對比系統建議

**建議新增 API 端點**:
```python
POST /v2/recommendations/{recommendation_id}/finalize

Request:
{
  "final_selections": [
    {"dish_name": "小籠包", "category": "點心", "price": 240},
    {"dish_name": "排骨蛋炒飯", "category": "主食", "price": 280}
  ],
  "total_price": 520,
  "session_duration_seconds": 180
}
```

**Firestore 結構**:
```json
{
  "users/{user_id}/orders": [
    {
      "order_id": "order_xyz789",
      "recommendation_id": "rec_abc123",
      "restaurant_name": "鼎泰豐",
      "restaurant_cuisine_type": "中式餐館",
      "user_input": {
        "dining_style": "Shared",
        "party_size": 3,
        "budget": {"type": "Per_Person", "amount": 500},
        "preferences": ["No_Beef"]
      },
      "initial_recommendations": [...],
      "final_selections": [...],
      "total_swap_count": 2,
      "initial_total_price": 640,
      "final_total_price": 520,
      "session_duration_seconds": 180,
      "created_at": "2024-11-25T11:50:00Z",
      "finalized_at": "2024-11-25T12:05:00Z"
    }
  ]
}
```

---

### 優先級 2：偏好學習 🟡

#### C. 菜品類別偏好統計
**目的**: 學習使用者對不同類別菜品的接受度

**Firestore 結構**:
```json
{
  "users/{user_id}/preferences": {
    "cuisine_preferences": {
      "中式餐館": {
        "visit_count": 15,
        "favorite_categories": ["點心", "冷菜"],
        "avoided_categories": ["湯品"],
        "avg_budget_per_person": 450
      },
      "日本料理": {
        "visit_count": 8,
        "favorite_categories": ["壽司", "刺身"],
        "avoided_categories": [],
        "avg_budget_per_person": 600
      }
    },
    "dietary_restrictions": {
      "No_Beef": 12,  // 使用次數
      "No_Pork": 0,
      "Vegetarian": 3
    },
    "price_sensitivity": {
      "avg_price_per_dish": 220,
      "max_single_dish_price": 800,
      "budget_adherence_rate": 0.85  // 85% 的時候在預算內
    }
  }
}
```

**更新機制**: 每次 `/finalize` 時自動更新統計

---

#### D. 菜品評分隱式推斷
**目的**: 從換菜行為推斷使用者偏好

**推斷邏輯**:
```python
# 被換掉的菜品 → 隱式負評 (-1 分)
# 被保留並確認的菜品 → 隱式正評 (+1 分)
# 最終獲得 5 星評價的訂單中的菜品 → 強正評 (+3 分)

{
  "users/{user_id}/dish_preferences": {
    "小籠包": {
      "implicit_score": 8,  // 被選擇 8 次
      "explicit_score": 5,  // 平均評分
      "total_exposure": 10  // 總共推薦 10 次
    },
    "宮保雞丁": {
      "implicit_score": -2,  // 被換掉 2 次
      "explicit_score": 3,
      "total_exposure": 5
    }
  }
}
```

---

### 優先級 3：進階分析 🟢

#### E. 時段與情境偏好
**目的**: 學習使用者在不同時段、場合的偏好差異

**Firestore 結構**:
```json
{
  "users/{user_id}/contextual_preferences": {
    "time_of_day": {
      "lunch": {
        "avg_budget": 300,
        "preferred_categories": ["主食", "湯品"],
        "avg_party_size": 1.5
      },
      "dinner": {
        "avg_budget": 600,
        "preferred_categories": ["熱菜", "點心"],
        "avg_party_size": 3.2
      }
    },
    "party_size_patterns": {
      "solo": {
        "preferred_dining_style": "Individual",
        "avg_dish_count": 2,
        "favorite_cuisines": ["日本料理", "美式餐廳"]
      },
      "group": {
        "preferred_dining_style": "Shared",
        "avg_dish_count": 6,
        "favorite_cuisines": ["中式餐館", "泰式料理"]
      }
    }
  }
}
```

---

## 🤖 RAG 應用場景設計

### 場景 1：個人化推薦提示詞增強

**原始 Prompt**:
```
User preferences: ["No_Beef"]
```

**RAG 增強後的 Prompt**:
```
User preferences: ["No_Beef"]

# Historical Behavior Analysis (Last 10 Orders)
- Frequently selects: 小籠包 (8/10), 炒空心菜 (6/10), 酸辣湯 (7/10)
- Frequently swaps: 宮保雞丁 (3/5 times recommended), 紅燒肉 (2/3 times)
- Favorite categories: 點心 (70% acceptance), 冷菜 (80% acceptance)
- Avoided categories: 湯品 (30% acceptance - often swapped)
- Average budget adherence: 85% (usually within ±10% of budget)

# Context
- Current time: 12:30 PM (Lunch)
- At lunch, user typically prefers lighter dishes (主食 + 1-2 小菜)
- Party size: 3 (Group dining - user prefers 4-6 dishes for this size)

# Recommendation Strategy
- Prioritize 點心 and 冷菜 categories
- Avoid recommending 宮保雞丁 (frequently rejected)
- Suggest 小籠包 if available (high acceptance rate)
```

**效果**: Gemini 可以基於真實歷史數據做出更精準的推薦

---

### 場景 2：即時換菜候選池優化

**使用者換菜請求**:
```
Original: "宮保雞丁" (熱菜, NT$280)
```

**RAG 查詢**:
```python
# 查詢使用者的菜品偏好
user_preferences = get_user_dish_preferences(user_id)

# 過濾條件
1. 同類別（熱菜）
2. 價格相近（NT$250-350）
3. 使用者從未拒絕過（implicit_score >= 0）
4. 評分較高（explicit_score >= 4 或無評分）

# 候選菜品排序
candidates = [
  {"dish_name": "糖醋魚", "score": 0.92},  // 高分：被選擇 5 次，從未拒絕
  {"dish_name": "紅燒茄子", "score": 0.88},
  {"dish_name": "炒空心菜", "score": 0.85}
]
```

**效果**: 推薦使用者更可能喜歡的替代菜品，減少換菜次數

---

### 場景 3：個人化搜尋與推薦排序

**使用者搜尋**: "台北中式餐廳"

**RAG 增強排序**:
```python
# 基礎排序：評分、距離、價格
base_ranking = get_restaurants_by_location("台北", cuisine_type="中式餐館")

# RAG 增強：使用者歷史偏好
user_history = {
  "visited_restaurants": ["鼎泰豐", "添好運", "金蓬萊"],
  "favorite_price_range": (300, 600),
  "preferred_ambiance": ["家庭友善", "有包廂"]
}

# 重新排序
for restaurant in base_ranking:
  score = base_score
  if restaurant.avg_price in user_history["favorite_price_range"]:
    score += 0.2
  if restaurant.has_private_room and "有包廂" in user_history["preferred_ambiance"]:
    score += 0.15
  if restaurant in similar_to(user_history["visited_restaurants"]):
    score += 0.1

# 最終推薦列表：符合使用者歷史偏好的餐廳排在前面
```

---

### 場景 4：智能預算建議

**使用者輸入**:
```
Party size: 4
Budget: Not specified
```

**RAG 查詢歷史數據**:
```python
user_budget_history = get_user_budget_patterns(user_id)

# 分析結果
{
  "avg_budget_per_person_for_4_people": 520,
  "typical_total_budget": 2080,
  "budget_distribution": {
    "min": 1600,
    "median": 2000,
    "max": 2500
  }
}

# 系統建議
"Based on your previous orders, we recommend a budget of NT$2,000 (NT$500 per person) for 4 people."
```

---

## 📐 實作步驟建議

### 階段 1：基礎追蹤（立即實作）✅
1. ✅ 新增 `/v2/recommendations/{id}/swap` API
2. ✅ 新增 `/v2/recommendations/{id}/finalize` API
3. ✅ 建立 Firestore `sessions` collection
4. ✅ 記錄換菜行為與最終選擇

### 階段 2：偏好學習（1-2 週後）⏳
1. ⏳ 實作隱式評分機制
2. ⏳ 建立 `preferences` collection
3. ⏳ 定期批次更新使用者偏好統計

### 階段 3：RAG 整合（1 個月後）⏳
1. ⏳ 建立 Vector Database（Pinecone / Weaviate）
2. ⏳ 將使用者行為向量化
3. ⏳ 實作 RAG 查詢邏輯
4. ⏳ 整合至 Gemini prompt

---

## 🎯 預期效果

### 短期（1-2 週）
- ✅ 記錄完整的使用者互動歷史
- ✅ 了解使用者換菜的頻率與原因
- ✅ 分析哪些菜品最受歡迎 / 最常被拒絕

### 中期（1-2 個月）
- ⏳ 推薦準確度提升 15-20%（減少換菜次數）
- ⏳ 使用者對推薦的滿意度提升
- ⏳ 個人化程度提升（基於歷史數據）

### 長期（3-6 個月）
- ⏳ 完整的個人化推薦引擎
- ⏳ 預測使用者偏好（主動推薦）
- ⏳ 跨餐廳的偏好遷移學習

---

## ⚠️ 隱私與資料保護注意事項

### GDPR / 個資法合規
1. ✅ 使用者必須同意資料追蹤（在註冊時明確告知）
2. ✅ 提供「刪除我的資料」功能
3. ✅ 資料加密儲存（Firestore 預設支援）
4. ✅ 匿名化處理（用於統計分析時移除個人識別資訊）

### 建議實作
```python
# 使用者資料管理 API
DELETE /v2/users/me/data  # 刪除所有個人資料
GET /v2/users/me/data     # 下載個人資料副本（資料可攜權）
PATCH /v2/users/me/privacy  # 調整隱私設定
```

---

## 📊 資料量估算

假設：
- 活躍使用者：1000 人
- 每人每月點餐：4 次
- 每次推薦 6 道菜
- 平均換菜 2 次

**每月資料量**:
```
1000 users × 4 orders × (6 dishes + 2 swaps) = 32,000 documents
每個 document 約 1 KB
總計：32 MB / 月

年度總計：約 384 MB
```

**Firestore 成本**（假設）:
- 寫入：32,000 次 × $0.18/100k = $0.06 / 月
- 儲存：0.384 GB × $0.18/GB = $0.07 / 月
- 總計：約 $0.13 / 月（極低成本）

---

## ✅ 總結

### 目前已有
- ✅ 使用者回饋（rating, comment, selected_items）
- ✅ 餐廳資料快取

### 建議新增（優先級 1）
- 🔴 換菜行為追蹤
- 🔴 最終點餐確認
- 🔴 完整的 session 記錄

### 未來 RAG 應用價值
- ✅ 個人化推薦準確度提升 15-20%
- ✅ 減少使用者換菜次數
- ✅ 更精準的預算與菜單規劃
- ✅ 跨餐廳的偏好學習

### 下一步行動
1. 實作 `/swap` 和 `/finalize` API
2. 前端整合追蹤機制
3. 累積 1-2 週數據後分析效果
