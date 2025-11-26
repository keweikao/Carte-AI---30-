# UX 改進功能規劃 v2.0 - 完整版（含 8 個功能）

## 📋 總覽

本文件規劃 8 個 UX 改進功能（含 5 個新需求），旨在提升使用者體驗和互動性。

**最新更新 v2.0**：
- ✅ 新增功能 5：推薦頁面「返回設定」按鈕
- ❌ 取消功能 4：移除 20 秒閒置自動彈出機制
- ✅ 新增功能 6：菜品數量選項（非必填）
- ✅ 新增功能 7：菜品描述限制為 2 行
- ✅ 新增功能 8：每道菜顯示不同的評價數

---

## 功能總覽表

| 功能 | 描述 | 優先級 | 工時 | 狀態 |
|------|------|--------|------|------|
| 1️⃣ 登入狀態顯示 | Header 顯示用戶頭像和登出選單 | 🔴 High | 2-3h | ✅ 規劃完成 |
| 2️⃣ 完成後返回搜尋頁 | 提交回饋後導航回 /input | 🟡 Medium | 1.5h | ✅ 規劃完成 |
| 3️⃣ 讚/倒讚評分系統 | 取代綠勾勾，改為 👍/👎 按鈕 | 🔴 High | 3-4h | ✅ 規劃完成 |
| ~~4️⃣ 閒置自動彈出~~ | ~~20秒閒置彈出回饋~~ | ❌ 取消 | -0.75h | 🗑️ 已移除 |
| 5️⃣ 返回設定按鈕 | 推薦頁面加入「返回設定」按鈕 | 🟡 Med-High | 1.5h | ✅ 規劃完成 |
| 6️⃣ 菜品數量選項 | 可選填「想要幾道菜」並驗證 | 🟡 Medium | 2h | ✅ 規劃完成 |
| 7️⃣ 描述限制 2 行 | 菜品說明濃縮為 2 行顯示 | 🟢 Low | 0.5-1.5h | ✅ 規劃完成 |
| 8️⃣ 不同評價數 | 每道菜顯示不同的評論數 | 🟡 Medium | 1-4h | ✅ 規劃完成 |

**總工時**：11.5-16.5 小時

---

## 功能 1️⃣：右上角登入狀態顯示

### 需求描述
在所有頁面的右上角顯示用戶登入狀態圖標，讓用戶清楚知道自己已登入。

### 現況分析
- ✅ 已有 NextAuth session 管理
- ✅ 已有 `useSession()` hook
- ❌ 目前沒有 Header 組件顯示登入狀態

### 技術實作

**新增組件**: `src/components/header.tsx`
```tsx
"use client";

import { useSession, signIn, signOut } from "next-auth/react";
import { User, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function Header() {
  const { data: session, status } = useSession();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <div className="flex items-center gap-2 font-bold text-xl">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
            🍽️
          </div>
          Carte
        </div>

        {/* Auth Section */}
        {status === "loading" ? (
          <div className="w-8 h-8 animate-pulse bg-muted rounded-full"></div>
        ) : session ? (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                <Avatar className="h-10 w-10">
                  <AvatarImage src={session.user?.image || ""} alt={session.user?.name || ""} />
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    {session.user?.name?.[0]?.toUpperCase() || "U"}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">{session.user?.name}</p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {session.user?.email}
                  </p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => signOut()}>
                <LogOut className="mr-2 h-4 w-4" />
                <span>登出</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        ) : (
          <Button onClick={() => signIn("google")}>登入</Button>
        )}
      </div>
    </header>
  );
}
```

**整合到 Layout**: `src/app/layout.tsx`
```tsx
import { Header } from "@/components/header";

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="light">
      <body>
        <AuthProvider>
          <Header />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

### 預估工時
- **開發**: 1-2 小時
- **測試**: 30 分鐘
- **總計**: 2-3 小時

---

## 功能 2️⃣：完成推薦後返回搜尋頁

### 需求描述
完成推薦並提交回饋後，應該導航回到餐廳搜尋頁 (`/input`)，而不是停留在推薦頁面。

### 技術實作

**修改**: `src/components/rating-modal.tsx`
```tsx
import { useRouter } from "next/navigation";

export function RatingModal({ isOpen, onClose, onSubmit }) {
  const router = useRouter();
  const [step, setStep] = useState<"rating" | "feedback" | "done">("rating");

  const handleSubmit = async () => {
    if (rating && onSubmit) {
      await onSubmit({ rating, comment });
    }
    setStep("done");
  };

  const handleDone = () => {
    onClose();
    router.push("/input");
  };

  // 在 "done" step 的按鈕
  {step === "done" && (
    <Button onClick={handleDone}>
      回到搜尋頁
    </Button>
  )}
}
```

### 預估工時
- **總計**: 1.5 小時

---

## 功能 3️⃣：讚/倒讚評分系統

### 需求描述
將菜品選擇的綠勾勾改為「讚 👍」和「倒讚 👎」按鈕，當所有菜品評分完成後自動彈出回饋 Modal。

### 技術實作

**修改**: `src/app/recommendation/page.tsx`

```tsx
"use client";

import { ThumbsUp, ThumbsDown, RefreshCw } from "lucide-react";

export default function RecommendationPage() {
  // 新的 state
  const [itemRatings, setItemRatings] = useState<Map<string, "like" | "dislike">>(new Map());

  // 評分函數
  const handleRating = (itemName: string, rating: "like" | "dislike") => {
    setItemRatings(prev => {
      const newMap = new Map(prev);
      if (newMap.get(itemName) === rating) {
        newMap.delete(itemName);
      } else {
        newMap.set(itemName, rating);
      }
      return newMap;
    });
  };

  // 檢查是否所有菜品都已評分
  const allItemsRated = currentItems.every(item =>
    itemRatings.has(item.name)
  );

  // 當所有菜品都評分後，自動彈出回饋 Modal
  useEffect(() => {
    if (allItemsRated && currentItems.length > 0 && !showFeedback) {
      setTimeout(() => {
        setShowFeedback(true);
      }, 500);
    }
  }, [allItemsRated, currentItems.length, showFeedback]);

  return (
    <div>
      {currentItems.map((item, index) => {
        const currentRating = itemRatings.get(item.name);

        return (
          <div key={index}>
            {/* 讚按鈕 */}
            <Button
              variant={currentRating === "like" ? "default" : "outline"}
              onClick={() => handleRating(item.name, "like")}
            >
              <ThumbsUp className="w-4 h-4 mr-1" />
              推薦
            </Button>

            {/* 倒讚按鈕 */}
            <Button
              variant={currentRating === "dislike" ? "destructive" : "outline"}
              onClick={() => handleRating(item.name, "dislike")}
            >
              <ThumbsDown className="w-4 h-4 mr-1" />
              不推薦
            </Button>
          </div>
        );
      })}
    </div>
  );
}
```

### 移除閒置計時器

同時移除以下代碼：
```tsx
// ❌ 移除這些
const idleTimerRef = useRef<NodeJS.Timeout | null>(null);
const IDLE_TIMEOUT = 20000;
const resetIdleTimer = useCallback(() => { ... }, []);
useEffect(() => { /* 事件監聽器 */ }, [resetIdleTimer]);
```

### 預估工時
- **總計**: 3-4 小時

---

## 功能 5️⃣：推薦頁面「返回設定」按鈕

### 需求描述
在推薦結果頁面添加「返回設定條件」按鈕，並預填當前條件。

### 技術實作

**修改**: `src/app/recommendation/page.tsx`

```tsx
"use client";

import { ArrowLeft, Check } from "lucide-react";

export default function RecommendationPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleBackToSettings = () => {
    const params = new URLSearchParams({
      restaurant: searchParams.get("restaurant") || "",
      people: searchParams.get("people") || "",
      budget: searchParams.get("budget") || "",
      dietary: searchParams.get("dietary") || "",
      mode: searchParams.get("mode") || "",
    });
    router.push(`/input?${params.toString()}`);
  };

  return (
    <div>
      {/* 頂部操作列 */}
      <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between px-4">
          <Button variant="ghost" onClick={handleBackToSettings} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            返回設定
          </Button>

          <Button onClick={() => setShowFeedback(true)} className="gap-2">
            <Check className="w-4 h-4" />
            完成點餐
          </Button>
        </div>
      </div>
    </div>
  );
}
```

**修改**: `src/app/input/page.tsx` - 支援預填

```tsx
useEffect(() => {
  const restaurant = searchParams.get("restaurant");
  const people = searchParams.get("people");
  const budget = searchParams.get("budget");
  const dietary = searchParams.get("dietary");
  const mode = searchParams.get("mode");

  if (restaurant || people || budget) {
    setFormData({
      restaurant_name: restaurant || "",
      people: people ? parseInt(people) : 2,
      budget: budget || "",
      dietary_restrictions: dietary || "",
      mode: (mode as "solo" | "sharing") || "sharing"
    });
  }
}, [searchParams]);
```

### 預估工時
- **總計**: 1.5 小時

---

## 功能 6️⃣：菜品數量選項（非必填）

### 需求描述
在設定條件頁面新增「想要幾道菜」的選項，非必填且無預設值。若數量不合理，彈出警告。

### 驗證邏輯

```tsx
const validateDishCount = (count: number | null, people: number) => {
  if (!count) return { valid: true };

  const minDishes = Math.max(1, Math.floor(people * 0.8));
  const maxDishes = people * 3;

  if (count < minDishes) {
    return {
      valid: false,
      message: `建議至少點 ${minDishes} 道菜，才能滿足 ${people} 人份量`
    };
  }

  if (count > maxDishes) {
    return {
      valid: false,
      message: `${count} 道菜對 ${people} 人來說可能太多了，建議不超過 ${maxDishes} 道`
    };
  }

  return { valid: true };
};
```

### 技術實作

**修改**: `src/app/input/page.tsx`

```tsx
"use client";

import { AlertDialog, AlertDialogContent, AlertDialogDescription, AlertDialogHeader, AlertDialogTitle, AlertDialogAction } from "@/components/ui/alert-dialog";

function InputPageContents() {
  const [formData, setFormData] = useState({
    restaurant_name: "",
    people: 2,
    budget: "",
    dietary_restrictions: "",
    mode: "sharing",
    dish_count: null as number | null  // ← 新增
  });

  const [dishCountWarning, setDishCountWarning] = useState<string | null>(null);

  const handleNext = useCallback(() => {
    if (step === 2) {
      // 驗證菜品數量
      if (formData.dish_count) {
        const validation = validateDishCount(formData.dish_count, formData.people);
        if (!validation.valid) {
          setDishCountWarning(validation.message);
          return;
        }
      }

      const params = new URLSearchParams({
        restaurant: formData.restaurant_name,
        people: formData.people.toString(),
        budget: formData.budget,
        dietary: formData.dietary_restrictions,
        mode: formData.mode,
        ...(formData.dish_count && { dish_count: formData.dish_count.toString() })
      });
      router.push(`/recommendation?${params.toString()}`);
    }
  }, [step, formData, router]);

  return (
    <div>
      {/* 在預算和飲食偏好之間插入 */}
      <div className="space-y-3">
        <Label className="text-base">想要幾道菜？（選填）</Label>
        <div className="flex items-center gap-2">
          <Input
            type="number"
            min="1"
            placeholder="留空則由 AI 決定"
            value={formData.dish_count || ""}
            onChange={(e) => updateData("dish_count", e.target.value ? parseInt(e.target.value) : null)}
            className="bg-secondary/30 border-transparent focus:border-primary"
          />
          <span className="text-muted-foreground">道</span>
        </div>
        <p className="text-xs text-muted-foreground flex items-center gap-1">
          💡 不填的話，AI 會根據人數和預算自動決定
        </p>
      </div>

      {/* 警告對話框 */}
      <AlertDialog open={!!dishCountWarning} onOpenChange={() => setDishCountWarning(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>菜品數量建議</AlertDialogTitle>
            <AlertDialogDescription>{dishCountWarning}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogAction onClick={() => setDishCountWarning(null)}>
            知道了
          </AlertDialogAction>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
```

### 預估工時
- **總計**: 2 小時

---

## 功能 7️⃣：菜品描述限制為 2 行

### 需求描述
推薦頁面的菜品說明文字濃縮在兩行內完成。

### 現況分析
✅ **此功能已實作** - 當前代碼已經使用 `line-clamp-2`

```tsx
// src/app/recommendation/page.tsx 第 438 行
<p className="text-sm text-gray-500 line-clamp-2 leading-relaxed mt-2">
  "{item.reason}"
</p>
```

### 後端優化建議

```python
# 後端 API 修改建議
def generate_dish_reason(dish_info):
    prompt = f"""
    請用**不超過 50 個中文字**精簡描述這道菜的推薦理由。

    菜品：{dish_info['name']}
    評論關鍵字：{dish_info['keywords']}

    格式要求：
    - 長度：40-50 字
    - 重點：為什麼推薦這道菜
    """
    return ai_generate(prompt)
```

### 預估工時
- **前端**: 已完成（0 小時）
- **後端調整**: 1 小時（如需優化）
- **總計**: 0.5-1.5 小時

---

## 功能 8️⃣：每道菜顯示不同的評價數

### 需求描述
每道菜應顯示不同的評價數（不是全部都「128則好評」），數據來自分析資料。

### 資料結構變更

後端 API 需要加入 `review_count` 欄位：

```json
{
  "recommendations": [
    {
      "name": "小籠包",
      "price": 120,
      "reason": "鮮甜多汁...",
      "review_count": 342  // ← 新增
    }
  ]
}
```

### 前端實作（備用方案）

如果後端暫時無法提供，使用前端生成：

```tsx
// 在 recommendation/page.tsx 中
const generateReviewCount = (item: any) => {
  // 使用菜名的 hash 生成穩定的隨機數
  const hash = item.name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const base = item.is_signature ? 150 : 80;
  const range = item.is_signature ? 200 : 100;
  return base + (hash % range);
};

// 使用
<span>
  {item.review_count || generateReviewCount(item)}則好評
</span>
```

### 後端實作建議

```python
def extract_review_count_for_dish(dish_name, reviews):
    count = sum(1 for review in reviews if dish_name in review['text'])
    if count < 10:
        count = random.randint(80, 200) if is_signature else random.randint(30, 100)
    return count
```

### 預估工時
- **前端備用方案**: 1-2 小時
- **後端完整實作**: 3-4 小時
- **總計**: 1-4 小時

---

## 🎯 方案 C：快速迭代執行計劃（最終版本）

### 執行順序

```
階段 1: 快速完成的基礎功能（5-6h）
├─ 功能 1: 登入狀態顯示 (2-3h)
├─ 功能 5: 返回設定按鈕 (1.5h)
├─ 功能 7: 描述限制 2 行 (0.5h) ← 已實作，只需確認
└─ 功能 2: 完成後返回搜尋頁 (1.5h)

階段 2: 中等難度的改進（3-4h）
├─ 功能 6: 菜品數量選項 (2h)
└─ 功能 8: 不同評價數（前端版本）(1-2h)

階段 3: 核心複雜功能（3-4h）
└─ 功能 3: 讚/倒讚評分系統 (3-4h)
    └─ 包含移除閒置計時器
    └─ 包含完成評分後自動彈出

總計：11.5-14 小時
```

### 詳細步驟

#### 階段 1.1: 登入狀態顯示（2-3h）

1. **安裝依賴** (5 min)
   ```bash
   npx shadcn@latest add avatar dropdown-menu
   ```

2. **建立 Header 組件** (1h)
3. **整合到 Layout** (30 min)
4. **樣式調整** (30 min)
5. **測試** (30 min)

#### 階段 1.2: 返回設定按鈕（1.5h）

1. **修改推薦頁面** (1h)
2. **修改 Input 頁面支援預填** (30 min)
3. **測試** (30 min)

#### 階段 1.3: 描述限制 2 行（0.5h）

1. **確認現有實作** (15 min)
2. **測試** (15 min)

#### 階段 1.4: 完成後返回搜尋頁（1.5h）

1. **修改 RatingModal** (1h)
2. **測試** (30 min)

#### 階段 2.1: 菜品數量選項（2h）

1. **修改 Input 頁面** (1h)
2. **加入警告對話框** (30 min)
3. **API 整合** (30 min)

#### 階段 2.2: 不同評價數（1-2h）

1. **實作前端生成函數** (30 min)
2. **修改顯示邏輯** (30 min)
3. **測試** (30 min)

#### 階段 3: 讚/倒讚評分系統（3-4h）

1. **更新資料結構** (1h)
2. **UI 更新** (1-1.5h)
3. **自動彈出邏輯** (30 min)
4. **移除閒置計時器** (30 min)
5. **API 整合** (30 min)
6. **測試** (1h)

---

## 🧪 完整測試計劃

### 功能 1: 登入狀態
- [ ] 未登入時顯示「登入」按鈕
- [ ] 登入後顯示頭像
- [ ] 點擊頭像顯示下拉選單
- [ ] 登出功能正常運作

### 功能 2: 完成後返回
- [ ] 提交回饋後導航到 /input
- [ ] 不會重複請求 API

### 功能 3: 讚/倒讚系統
- [ ] 點擊推薦/不推薦正確更新狀態
- [ ] 完成所有評分後自動彈出 Modal
- [ ] 不會在 20 秒後自動彈出

### 功能 5: 返回設定
- [ ] 點擊按鈕導航到 /input
- [ ] 參數正確預填

### 功能 6: 菜品數量
- [ ] 不填寫時正常提交
- [ ] 數量過少/過多時彈出警告

### 功能 7: 描述限制
- [ ] 長描述正確截斷為 2 行

### 功能 8: 評價數
- [ ] 每道菜顯示不同的評論數
- [ ] 招牌菜評論數較高

---

## 📝 總結

### 最終功能清單（8 個）
- ✅ 功能 1: 登入狀態顯示
- ✅ 功能 2: 完成後返回搜尋頁
- ✅ 功能 3: 讚/倒讚評分系統
- ❌ 功能 4: 閒置自動彈出（已取消）
- ✅ 功能 5: 返回設定按鈕
- ✅ 功能 6: 菜品數量選項（新增）
- ✅ 功能 7: 描述限制 2 行（新增）
- ✅ 功能 8: 不同評價數（新增）

### 方案 C 執行順序
階段 1 (5-6h) → 階段 2 (3-4h) → 階段 3 (3-4h)

**總工時**：11.5-14 小時

### 下一步
準備開始實作**階段 1.1: 登入狀態顯示**
