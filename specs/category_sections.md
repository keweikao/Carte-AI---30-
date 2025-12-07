# 規格文件：類別分組顯示功能 (Category Sections)

## 1. 需求背景

### 使用者問題
目前推薦頁面的菜品是以列表方式平鋪顯示，使用者無法快速了解：
1. 推薦了哪些類別的菜品
2. 是否缺少某些重要類別（例如：沒有湯品、沒有甜點）
3. 整體推薦的結構是否合理

### 使用者回饋（原文）
> "現在既然有作品像分類，我建議呈現的時候也應該呈現出來，可以讓使用者知道我們的推薦有沒有缺少的，我覺得直接建立類別的 section，只是 section 名稱會根據不同餐廳型態改變，沒出現的類別就不顯示，我覺得這樣更清楚。"

### 目標
將推薦頁面改為**依類別分組顯示**，讓使用者一眼看出推薦結構，並能快速發現缺少的類別。

---

## 2. 功能範圍

### 2.1 核心功能
- ✅ **類別分組顯示**：將菜品依類別分組，每個類別為一個 Section
- ✅ **動態類別標題**：根據餐廳類型（中式、日式、美式等）顯示對應的類別名稱
- ✅ **類別圖示**：每個類別配上對應的 Emoji 圖示
- ✅ **類別統計**：顯示每個類別有幾道菜（例如：冷菜 (2)）
- ✅ **推薦摘要**：在頂部顯示整體推薦結構

### 2.2 不包含的功能
- ❌ 使用者手動調整類別順序
- ❌ 點擊類別標題展開/收合
- ❌ 類別篩選功能

---

## 3. UI/UX 規格

### 3.1 整體佈局

```
┌─────────────────────────────────────┐
│ [Header: Carte AI Logo + 使用者頭像]  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📊 為您推薦 5 道菜                    │
│ 冷菜 1 道 · 熱菜 2 道 · 主食 1 道     │
│ 湯品 1 道                            │
└─────────────────────────────────────┘

━━━━━━━━ 🥶 冷菜 (1) ━━━━━━━━

[菜品卡片 1]
[菜品卡片 2] (如果有多道)

━━━━━━━━ 🔥 熱菜 (2) ━━━━━━━━

[菜品卡片 3]
[菜品卡片 4]

━━━━━━━━ 🍚 主食 (1) ━━━━━━━━

[菜品卡片 5]

━━━━━━━━ 🍲 湯品 (1) ━━━━━━━━

[菜品卡片 6]

┌─────────────────────────────────────┐
│  💡 還想追加什麼嗎？(未來功能)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│     ✓ 還有 6 道菜未確認              │
└─────────────────────────────────────┘
```

### 3.2 推薦摘要 (Recommendation Summary)

**位置**：頁面頂部（Header 下方）

**設計**：
```tsx
<Card className="mb-6 p-4 bg-cream-100 border-caramel/20">
  <div className="text-center">
    <div className="flex items-center justify-center gap-2 mb-2">
      <span className="text-2xl">📊</span>
      <h2 className="text-lg font-semibold text-foreground">
        為您推薦 {totalDishes} 道菜
      </h2>
    </div>
    <p className="text-sm text-muted-foreground">
      冷菜 1 道 · 熱菜 2 道 · 主食 1 道 · 湯品 1 道
    </p>
  </div>
</Card>
```

**內容**：
- 總道數：`為您推薦 5 道菜`
- 類別摘要：`冷菜 1 道 · 熱菜 2 道 · 主食 1 道`（用 `·` 分隔）

### 3.3 類別標題 (Category Header)

**設計**：
```tsx
<div className="flex items-center justify-center my-6">
  <div className="flex items-center gap-2 px-4 py-2 bg-sage/10 rounded-full">
    <span className="text-xl">{categoryIcon}</span>
    <h3 className="text-md font-semibold text-sage-800">
      {categoryName} ({dishCount})
    </h3>
  </div>
</div>
```

**樣式**：
- 背景色：`bg-sage/10`（淺綠色，品牌色）
- 圓角：`rounded-full`（藥丸形狀）
- 文字顏色：`text-sage-800`（深綠色）
- 圖示大小：`text-xl`
- 置中顯示

**範例**：
- `🥶 冷菜 (1)`
- `🔥 熱菜 (2)`
- `🍚 主食 (1)`

### 3.4 類別圖示對應

#### 中式餐館
| 類別 | 圖示 | Emoji |
|------|------|-------|
| 冷菜 | 🥶 | `:cold_face:` |
| 熱菜 | 🔥 | `:fire:` |
| 主食 | 🍚 | `:cooked_rice:` |
| 點心 | 🥟 | `:dumpling:` |
| 湯品 | 🍲 | `:stew:` |

#### 日本料理
| 類別 | 圖示 | Emoji |
|------|------|-------|
| 刺身 | 🐟 | `:fish:` |
| 壽司 | 🍣 | `:sushi:` |
| 燒烤 | 🔥 | `:fire:` |
| 麵類 | 🍜 | `:ramen:` |
| 湯物 | 🍵 | `:tea:` |

#### 美式餐廳
| 類別 | 圖示 | Emoji |
|------|------|-------|
| 前菜 (Appetizers) | 🥗 | `:salad:` |
| 主餐 (Main) | 🍔 | `:burger:` |
| 配菜 (Sides) | 🍟 | `:fries:` |
| 甜點 (Desserts) | 🍰 | `:cake:` |
| 飲料 (Beverages) | 🥤 | `:cup_with_straw:` |

#### 義式料理
| 類別 | 圖示 | Emoji |
|------|------|-------|
| 前菜 (Antipasti) | 🧀 | `:cheese:` |
| 義大利麵 (Pasta) | 🍝 | `:spaghetti:` |
| 披薩 (Pizza) | 🍕 | `:pizza:` |
| 主菜 (Main) | 🥩 | `:steak:` |
| 甜點 (Dolci) | 🍰 | `:cake:` |

#### 泰式料理
| 類別 | 圖示 | Emoji |
|------|------|-------|
| 開胃菜 (Appetizers) | 🦐 | `:shrimp:` |
| 咖哩 (Curry) | 🍛 | `:curry:` |
| 炒飯麵 (Rice/Noodles) | 🍜 | `:ramen:` |
| 湯類 (Soups) | 🍲 | `:stew:` |
| 甜品 (Desserts) | 🥭 | `:mango:` |

### 3.5 類別順序

**排序邏輯**：依照用餐順序（前菜 → 主菜 → 主食 → 湯品 → 甜點）

#### 中式餐館順序
1. 冷菜
2. 熱菜
3. 主食
4. 點心
5. 湯品

#### 日本料理順序
1. 刺身
2. 壽司
3. 燒烤
4. 麵類
5. 湯物

#### 美式餐廳順序
1. 前菜 (Appetizers)
2. 主餐 (Main)
3. 配菜 (Sides)
4. 甜點 (Desserts)
5. 飲料 (Beverages)

**實作方式**：使用 `prompt_builder.py` 中已定義的 `category_order` 陣列。

---

## 4. 技術規格

### 4.1 資料結構

**現有資料**（無需修改後端）：

```typescript
interface RecommendationResponse {
  recommendation_id: string;
  restaurant_name: string;
  cuisine_type: string;  // "中式餐館", "日本料理", etc.
  total_price: number;
  items: DishSlotResponse[];
  category_summary: Record<string, number>;  // {"冷菜": 1, "熱菜": 2}
}

interface DishSlotResponse {
  category: string;  // "冷菜", "熱菜", etc.
  display: MenuItem;
  alternatives: MenuItem[];
}
```

### 4.2 前端資料轉換

**步驟 1：將 items 依類別分組**

```typescript
// 輸入：items (DishSlotResponse[])
// 輸出：Map<category, DishSlotResponse[]>

const groupedByCategory = items.reduce((acc, item) => {
  const category = item.category;
  if (!acc.has(category)) {
    acc.set(category, []);
  }
  acc.get(category)!.push(item);
  return acc;
}, new Map<string, DishSlotResponse[]>());
```

**步驟 2：依類別順序排序**

```typescript
// 從 prompt_builder.py 複製類別順序
const categoryOrder = {
  "中式餐館": ["冷菜", "熱菜", "主食", "點心", "湯品"],
  "日本料理": ["刺身", "壽司", "燒烤", "麵類", "湯物"],
  "美式餐廳": ["前菜", "主餐", "配菜", "甜點", "飲料"],
  // ...
};

const orderedCategories = categoryOrder[cuisineType].filter(cat =>
  groupedByCategory.has(cat)
);
```

**步驟 3：渲染分組**

```tsx
{orderedCategories.map(category => (
  <div key={category}>
    <CategoryHeader
      category={category}
      count={groupedByCategory.get(category)!.length}
      cuisineType={cuisineType}
    />
    {groupedByCategory.get(category)!.map(slot => (
      <DishCard key={slot.display.dish_name} {...slot} />
    ))}
  </div>
))}
```

### 4.3 組件設計

#### CategoryHeader 組件

```typescript
interface CategoryHeaderProps {
  category: string;        // "冷菜"
  count: number;          // 2
  cuisineType: string;    // "中式餐館"
}

function CategoryHeader({ category, count, cuisineType }: CategoryHeaderProps) {
  const icon = getCategoryIcon(category, cuisineType);

  return (
    <div className="flex items-center justify-center my-6">
      <div className="flex items-center gap-2 px-4 py-2 bg-sage/10 rounded-full">
        <span className="text-xl">{icon}</span>
        <h3 className="text-md font-semibold text-sage-800">
          {category} ({count})
        </h3>
      </div>
    </div>
  );
}
```

#### RecommendationSummary 組件

```typescript
interface RecommendationSummaryProps {
  totalDishes: number;
  categorySummary: Record<string, number>;
}

function RecommendationSummary({ totalDishes, categorySummary }: RecommendationSummaryProps) {
  const summaryText = Object.entries(categorySummary)
    .map(([cat, count]) => `${cat} ${count} 道`)
    .join(' · ');

  return (
    <Card className="mb-6 p-4 bg-cream-100 border-caramel/20">
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-2xl">📊</span>
          <h2 className="text-lg font-semibold text-foreground">
            為您推薦 {totalDishes} 道菜
          </h2>
        </div>
        <p className="text-sm text-muted-foreground">{summaryText}</p>
      </div>
    </Card>
  );
}
```

#### getCategoryIcon 輔助函數

```typescript
const categoryIcons: Record<string, Record<string, string>> = {
  "中式餐館": {
    "冷菜": "🥶",
    "熱菜": "🔥",
    "主食": "🍚",
    "點心": "🥟",
    "湯品": "🍲",
  },
  "日本料理": {
    "刺身": "🐟",
    "壽司": "🍣",
    "燒烤": "🔥",
    "麵類": "🍜",
    "湯物": "🍵",
  },
  // ...
};

function getCategoryIcon(category: string, cuisineType: string): string {
  return categoryIcons[cuisineType]?.[category] || "🍽️";
}
```

### 4.4 類別順序常數

**位置**：`frontend/src/constants/categories.ts`（新檔案）

```typescript
export const CATEGORY_ORDER: Record<string, string[]> = {
  "中式餐館": ["冷菜", "熱菜", "主食", "點心", "湯品"],
  "日本料理": ["刺身", "壽司", "燒烤", "麵類", "湯物"],
  "美式餐廳": ["前菜", "主餐", "配菜", "甜點", "飲料"],
  "義式料理": ["前菜", "義大利麵", "披薩", "主菜", "甜點"],
  "泰式料理": ["開胃菜", "咖哩", "炒飯麵", "湯類", "甜品"],
};

export const CATEGORY_ICONS: Record<string, Record<string, string>> = {
  "中式餐館": {
    "冷菜": "🥶",
    "熱菜": "🔥",
    "主食": "🍚",
    "點心": "🥟",
    "湯品": "🍲",
  },
  // ... (如上)
};
```

---

## 5. 邊界案例 (Edge Cases)

### 5.1 只有一個類別

**情境**：推薦結果只有「主食」（例如：拉麵店）

**處理**：
- 仍然顯示類別標題：`🍜 麵類 (1)`
- 推薦摘要：`為您推薦 1 道菜 · 麵類 1 道`

### 5.2 類別順序不在預設列表中

**情境**：AI 返回了一個未定義的類別（例如：`特色菜`）

**處理**：
- 顯示預設圖示：`🍽️ 特色菜 (1)`
- 排序：放在所有已知類別之後

### 5.3 沒有 category_summary

**情境**：後端返回的資料缺少 `category_summary` 欄位（向下相容）

**處理**：
- 從 `items` 手動計算 `category_summary`
```typescript
const categorySummary = items.reduce((acc, item) => {
  acc[item.category] = (acc[item.category] || 0) + 1;
  return acc;
}, {} as Record<string, number>);
```

### 5.4 未知的 cuisineType

**情境**：後端返回了未定義的餐廳類型（例如：`韓式料理`）

**處理**：
- 使用預設排序：依類別名稱的字母順序
- 使用預設圖示：`🍽️`

---

## 6. 測試計畫

### 6.1 視覺測試

- [ ] 類別標題顯示正確（圖示 + 名稱 + 數量）
- [ ] 類別標題樣式正確（置中、圓角、品牌色）
- [ ] 推薦摘要顯示正確
- [ ] 不同餐廳類型使用對應的圖示
- [ ] 類別順序符合用餐順序

### 6.2 功能測試

**測試案例 1：中式餐館（多類別）**
- 輸入：鼎泰豐，5 道菜（冷菜 1、熱菜 2、主食 1、湯品 1）
- 預期：
  - 推薦摘要：`為您推薦 5 道菜 · 冷菜 1 道 · 熱菜 2 道 · 主食 1 道 · 湯品 1 道`
  - 類別順序：冷菜 → 熱菜 → 主食 → 湯品
  - 圖示正確：🥶 冷菜、🔥 熱菜、🍚 主食、🍲 湯品

**測試案例 2：日式料理（單類別）**
- 輸入：拉麵店，1 道菜（麵類 1）
- 預期：
  - 推薦摘要：`為您推薦 1 道菜 · 麵類 1 道`
  - 類別標題：🍜 麵類 (1)

**測試案例 3：美式餐廳**
- 輸入：漢堡店，3 道菜（主餐 1、配菜 1、飲料 1）
- 預期：
  - 類別順序：主餐 → 配菜 → 飲料
  - 圖示：🍔 主餐、🍟 配菜、🥤 飲料

### 6.3 邊界測試

- [ ] 未知類別使用預設圖示 🍽️
- [ ] 未知餐廳類型使用預設排序
- [ ] 缺少 category_summary 時自動計算

---

## 7. 效益評估

### 7.1 使用者體驗改善

**改善前**：
```
[豬耳朵卡片]
[滷味拼盤卡片]
[牛肉麵卡片]
```
使用者：「不知道推薦了什麼類別，有沒有湯？有沒有甜點？」

**改善後**：
```
🥶 冷菜 (1)
[豬耳朵卡片]

🔥 熱菜 (1)
[滷味拼盤卡片]

🍜 麵類 (1)
[牛肉麵卡片]
```
使用者：「喔，原來有冷菜、熱菜、麵類，但沒有湯品和甜點。我可能需要追加。」

### 7.2 預期成效

- ✅ **提升透明度**：使用者清楚知道推薦結構
- ✅ **減少困惑**：不會懷疑「為什麼都推薦主食」
- ✅ **引導追加**：發現缺少的類別，主動追加（為需求 2 鋪路）
- ✅ **提升信任**：展示 AI 的推薦邏輯，增加可信度

---

## 8. 未來擴充方向

### 8.1 Phase 2 功能（追加點餐）

當使用者看到「缺少湯品」時，可以點擊「追加湯品」按鈕：

```
🥶 冷菜 (1)
🔥 熱菜 (1)
🍜 麵類 (1)

[缺少：🍲 湯品]  [+ 追加]
[缺少：🥟 點心]  [+ 追加]
```

### 8.2 Phase 3 功能（智慧建議）

AI 主動提示：
```
💡 您的推薦結構很均衡，但缺少湯品。
建議追加：酸辣湯 (NT$ 60) 或 玉米濃湯 (NT$ 50)
```

---

## 9. 參考資料

- **使用者需求**：2025-11-27 對話記錄
- **相關文件**：
  - `project_foundation.md`：核心哲學
  - `agent/prompt_builder.py`：類別定義和順序

---

**文件版本**：1.0
**建立日期**：2025-11-27
**最後更新**：2025-11-27
**負責人**：AI Assistant (Claude)
**狀態**：✅ 規格確認完成，待實作
