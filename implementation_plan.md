# Input 頁面 UX 優化實作計畫

## 1. 技術架構分析

### 1.1 現有架構
- **檔案位置**：`frontend/src/app/input/page.tsx`
- **框架**：Next.js 14 App Router + React
- **UI 庫**：shadcn/ui
- **狀態管理**：React useState
- **表單資料結構**：
  ```typescript
  {
    restaurant_name: string,
    people: number,
    budget: string,
    dietary_restrictions: string,  // 逗號分隔的字串
    mode: "sharing" | "individual",
    dish_count: number | null
  }
  ```

### 1.2 需要修改的區域
1. **頁面標題**：第 272 行附近的 `<h1>` 標籤
2. **預算類型選擇器**：第 330-345 行的按鈕組
3. **預算金額輸入**：第 352 行的 Slider 元件
4. **飲食偏好區塊**：需要找到相關區域
5. **返回按鈕**：頁面頂部導航區

---

## 2. 實作策略

### 2.1 修改順序（從簡單到複雜）
1. ✅ 標題文案修改（最簡單）
2. ✅ 返回按鈕新增（簡單）
3. ✅ 預算金額輸入優化（中等）
4. ✅ 預算類型選擇器視覺優化（中等）
5. ✅ 飲食偏好重新設計（最複雜，涉及資料結構）

### 2.2 資料結構變更評估

#### 飲食偏好選項變更
**現有選項** → **新選項**：
- `vegetarian` → `need_vegetarian_option`（需要素食選項）
- `seafood` → `more_seafood`（多點海鮮）
- 新增：`love_meat`（愛吃肉）
- 新增：`more_vegetables`（多蔬菜）
- 新增：`prefer_light`（偏好清淡）
- 新增：`can_eat_spicy`（能吃辣）
- 新增：`avoid_allergens`（避免過敏原）

**新增欄位**：
- `dietary_custom_note: string` - 自由輸入的特殊需求

#### 後端相容性分析
- **問題**：後端 API 是否能處理新的飲食偏好選項？
- **方案 A（保守）**：前端收集新選項，但轉換成舊格式傳給後端
- **方案 B（激進）**：直接傳新格式，需要修改後端
- **建議**：先採用方案 A，避免破壞現有功能

#### 轉換邏輯（方案 A）
```typescript
// 新選項 → 舊格式對應
const dietaryMapping = {
  'love_meat': 'meat',
  'more_seafood': 'seafood',
  'need_vegetarian_option': 'vegetarian',
  'more_vegetables': 'healthy',
  'prefer_light': 'healthy',
  'can_eat_spicy': 'spicy',
  'avoid_allergens': '' // 特殊處理
}

// 如果有自訂需求，附加到現有格式
if (dietary_custom_note) {
  // 可能需要透過其他欄位傳遞，或暫時忽略
}
```

---

## 3. 詳細實作步驟

### 3.1 標題優化
**檔案**：`frontend/src/app/input/page.tsx`

**修改位置**：搜尋「客製化你的餐點」

**程式碼變更**：
```tsx
// 修改前
<h1 className="...">客製化你的餐點</h1>

// 修改後
<h1 className="...">開啟你的美食探索之旅</h1>
```

---

### 3.2 返回按鈕新增
**位置**：頁面左上角，可能在 header 區域

**設計**：
```tsx
<Button
  variant="ghost"
  onClick={() => router.back()}
  className="gap-2"
  aria-label="返回上一頁"
>
  <ArrowLeft className="w-4 h-4" />
  返回
</Button>
```

**注意事項**：
- 確認是否已經有 header 區域，如果沒有需要建立
- 確保響應式設計（小螢幕上可能只顯示圖示）

---

### 3.3 預算類型選擇器視覺優化

**修改目標**：
- 增加 hover 效果
- 加強未選中狀態的視覺提示
- 提升可點擊性的感知

**程式碼變更**（第 330-345 行附近）：
```tsx
// 修改前
<button
  className={`px-2 sm:px-3 py-1 text-xs rounded-md transition-all ${
    budgetType === "person"
      ? "bg-white shadow-sm text-foreground font-medium"
      : "text-muted-foreground"
  }`}
  onClick={() => setBudgetType("person")}
>
  每人(客單)
</button>

// 修改後
<button
  className={`px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${
    budgetType === "person"
      ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary"
      : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"
  }`}
  onClick={() => setBudgetType("person")}
  aria-label="選擇每人預算模式"
  aria-pressed={budgetType === "person"}
>
  <div className="flex items-center gap-2">
    <User className="w-4 h-4" />
    每人(客單)
  </div>
</button>
```

**需要新增的 icon**：
```tsx
import { User, Users } from "lucide-react";
```

---

### 3.4 預算金額輸入優化

**目標**：
- 移除預設值 0
- 增加 placeholder
- 改善輸入框視覺

**修改位置**：數字輸入框

**程式碼變更**：
```tsx
// 搜尋 type="number" 的 input
<input
  type="number"
  className="..."
  value={formData.budget === "0" ? "" : formData.budget}
  onChange={(e) => updateData("budget", e.target.value)}
  placeholder="例如：500"
  min="0"
/>
```

**Slider 預設值調整**：
```tsx
// 修改前
value={[Number(formData.budget) || (budgetType === 'person' ? 500 : 2000)]}

// 修改後
value={[Number(formData.budget) || 0]}
// 當值為 0 時，顯示起始位置但不顯示金額
```

---

### 3.5 飲食偏好重新設計

**這是最複雜的部分，需要：**
1. 修改選項內容
2. 新增自由輸入框
3. 處理資料轉換（新格式 → 舊格式）

#### Step 1: 定義新選項
```tsx
const dietaryOptions = [
  {
    id: 'love_meat',
    label: '愛吃肉',
    description: '多點肉類料理',
    legacy: 'meat'
  },
  {
    id: 'more_seafood',
    label: '多點海鮮',
    description: '偏好海鮮類',
    legacy: 'seafood'
  },
  {
    id: 'need_vegetarian_option',
    label: '需要素食選項',
    description: '有人吃素',
    legacy: 'vegetarian'
  },
  {
    id: 'more_vegetables',
    label: '多蔬菜',
    description: '增加蔬菜比例',
    legacy: 'healthy'
  },
  {
    id: 'prefer_light',
    label: '偏好清淡',
    description: '少油少鹽',
    legacy: 'healthy'
  },
  {
    id: 'can_eat_spicy',
    label: '能吃辣',
    description: '可以有辣味菜',
    legacy: 'spicy'
  },
  {
    id: 'avoid_allergens',
    label: '避免過敏原',
    description: '海鮮/堅果等',
    legacy: ''
  },
];
```

#### Step 2: 新增狀態管理
```tsx
const [dietaryPreferences, setDietaryPreferences] = useState<string[]>([]);
const [dietaryCustomNote, setDietaryCustomNote] = useState<string>("");
```

#### Step 3: UI 實作
```tsx
<div className="space-y-3">
  <Label className="text-base">用餐風格偏好</Label>
  <p className="text-sm text-muted-foreground">可多選</p>

  <div className="grid grid-cols-2 gap-2">
    {dietaryOptions.map(option => (
      <button
        key={option.id}
        type="button"
        className={`p-3 rounded-lg border-2 transition-all text-left ${
          dietaryPreferences.includes(option.id)
            ? 'border-primary bg-primary/5'
            : 'border-border hover:border-primary/50'
        }`}
        onClick={() => {
          setDietaryPreferences(prev =>
            prev.includes(option.id)
              ? prev.filter(id => id !== option.id)
              : [...prev, option.id]
          )
        }}
      >
        <div className="font-medium">{option.label}</div>
        <div className="text-xs text-muted-foreground">{option.description}</div>
      </button>
    ))}
  </div>

  {/* 自由輸入框 */}
  <div className="mt-4">
    <Textarea
      placeholder="還有什麼特別需求都可以告訴我，例如：不吃牛、怕過敏、偏好當季食材..."
      value={dietaryCustomNote}
      onChange={(e) => setDietaryCustomNote(e.target.value)}
      className="min-h-[80px]"
    />
  </div>
</div>
```

#### Step 4: 資料轉換（提交時）
```tsx
const handleSubmit = () => {
  // 轉換新選項為舊格式
  const legacyDietary = dietaryPreferences
    .map(id => {
      const option = dietaryOptions.find(opt => opt.id === id);
      return option?.legacy || '';
    })
    .filter(v => v)
    .join(',');

  // 如果有自訂需求，暫時附加到現有格式（或存到其他地方）
  // 這部分需要確認後端如何處理

  const params = new URLSearchParams({
    restaurant: formData.restaurant_name,
    people: formData.people.toString(),
    budget: formData.budget,
    dietary: legacyDietary, // 使用轉換後的舊格式
    mode: formData.mode,
    budget_type: budgetType,
    ...(formData.dish_count && { dish_count: formData.dish_count.toString() })
  });

  router.push(`/recommendation?${params.toString()}`);
};
```

---

## 4. 測試計畫

### 4.1 功能測試
- [ ] 標題正確顯示
- [ ] 返回按鈕點擊後正確返回
- [ ] 預算類型選擇器切換正常
- [ ] 預算類型選擇器 hover 效果正確
- [ ] 預算金額輸入框 placeholder 正確顯示
- [ ] 預算金額輸入框與 slider 雙向同步
- [ ] 飲食偏好多選正常運作
- [ ] 飲食偏好自由輸入框正常
- [ ] 資料轉換邏輯正確（新格式 → 舊格式）
- [ ] 提交後導航正常

### 4.2 視覺測試
- [ ] 響應式設計在手機上正常
- [ ] 響應式設計在平板上正常
- [ ] 響應式設計在桌面上正常
- [ ] 所有 hover 效果正常
- [ ] 所有 focus 效果正常
- [ ] 顏色對比符合無障礙標準

### 4.3 整合測試
- [ ] 與 recommendation 頁面整合正常
- [ ] 後端 API 接收資料正確
- [ ] 建置無錯誤

---

## 5. 風險評估

### 5.1 技術風險
- **飲食偏好資料格式變更**：可能影響後端
  - **緩解措施**：使用轉換邏輯，保持後端相容性

### 5.2 UX 風險
- **使用者可能不理解新的飲食偏好選項**
  - **緩解措施**：提供清楚的說明文字（description）

### 5.3 效能風險
- **新增元件可能影響載入速度**
  - **緩解措施**：保持元件輕量，避免過度渲染

---

## 6. 待辦事項與時程

### Phase 1: 簡單修改（優先）
1. 標題文案修改
2. 返回按鈕新增
3. 預算金額輸入優化

### Phase 2: 視覺優化
4. 預算類型選擇器視覺優化

### Phase 3: 複雜功能
5. 飲食偏好重新設計

### Phase 4: 測試與修正
6. 功能測試
7. 視覺測試
8. 整合測試
9. Bug 修正

---

## 7. 備註

### 7.1 需要新增的 imports
```tsx
import { ArrowLeft, User, Users } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
```

### 7.2 需要確認的問題
1. 後端是否能處理新的飲食偏好格式？如果不行，需要使用轉換邏輯
2. `dietaryCustomNote` 欄位應該如何傳遞給後端？
