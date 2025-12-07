# 規格文件：數量顯示功能 (Quantity Display)

## 1. 需求背景

### 使用者問題
最終使用者可能會用推薦結果跟餐廳店員點餐，但目前系統只顯示菜名和價格，沒有顯示**應該點幾份**，導致使用者不知道如何下單。

### 使用者回饋（原文）
> "還有一個問題，因為最終使用者可能會用這個跟店員點餐，所以其實需要加上數量"

### 目標
讓推薦結果明確顯示每道菜的**點餐數量**，使用者可以直接拿著菜單跟店員說：
- "小籠包 2 份"
- "宮保雞丁 1 份"
- "白飯 3 碗"

---

## 2. 功能範圍

### 2.1 核心功能
- ✅ **後端計算數量**：AI 根據用餐模式和人數計算合理的點餐數量
- ✅ **前端顯示數量**：推薦頁面和最終菜單頁面都顯示數量
- ✅ **價格計算調整**：顯示總價（單價 × 數量）

### 2.2 不包含的功能
- ❌ 使用者手動調整數量（未來功能）
- ❌ 數量建議提示（例如：「建議點 2 份會更適合」）
- ❌ 庫存檢查

---

## 3. 數量計算規則

### 3.1 多人分享模式 (Shared Style)

**原則**：一桌共享，主菜點 1 份大盤，小菜適量，主食每人 1 份

| 菜品類別 | 數量計算公式 | 範例（3 人） |
|---------|------------|------------|
| 主菜（熱菜、主餐、炒飯麵、咖哩等） | `1` | 宮保雞丁 x1 |
| 小菜/前菜（冷菜、配菜、開胃菜等） | `ceil(party_size / 2)` | 涼拌小黃瓜 x2 |
| 主食（米飯、麵類） | `party_size` | 白飯 x3 |
| 湯品 | `1` | 酸辣湯 x1 |
| 甜點 | `ceil(party_size / 2)` | 提拉米蘇 x2 |

**ceil() 說明**：
- 3 人 → ceil(3/2) = 2 份
- 4 人 → ceil(4/2) = 2 份
- 5 人 → ceil(5/2) = 3 份

### 3.2 個人套餐模式 (Individual Style)

**原則**：每人各自點餐，所有菜品都是 `人數` 份

| 菜品類別 | 數量計算公式 | 範例（3 人） |
|---------|------------|------------|
| 所有菜品 | `party_size` | 牛肉麵 x3 |

---

## 4. UI/UX 規格

### 4.1 推薦頁面 (recommendation page)

**菜品卡片 (DishCard)**：

```
┌─────────────────────────────────────┐
│ 🍜  小籠包 x2              NT$ 400  │
│                         2 × NT$ 200 │
│                                     │
│ "鼎泰豐招牌菜品，342 則評論..."      │
│ ⭐ 342 則好評                        │
│                                     │
│ [換一道]  [我要點]                   │
└─────────────────────────────────────┘
```

**顯示規則**：
- 數量 = 1：只顯示菜名和總價
  - `小籠包` / `NT$ 200`
- 數量 > 1：顯示菜名 x數量，總價，和計算細節
  - `小籠包 x2` / `NT$ 400` / `2 × NT$ 200`

**顏色**：
- 數量 x2 的文字使用 `caramel` 色（品牌色）突出顯示

### 4.2 最終菜單頁面 (menu page)

**菜品列表**：

```
推薦菜色

1. 小籠包 x2                    NT$ 400
   [點心]                       2 × NT$ 200
   鼎泰豐招牌菜品，342 則評論...
   342 則好評

2. 宮保雞丁                     NT$ 380
   [熱菜]
   經典川菜，麻辣香濃...
   156 則好評
```

**分享圖片 (Canvas)**：

```
┌────────────────────────────────┐
│  Carte AI 推薦菜單              │
│                                │
│  鼎泰豐                         │
│  中式餐館                        │
│                                │
│  總價: NT$ 1,500               │
│  人均: NT$ 500                 │
│                                │
│  推薦菜色                        │
│  1. 小籠包 x2      NT$ 400     │
│  2. 宮保雞丁       NT$ 380     │
│  3. 白飯 x3        NT$ 90      │
│                                │
│  由 Carte AI 智慧推薦 🍽️        │
└────────────────────────────────┘
```

---

## 5. 技術規格

### 5.1 資料結構

**Backend Schema** (`schemas/recommendation.py`):

```python
class MenuItemV2(BaseModel):
    dish_id: Optional[str] = Field(None, description="Corresponding menu item ID")
    dish_name: str = Field(..., description="Name of the dish")
    price: int = Field(..., description="Price of the dish")
    quantity: int = Field(..., description="Quantity of this dish to order", ge=1)  # 新增欄位
    reason: str = Field(..., description="Reason for recommending this dish")
    category: str = Field(..., description="Dish category (e.g., 冷菜, 熱菜, 刺身, 壽司)")
    review_count: Optional[int] = Field(None, description="Number of reviews mentioning this dish")
```

**Frontend Type** (`frontend/src/types/index.ts`):

```typescript
export interface MenuItem {
  dish_id: string | null;
  dish_name: string;
  price: number;
  quantity: number;  // 新增欄位
  category: string;
  reason: string;
  review_count?: number;
  price_estimated?: boolean;
}
```

### 5.2 AI Prompt 修改

**位置**：`agent/prompt_builder.py` - Section 4

**新增內容**：

```markdown
## 4. Portion Size, Quantity & Satiety Check

### Quantity Calculation (MANDATORY for every dish)
Every dish MUST include a `quantity` field indicating how many portions to order:

- **Shared Style**:
  - **Main Dishes** (熱菜, 主菜, 主餐, 炒飯麵, 咖哩, etc.): `quantity = 1`
  - **Small Dishes / Sides** (冷菜, 前菜, 配菜, 開胃菜, etc.): `quantity = ceil(Party_Size / 2)`
  - **Staples** (主食, 米飯, 麵類, etc.): `quantity = Party_Size`
  - **Soups** (湯品, 湯類, 湯物): `quantity = 1`
  - **Desserts** (甜點, 甜品, Dolci): `quantity = ceil(Party_Size / 2)`

- **Individual Style**:
  - **All dishes**: `quantity = Party_Size`

**Examples:**
- Party of 3, Shared Style:
  - "宮保雞丁" (main): quantity = 1
  - "涼拌小黃瓜" (cold dish): quantity = 2 (ceil(3/2))
  - "白飯" (staple): quantity = 3

- Party of 4, Individual Style:
  - "牛肉麵" (main): quantity = 4
  - "小籠包" (appetizer): quantity = 4
```

### 5.3 前端組件修改

**DishCard.tsx**：
- 顯示 `{dish.dish_name} {quantity > 1 && <span>x{quantity}</span>}`
- 價格顯示 `NT$ {price * quantity}`
- 當 quantity > 1 時顯示細節 `{quantity} × NT$ {price}`

**menu/page.tsx**：
- 菜品列表顯示數量
- Canvas 圖片包含數量資訊
- 總價計算使用 `price * quantity`

---

## 6. 邊界案例 (Edge Cases)

### 6.1 單人用餐

**情境**：1 人，多人分享模式
**處理**：
- 主菜：quantity = 1 ✅
- 小菜：ceil(1/2) = 1 ✅
- 主食：quantity = 1 ✅

**結果**：符合邏輯

### 6.2 大團體用餐

**情境**：10 人，多人分享模式
**處理**：
- 主菜：quantity = 1（可能不夠，但這是 AI 根據餐廳份量決定）
- 小菜：ceil(10/2) = 5
- 主食：quantity = 10

**潛在問題**：主菜 1 份可能不夠 10 人吃
**解決方案**：
- 短期：信任 AI 判斷（AI 可以根據餐廳資訊調整）
- 長期：在 prompt 中加入「若人數 > 6，主菜可考慮點 2 份」

### 6.3 餐廳小份量

**情境**：Tapas、Dim Sum 等小份量餐廳
**處理**：
- Prompt 已包含「如果餐廳以小份量著稱，建議增加數量或菜品數」
- AI 可以自行調整 quantity

### 6.4 估價菜品

**情境**：某些菜品沒有價格資料，使用估價
**處理**：
- quantity 欄位仍然顯示
- 總價 = 估價 × quantity
- 顯示「估價」標籤

---

## 7. 測試計畫

### 7.1 單元測試（未實作，但應該有）

**Backend**：
```python
def test_quantity_shared_mode_3_people():
    # 測試 3 人分享模式的數量計算
    assert calculate_quantity("熱菜", party_size=3, mode="Shared") == 1
    assert calculate_quantity("冷菜", party_size=3, mode="Shared") == 2
    assert calculate_quantity("主食", party_size=3, mode="Shared") == 3

def test_quantity_individual_mode():
    # 測試個人模式
    assert calculate_quantity("任何類別", party_size=4, mode="Individual") == 4
```

**Frontend**：
```typescript
describe('DishCard quantity display', () => {
  it('should show quantity when > 1', () => {
    const item = { dish_name: '小籠包', price: 200, quantity: 2 };
    // 預期顯示 "小籠包 x2" 和 "NT$ 400"
  });

  it('should hide quantity when = 1', () => {
    const item = { dish_name: '小籠包', price: 200, quantity: 1 };
    // 預期顯示 "小籠包" 和 "NT$ 200"
  });
});
```

### 7.2 整合測試

**測試案例 1：3 人分享模式**
- 輸入：鼎泰豐，3 人，分享模式，預算 500/人
- 預期：
  - 主菜 x1
  - 小菜 x2
  - 主食 x3
  - 總價正確計算

**測試案例 2：2 人個人模式**
- 輸入：拉麵店，2 人，個人模式，預算 300/人
- 預期：所有菜品 x2

**測試案例 3：單人用餐**
- 輸入：咖啡廳，1 人，分享模式，預算 200
- 預期：所有數量 = 1

### 7.3 手動測試檢查表

- [ ] 推薦頁面：數量 > 1 時顯示「x數量」
- [ ] 推薦頁面：總價 = 單價 × 數量
- [ ] 推薦頁面：計算細節顯示正確
- [ ] 最終菜單頁面：數量顯示正確
- [ ] 分享圖片：包含數量資訊
- [ ] 價格摘要：總價計算正確（sum of price × quantity）
- [ ] 不同用餐模式：分享 vs 個人的數量邏輯正確
- [ ] 不同人數：1 人、3 人、5 人、10 人測試

---

## 8. 效益評估

### 8.1 使用者體驗改善

**改善前**：
```
使用者：「請給我你推薦的菜單」
店員：「好的，小籠包、宮保雞丁、白飯」
使用者：「各要幾份？」（困惑）
```

**改善後**：
```
使用者：「小籠包 2 份、宮保雞丁 1 份、白飯 3 碗」
店員：「好的！」（順暢下單）
```

### 8.2 預期成效

- ✅ **減少溝通成本**：使用者不用再猜測或詢問數量
- ✅ **提升點餐信心**：明確的數量讓使用者更敢使用推薦
- ✅ **避免點錯**：不會因為數量不對導致吃不飽或浪費
- ✅ **完整的點餐體驗**：從推薦到下單一氣呵成

### 8.3 可能風險

1. **AI 數量判斷不準**：
   - 風險：某些餐廳份量特別大或特別小
   - 緩解：在 prompt 中已加入份量判斷邏輯

2. **使用者習慣**：
   - 風險：有些使用者可能習慣自己調整數量
   - 緩解：未來可加入「調整數量」功能

---

## 9. 未來擴充方向

### 9.1 Phase 2 功能（未實作）

- [ ] **手動調整數量**：使用者可在推薦頁面調整數量
- [ ] **數量建議提示**：「建議 3 人點 2 份更適合」
- [ ] **智慧數量優化**：根據歷史點餐數據優化數量建議

### 9.2 Phase 3 功能（未實作）

- [ ] **餐廳份量資料庫**：記錄各餐廳的實際份量大小
- [ ] **使用者反饋學習**：「這次點的量太多/太少」→ 調整演算法
- [ ] **數量分組顯示**：「建議 2 人分享 1 份，3-4 人點 2 份」

---

## 10. 參考資料

- **使用者需求**：2025-11-27 對話記錄
- **相關文件**：
  - `project_foundation.md`：核心哲學
  - `agent/prompt_builder.py`：AI Prompt 邏輯
  - `schemas/recommendation.py`：資料結構定義

---

**文件版本**：1.0
**建立日期**：2025-11-27
**最後更新**：2025-11-27
**負責人**：AI Assistant (Claude)
