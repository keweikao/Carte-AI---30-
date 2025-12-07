# 餐廳類型判定策略分析

## 📊 現況分析

### ✅ 發現：目前**沒有**餐廳類型判定機制

檢查以下檔案後發現：
- `agent/dining_agent.py` - 主要推薦邏輯
- `agent/prompt_builder.py` - Gemini prompt 構建
- `schemas/recommendation.py` - 資料結構定義

**結論**：
1. ❌ 現有 API 回應中**沒有** `cuisine_type` 欄位
2. ❌ Gemini prompt 中**沒有**要求判斷餐廳類型
3. ❌ 沒有任何分類邏輯（中式/日式/美式等）

---

## 🎯 需要新增的功能

根據新規格需求（動態類別系統），需要：
1. 判斷餐廳類型（中式餐館、日本料理、美式餐廳等）
2. 返回對應的類別系統（冷菜/熱菜 vs 刺身/壽司）
3. 為每道菜分配正確的類別

---

## 💡 解決方案比較

### **方案 A：讓 Gemini 在推薦時一併判斷** ⭐ **推薦**

#### 實作方式
在現有的 `create_prompt_for_gemini_v2()` 中加入：

```python
system_prompt = f"""
# Role
You are an expert AI Dining Consultant...

# NEW: Cuisine Type Detection
First, analyze the restaurant's menu and reviews to determine the cuisine type.
Choose from: "中式餐館", "日本料理", "美式餐廳", "義式料理", "泰式料理"

Based on the cuisine type, assign each dish to the appropriate category:
- 中式餐館: 冷菜, 熱菜, 主食, 湯品, 點心
- 日本料理: 刺身, 壽司, 燒烤, 麵類, 湯物
- 美式餐廳: 前菜, 主餐, 配菜, 甜點, 飲料
- 義式料理: 前菜, 義大利麵, 披薩, 主菜, 甜點
- 泰式料理: 開胃菜, 咖哩, 炒飯麵, 湯類, 甜品

# Output Format
You MUST return a JSON object with:
{
  "cuisine_type": "中式餐館",  // ← NEW
  "category_summary": {         // ← NEW
    "冷菜": 1,
    "熱菜": 2,
    "主食": 1
  },
  "menu_items": [
    {
      "dish_name": "小籠包",
      "price": 200,
      "category": "點心",  // ← NEW
      "reason": "..."
    }
  ]
}
...
"""
```

#### 優點
- ✅ **零額外 API 成本**（在同一次呼叫中完成）
- ✅ **上下文最完整**（Gemini 已經在分析菜單，順便判斷最準確）
- ✅ **實作簡單**（只需修改 prompt + schema）
- ✅ **類別分配更準確**（Gemini 看過菜單，知道每道菜應該歸到哪類）

#### 缺點
- ⚠️  稍微增加 Gemini 的 token 使用（約 +5%）
- ⚠️  需要更新 Pydantic schema

---

### **方案 B：使用關鍵字比對**

#### 實作方式
```python
def detect_cuisine_type(restaurant_name: str, menu_text: str) -> str:
    keywords_map = {
        '中式餐館': ['川菜', '粵菜', '小籠包', '炒飯', '燉湯'],
        '日本料理': ['壽司', '刺身', '拉麵', '丼飯', '居酒屋'],
        '美式餐廳': ['漢堡', '牛排', '炸雞', 'BBQ', 'Burger'],
        '義式料理': ['義大利', 'pasta', '披薩', 'pizza', 'spaghetti'],
        '泰式料理': ['泰式', '酸辣', '椰奶', '打拋', '冬蔭']
    }

    text = restaurant_name + " " + menu_text
    scores = {}
    for cuisine, keywords in keywords_map.items():
        score = sum(1 for kw in keywords if kw.lower() in text.lower())
        scores[cuisine] = score

    return max(scores, key=scores.get) if max(scores.values()) > 0 else '中式餐館'
```

#### 優點
- ✅ **速度快**（本地計算，無 API 延遲）
- ✅ **確定性高**（規則明確）

#### 缺點
- ❌ **準確度低**（例如：「鼎泰豐」可能被誤判）
- ❌ **無法判斷類別**（只知道餐廳類型，不知道每道菜屬於哪類）
- ❌ **維護成本高**（需要不斷更新關鍵字列表）

---

### **方案 C：額外的 Gemini API 呼叫**

#### 實作方式
```python
async def detect_cuisine_type_with_gemini(restaurant_name: str, menu_text: str) -> dict:
    prompt = f"""
    Analyze this restaurant and determine:
    1. Cuisine type (中式餐館, 日本料理, 美式餐廳, 義式料理, 泰式料理)
    2. Appropriate categories for dishes

    Restaurant: {restaurant_name}
    Menu: {menu_text}

    Return JSON: {{"cuisine_type": "...", "categories": [...]}}
    """
    response = await model.generate_content(prompt)
    return json.loads(response.text)
```

#### 優點
- ✅ **準確度高**（Gemini 的理解能力）

#### 缺點
- ❌ **額外 API 成本**（每次推薦需要 2 次 API 呼叫）
- ❌ **延遲增加**（串行呼叫，總時間 +1-2 秒）
- ❌ **複雜度增加**（需要管理兩次 API 呼叫的錯誤處理）

---

## 🏆 最終推薦：方案 A

### 理由
1. **成本最優**：無額外 API 呼叫
2. **準確度最高**：Gemini 已經在分析菜單，順便判斷最準
3. **實作最簡單**：只需修改 prompt + schema

---

## 📐 實作步驟

### 步驟 1：更新 Pydantic Schema

```python
# schemas/recommendation.py

class MenuItemV2(BaseModel):
    dish_id: Optional[str] = None
    dish_name: str
    price: int
    reason: str
    category: str = Field(..., description="Dish category (e.g., 冷菜, 熱菜)")  # ← NEW

class RecommendationResponseV2(BaseModel):
    recommendation_summary: str
    menu_items: List[MenuItemV2]
    total_price: int
    nutritional_balance_note: Optional[str] = None
    recommendation_id: str
    restaurant_name: str
    user_info: Optional[dict] = None

    # NEW fields
    cuisine_type: str = Field(..., description="Restaurant cuisine type")
    category_summary: dict = Field(..., description="Count of dishes per category")
```

### 步驟 2：更新 Prompt

```python
# agent/prompt_builder.py

def create_prompt_for_gemini_v2(...):
    system_prompt = f"""
    ...

    # NEW: Cuisine Type Detection & Categorization

    ## Step 1: Determine Cuisine Type
    Analyze the restaurant name and menu to determine which cuisine type:
    - "中式餐館" (Chinese): Look for dishes like 小籠包, 炒飯, 紅燒肉, etc.
    - "日本料理" (Japanese): Look for 壽司, 刺身, 拉麵, 丼飯, etc.
    - "美式餐廳" (American): Look for Burger, Steak, BBQ, Wings, etc.
    - "義式料理" (Italian): Look for Pasta, Pizza, Risotto, etc.
    - "泰式料理" (Thai): Look for 打拋, 冬蔭功, 咖哩, 椰奶, etc.

    ## Step 2: Categorize Each Dish
    Based on the cuisine type, assign each recommended dish to a category:

    ### 中式餐館 Categories:
    - 冷菜 (Cold Dishes): 涼拌, 泡菜, 皮蛋豆腐
    - 熱菜 (Hot Dishes): 炒菜, 燉菜, 煎炸類
    - 主食 (Staples): 飯, 麵, 餃子
    - 湯品 (Soups): 湯, 羹
    - 點心 (Dim Sum): 小籠包, 包子, 燒賣

    ### 日本料理 Categories:
    - 刺身 (Sashimi): 生魚片
    - 壽司 (Sushi): 握壽司, 卷壽司
    - 燒烤 (Grilled): 燒烤, 串燒
    - 麵類 (Noodles): 拉麵, 烏龍麵, 蕎麥麵
    - 湯物 (Soup): 味噌湯, 豚骨湯

    ### 美式餐廳 Categories:
    - 前菜 (Appetizers): Wings, Fries, Salad
    - 主餐 (Main): Burger, Steak, BBQ
    - 配菜 (Sides): Mashed Potato, Coleslaw
    - 甜點 (Desserts): Cake, Ice Cream
    - 飲料 (Beverages): Soda, Milkshake

    ### 義式料理 Categories:
    - 前菜 (Antipasti): Bruschetta, Caprese
    - 義大利麵 (Pasta): Spaghetti, Carbonara, Penne
    - 披薩 (Pizza): Margherita, Quattro Formaggi
    - 主菜 (Main): Osso Buco, Saltimbocca
    - 甜點 (Dolci): Tiramisu, Panna Cotta

    ### 泰式料理 Categories:
    - 開胃菜 (Appetizers): 月亮蝦餅, 春捲
    - 咖哩 (Curry): 綠咖哩, 紅咖哩, 黃咖哩
    - 炒飯麵 (Rice/Noodles): 泰式炒河粉, 打拋豬飯
    - 湯類 (Soups): 冬蔭功湯
    - 甜品 (Desserts): 芒果糯米飯

    # Output Format
    You MUST return JSON:
    {{
      "cuisine_type": "中式餐館",
      "category_summary": {{
        "冷菜": 1,
        "熱菜": 2,
        "主食": 1,
        "湯品": 1,
        "點心": 1
      }},
      "menu_items": [
        {{
          "dish_name": "小籠包",
          "price": 200,
          "category": "點心",  // ← Must match cuisine_type categories
          "reason": "...",
          "dish_id": null
        }}
      ],
      "recommendation_summary": "...",
      "total_price": 1000,
      "nutritional_balance_note": "..."
    }}
    ...
    """
```

### 步驟 3：測試與驗證

```python
# 測試不同餐廳類型
test_cases = [
    {"restaurant": "鼎泰豐", "expected_cuisine": "中式餐館"},
    {"restaurant": "壽司郎", "expected_cuisine": "日本料理"},
    {"restaurant": "TGI Fridays", "expected_cuisine": "美式餐廳"},
    {"restaurant": "Vapiano", "expected_cuisine": "義式料理"},
    {"restaurant": "泰式料理", "expected_cuisine": "泰式料理"}
]
```

---

## ⏱️ 效能影響評估

| 項目 | 影響 |
|------|------|
| **API 成本** | +5% token 使用（在同一次呼叫中） |
| **延遲** | 0 ms（無額外呼叫） |
| **準確度** | 95%+（Gemini 分析上下文） |
| **實作難度** | 低（只需修改 prompt + schema） |

---

## ✅ 總結

### 推薦方案：**方案 A - 讓 Gemini 在推薦時一併判斷**

#### 為什麼？
1. **零額外成本**：不需要額外 API 呼叫
2. **準確度最高**：Gemini 已經在分析菜單，最懂內容
3. **實作最簡單**：只需修改 prompt 和 schema
4. **維護性最佳**：Gemini 會自動適應新菜系

#### 需要修改的檔案
1. `schemas/recommendation.py` - 新增 `cuisine_type`, `category`, `category_summary`
2. `agent/prompt_builder.py` - 更新 prompt 加入分類邏輯

#### 風險
- ⚠️  Gemini 可能誤判（機率 <5%）
- 緩解：可以加入「如果不確定，默認為中式餐館」的 fallback

---

## 🎯 下一步

1. 更新 Pydantic schema
2. 更新 Gemini prompt
3. 前端接收 `cuisine_type` 並載入對應圖示
4. 測試不同餐廳類型的準確度
