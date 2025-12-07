# UX 改進功能規劃

## 📋 總覽

本文件規劃 5 個 UX 改進功能，旨在提升使用者體驗和互動性。

**最新更新**：
- ✅ 新增功能 5：推薦頁面「返回設定」按鈕
- ❌ 取消功能 4：移除 20 秒閒置自動彈出機制

---

## 功能 1️⃣：右上角登入狀態顯示

### 需求描述
在所有頁面的右上角顯示用戶登入狀態圖標，讓用戶清楚知道自己已登入。

### 現況分析
- ✅ 已有 NextAuth session 管理
- ✅ 已有 `useSession()` hook
- ❌ 目前沒有 Header 組件顯示登入狀態

### 設計方案

#### UI 設計
```
┌─────────────────────────────────────────┐
│  Carte Logo          [User Avatar] ▼   │ ← Header
└─────────────────────────────────────────┘

未登入：顯示「登入」按鈕
已登入：顯示頭像 + 下拉選單
  - 用戶名稱
  - 登出
```

#### 技術實作

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

### 相依組件需求
- ✅ `Avatar` component (shadcn/ui)
- ✅ `DropdownMenu` component (shadcn/ui)

### 預估工時
- **開發**: 1-2 小時
- **測試**: 30 分鐘
- **總計**: 2-3 小時

### 優先級
**🔴 High** - 基礎 UX，讓用戶知道登入狀態

---

## 功能 2️⃣：完成推薦後返回搜尋頁

### 需求描述
完成推薦並提交回饋後，應該導航回到餐廳搜尋頁 (`/input`)，而不是停留在推薦頁面。避免用戶刷新頁面時重新觸發 API 請求。

### 現況分析
- ✅ 已有 RatingModal 組件
- ✅ 已有 feedback 提交邏輯
- ❌ 提交後沒有導航邏輯
- ❌ 刷新頁面會重新請求 API

### 設計方案

#### 流程設計
```
[Recommendation Page]
  → 用戶評分菜品 (讚/倒讚)
  → 完成所有評分
  → 彈出 RatingModal
  → 提交回饋
  → 導航到 /input  ← 新增此步驟
```

#### 技術實作

**方案 A: 在 RatingModal 中處理** (推薦)

修改 `src/components/rating-modal.tsx`:
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
    // 關閉 Modal
    onClose();

    // 導航到搜尋頁
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

**方案 B: 在 Recommendation Page 中處理**

修改 `src/app/recommendation/page.tsx`:
```tsx
const router = useRouter();

const handleFeedbackSubmit = async (data) => {
  // ... 提交邏輯

  // 提交後導航
  setTimeout(() => {
    router.push("/input");
  }, 2000); // 2秒後導航，讓用戶看到「感謝」訊息
};
```

### 防止重複請求

添加 URL state 檢查：
```tsx
useEffect(() => {
  const params = searchParams;
  const restaurant = params.get("restaurant");

  // 檢查是否有必要參數
  if (!restaurant || !params.get("people")) {
    router.push("/input");
    return;
  }

  // 只在初次載入時請求
  if (!loading && !data) {
    fetchRecommendations();
  }
}, [searchParams]);
```

### 預估工時
- **開發**: 1 小時
- **測試**: 30 分鐘
- **總計**: 1.5 小時

### 優先級
**🟡 Medium** - 改善流程，但不影響核心功能

---

## 功能 3️⃣：讚/倒讚評分系統

### 需求描述
將菜品選擇的綠勾勾改為「讚 👍」和「倒讚 👎」按鈕，讓用戶更清楚地表達對每道菜的評價。

### 現況分析
- ✅ 已有 `selectedItems` state 管理選中的菜品
- ✅ 已有 `toggleItemSelection` 函數
- ❌ 目前只有「選中」狀態（綠勾勾），沒有「不喜歡」狀態

### 設計方案

#### UI 設計
```
┌──────────────────────────────────────┐
│  🍜 小籠包            NT$ 120         │
│  鮮甜多汁的經典招牌                   │
│                                       │
│  [👍 推薦]  [👎 不推薦]  [🔄 換一道]  │
└──────────────────────────────────────┘

狀態：
- 未評分：兩個按鈕都是 outline 樣式
- 按下讚：👍 按鈕變成 solid primary 樣式
- 按下倒讚：👎 按鈕變成 solid destructive 樣式
```

#### 數據結構

擴展 state 管理：
```tsx
// 舊版：只記錄「選中」
const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set());

// 新版：記錄「讚」和「倒讚」
interface ItemRating {
  itemName: string;
  rating: "like" | "dislike" | null;
}

const [itemRatings, setItemRatings] = useState<Map<string, "like" | "dislike">>(new Map());
```

#### 技術實作

修改 `src/app/recommendation/page.tsx`:

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

      // 如果點擊相同的評分，則取消
      if (newMap.get(itemName) === rating) {
        newMap.delete(itemName);
      } else {
        newMap.set(itemName, rating);
      }

      return newMap;
    });

    resetIdleTimer(); // 重置閒置計時器
  };

  // 檢查是否所有菜品都已評分
  const allItemsRated = currentItems.every(item =>
    itemRatings.has(item.name)
  );

  // 當所有菜品都評分後，自動彈出回饋 Modal
  useEffect(() => {
    if (allItemsRated && currentItems.length > 0 && !showFeedback) {
      // 短暫延遲後顯示
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
          <div key={index} className="border rounded-lg p-4">
            <h3 className="font-bold">{item.name}</h3>
            <p className="text-sm text-muted-foreground">{item.description}</p>
            <p className="font-mono">NT$ {item.price}</p>

            <div className="flex gap-2 mt-3">
              {/* 讚按鈕 */}
              <Button
                variant={currentRating === "like" ? "default" : "outline"}
                size="sm"
                onClick={() => handleRating(item.name, "like")}
                className={currentRating === "like" ? "bg-primary" : ""}
              >
                <ThumbsUp className="w-4 h-4 mr-1" />
                推薦
              </Button>

              {/* 倒讚按鈕 */}
              <Button
                variant={currentRating === "dislike" ? "destructive" : "outline"}
                size="sm"
                onClick={() => handleRating(item.name, "dislike")}
              >
                <ThumbsDown className="w-4 h-4 mr-1" />
                不推薦
              </Button>

              {/* 換一道按鈕 */}
              {item.alternatives && item.alternatives.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleSwap(index)}
                >
                  <RefreshCw className="w-4 h-4 mr-1" />
                  換一道
                </Button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

### API 整合

修改提交給後端的資料格式：

```tsx
const handleFeedbackSubmit = async (data: { rating: "up" | "down"; comment: string }) => {
  // 整理菜品評分
  const itemFeedback = Array.from(itemRatings.entries()).map(([name, rating]) => ({
    item_name: name,
    rating: rating === "like" ? 1 : -1  // 1 = 喜歡, -1 = 不喜歡
  }));

  await submitFeedback({
    recommendation_id: recommendationId,
    overall_rating: data.rating === "up" ? 5 : 1,
    item_ratings: itemFeedback,  // 新增：個別菜品評分
    comment: data.comment
  }, token);
};
```

### 預估工時
- **開發**: 2-3 小時
- **測試**: 1 小時
- **總計**: 3-4 小時

### 優先級
**🔴 High** - 顯著改善用戶回饋質量

---

## 功能 4️⃣：完成評分後自動彈出回饋表單

### 需求描述
當用戶完成所有菜品的評分（讚/倒讚）後，自動彈出整體推薦回饋和功能回饋表單。

### 現況分析
- ✅ 已有 RatingModal 組件
- ✅ 已有閒置計時器（20秒無操作彈出）
- ❌ 沒有「完成所有評分」的觸發條件

### 設計方案

#### 觸發邏輯
```
當用戶評分菜品時：
  → 檢查是否所有菜品都已評分
  → 如果是：等待 500ms 後彈出 RatingModal
  → 如果否：繼續等待

優先級：
1. 完成所有評分 → 自動彈出
2. 閒置 20 秒 → 自動彈出（備用）
```

#### 技術實作

已在**功能 3**中實作：

```tsx
// 檢查是否所有菜品都已評分
const allItemsRated = currentItems.every(item =>
  itemRatings.has(item.name)
);

// 自動彈出回饋 Modal
useEffect(() => {
  if (allItemsRated && currentItems.length > 0 && !showFeedback) {
    // 短暫延遲，避免過於突兀
    setTimeout(() => {
      setShowFeedback(true);
    }, 500);
  }
}, [allItemsRated, currentItems.length, showFeedback]);
```

#### 優化 RatingModal

更新問題文字以反映新流程：

```tsx
// 在 RatingModal 的 "rating" step
<h3 className="text-2xl font-bold">
  感謝您的評分！整體推薦滿意嗎？
</h3>
<p className="text-muted-foreground">
  您已評價了 {itemCount} 道菜，請告訴我們整體感受
</p>
```

### 預估工時
- **開發**: 30 分鐘（與功能 3 合併）
- **測試**: 30 分鐘
- **總計**: 1 小時

### 優先級
**🔴 High** - 與功能 3 緊密相關，應一起實作

---

## 📊 實作優先順序建議

### 推薦順序 A：按依賴關係

```
Phase 1: 基礎改進（獨立功能）
├─ 功能 1: 登入狀態顯示 (2-3 小時)
└─ 功能 2: 完成後返回搜尋頁 (1.5 小時)

Phase 2: 評分系統改進（互相依賴）
├─ 功能 3: 讚/倒讚系統 (3-4 小時)
└─ 功能 4: 自動彈出回饋 (1 小時) ← 依賴功能 3

總計：7.5-9.5 小時
```

### 推薦順序 B：按影響力

```
1️⃣ 功能 3 + 4: 評分系統改進 (4-5 小時) - 最大影響
2️⃣ 功能 1: 登入狀態顯示 (2-3 小時) - 基礎 UX
3️⃣ 功能 2: 返回搜尋頁 (1.5 小時) - 流程優化
```

### 推薦順序 C：快速迭代

```
1️⃣ 功能 1: 登入狀態 (快速完成，立即改善 UX)
2️⃣ 功能 2: 返回搜尋頁 (快速完成，修復流程問題)
3️⃣ 功能 3 + 4: 評分系統 (較複雜，但價值最高)
```

---

## 🧪 測試計劃

### 功能 1: 登入狀態
- [ ] 未登入時顯示「登入」按鈕
- [ ] 登入後顯示頭像
- [ ] 點擊頭像顯示下拉選單
- [ ] 下拉選單顯示正確的用戶名和郵箱
- [ ] 登出功能正常運作
- [ ] 頭像圖片載入失敗時顯示 fallback

### 功能 2: 導航流程
- [ ] 提交回饋後導航到 /input
- [ ] 刷新推薦頁面時檢查參數，缺少則導航
- [ ] 不會重複請求 API

### 功能 3: 評分系統
- [ ] 點擊「推薦」按鈕正確更新狀態
- [ ] 點擊「不推薦」按鈕正確更新狀態
- [ ] 再次點擊相同按鈕可取消評分
- [ ] 按鈕樣式正確反映當前狀態
- [ ] 評分資料正確提交到後端

### 功能 4: 自動彈出
- [ ] 完成所有評分後自動彈出 Modal
- [ ] 延遲 500ms 後彈出（避免突兀）
- [ ] 如果已彈出過，不重複彈出
- [ ] 閒置 20 秒仍會彈出（備用機制）

---

## 📝 後端 API 需求

### 需要更新的 API

**POST `/api/feedback`**

現有格式：
```json
{
  "recommendation_id": "string",
  "rating": 5,
  "selected_items": ["小籠包", "蝦仁炒飯"],
  "comment": "很滿意"
}
```

新增格式：
```json
{
  "recommendation_id": "string",
  "overall_rating": 5,              // 整體評分
  "item_ratings": [                 // 新增：個別菜品評分
    {
      "item_name": "小籠包",
      "rating": 1                    // 1 = 喜歡, -1 = 不喜歡
    },
    {
      "item_name": "蝦仁炒飯",
      "rating": -1
    }
  ],
  "comment": "很滿意"
}
```

### 後端改動
- 更新 `feedback` schema 支援 `item_ratings`
- 儲存到 Firestore 時包含個別菜品評分
- 用於未來的推薦算法優化

---

## 🎯 成功指標

### 定量指標
- 用戶完成評分率提升 > 30%
- 平均評分時間減少 > 20%
- 回饋提交率提升 > 40%

### 定性指標
- 用戶清楚知道登入狀態
- 用戶明確表達對每道菜的喜好
- 流程更順暢，減少困惑

---

## 📦 所需依賴

### 新增 shadcn/ui 組件
```bash
npx shadcn@latest add avatar
npx shadcn@latest add dropdown-menu
```

### 圖標
- ✅ 已有 `lucide-react`
- 需要的圖標：`ThumbsUp`, `ThumbsDown`, `RefreshCw`, `User`, `LogOut`

---

## 🚀 部署檢查清單

部署前確認：
- [ ] 所有測試通過
- [ ] 後端 API 已更新
- [ ] 環境變數正確設置
- [ ] 樣式在生產環境正確顯示
- [ ] 響應式設計在各裝置正常
- [ ] 性能無明顯下降

---

**總結**: 這 4 個功能能顯著提升 UX，建議按 Phase 1 → Phase 2 順序實作，或按影響力優先實作功能 3+4。

---

## 功能 5️⃣：推薦頁面「返回設定」按鈕

### 需求描述
在推薦結果頁面添加一個「返回設定條件」按鈕，讓用戶可以快速回到 Input 頁面重新設定條件，無需從頭開始。

### 現況分析
- ✅ 已有推薦結果頁面
- ❌ 目前沒有返回按鈕
- ❌ 用戶想重新設定需要手動輸入 URL 或刷新頁面

### 設計方案

#### UI 設計
```
┌────────────────────────────────────────────┐
│  [← 返回設定]              [完成點餐] 按鈕  │ ← 頂部操作列
├────────────────────────────────────────────┤
│                                             │
│  推薦菜單內容...                            │
│                                             │
└────────────────────────────────────────────┘

位置選項：
方案 A: 固定在頁面頂部（推薦）
方案 B: 浮動按鈕在左上角
方案 C: 在標題旁邊
```

#### 技術實作

**修改**: `src/app/recommendation/page.tsx`

```tsx
"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Check } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function RecommendationPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // 返回設定頁面，保留當前參數
  const handleBackToSettings = () => {
    // 選項 A: 直接返回 input 頁面（重新開始）
    router.push("/input");

    // 選項 B: 返回 input 頁面並預填當前參數（推薦）
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
    <div className="min-h-screen bg-background">
      {/* 頂部操作列 - 方案 A（推薦）*/}
      <div className="sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between px-4">
          <Button
            variant="ghost"
            onClick={handleBackToSettings}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            返回設定
          </Button>

          <Button
            onClick={() => setShowFeedback(true)}
            className="gap-2 bg-primary"
          >
            <Check className="w-4 h-4" />
            完成點餐
          </Button>
        </div>
      </div>

      {/* 推薦內容 */}
      <div className="container py-8">
        {/* ... 現有的推薦內容 ... */}
      </div>
    </div>
  );
}
```

**選項 B: 浮動按鈕**（如果不想要頂部操作列）

```tsx
{/* 浮動返回按鈕 */}
<Button
  variant="outline"
  size="icon"
  className="fixed top-20 left-4 z-50 rounded-full shadow-lg"
  onClick={handleBackToSettings}
>
  <ArrowLeft className="w-5 h-5" />
</Button>
```

#### Input 頁面支援預填

**修改**: `src/app/input/page.tsx`

```tsx
"use client";

import { useSearchParams } from "next/navigation";
import { useEffect } from "react";

export default function InputPage() {
  const searchParams = useSearchParams();
  const [formData, setFormData] = useState({
    restaurant_name: "",
    people: 2,
    budget: "",
    dietary_restrictions: "",
    mode: "sharing"
  });

  // 從 URL 參數預填表單
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

  // ... 其他邏輯
}
```

### 用戶體驗流程

```
推薦頁面
  ↓
點擊「返回設定」
  ↓
返回 Input 頁面（已預填當前條件）
  ↓
修改條件
  ↓
重新搜尋
```

### 預估工時
- **開發**: 1 小時
- **測試**: 30 分鐘
- **總計**: 1.5 小時

### 優先級
**🟡 Medium-High** - 改善用戶控制感，但不影響核心流程

---

## 🔄 功能 4 更新：移除閒置計時器

### 變更說明
根據最新需求，**移除** 20 秒閒置自動彈出回饋 Modal 的機制。

### 原因
- 20 秒自動彈出可能打斷用戶思考
- 用戶可能還在瀏覽菜單，不想被打斷
- 改為完全由用戶主動觸發（完成評分或點擊按鈕）

### 技術實作

**修改**: `src/app/recommendation/page.tsx`

```tsx
// ❌ 移除這些代碼
const idleTimerRef = useRef<NodeJS.Timeout | null>(null);
const IDLE_TIMEOUT = 20000;

const resetIdleTimer = useCallback(() => {
  if (idleTimerRef.current) {
    clearTimeout(idleTimerRef.current);
  }
  if (!loading && !showFeedback) {
    idleTimerRef.current = setTimeout(() => {
      setShowFeedback(true);
    }, IDLE_TIMEOUT);
  }
}, [loading, showFeedback]);

useEffect(() => {
  const events = ["mousemove", "mousedown", "click", "scroll", "keydown", "touchstart"];
  const handleActivity = () => resetIdleTimer();
  events.forEach(event => window.addEventListener(event, handleActivity));
  resetIdleTimer();
  return () => {
    events.forEach(event => window.removeEventListener(event, handleActivity));
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
  };
}, [resetIdleTimer]);
```

### 新的觸發機制

只保留兩種觸發方式：

1. **完成所有菜品評分**（自動）
```tsx
useEffect(() => {
  if (allItemsRated && currentItems.length > 0 && !showFeedback) {
    setTimeout(() => setShowFeedback(true), 500);
  }
}, [allItemsRated, currentItems.length, showFeedback]);
```

2. **點擊「完成點餐」按鈕**（手動）
```tsx
<Button onClick={() => setShowFeedback(true)}>
  完成點餐
</Button>
```

### 預估工時
- **開發**: 30 分鐘（刪除代碼）
- **測試**: 15 分鐘
- **總計**: 45 分鐘

### 優先級
**🟢 Low** - 簡化邏輯，與功能 3 一起處理

---

## 📊 更新後的實作優先順序

### 最新功能列表

| 功能 | 優先級 | 工時 | 難度 | 影響力 | 狀態 |
|------|--------|------|------|--------|------|
| 1️⃣ 登入狀態顯示 | 🔴 High | 2-3h | 簡單 | 中 | ✅ 規劃完成 |
| 2️⃣ 返回搜尋頁 | 🟡 Medium | 1.5h | 簡單 | 低 | ✅ 規劃完成 |
| 3️⃣ 讚/倒讚系統 | 🔴 High | 3-4h | 中等 | 高 | ✅ 規劃完成 |
| 4️⃣ ~~閒置彈出~~ | ❌ 取消 | -0.75h | - | - | 🗑️ 已移除 |
| 5️⃣ 返回設定按鈕 | 🟡 Med-High | 1.5h | 簡單 | 中 | ✅ 規劃完成 |

**調整後總計**：7.5-9 小時

### 推薦執行順序（更新版）

#### 方案 A：按依賴關係
```
Phase 1: 基礎 UX 改進
├─ 功能 1: 登入狀態顯示 (2-3h)
├─ 功能 5: 返回設定按鈕 (1.5h)
└─ 功能 2: 完成後返回 (1.5h)

Phase 2: 評分系統
└─ 功能 3: 讚/倒讚 + 自動彈出 (3-4h)
    └─ 包含移除閒置計時器 (已含在內)
```

#### 方案 B：按影響力（推薦）⭐️
```
1️⃣ 功能 3: 讚/倒讚系統 (3-4h)
   └─ 最大價值，包含移除閒置計時器

2️⃣ 功能 1: 登入狀態 (2-3h)
   └─ 基礎 UX，全站可見

3️⃣ 功能 5: 返回設定 (1.5h)
   └─ 改善控制感

4️⃣ 功能 2: 完成後返回 (1.5h)
   └─ 流程優化
```

#### 方案 C：快速迭代
```
1️⃣ 功能 1: 登入狀態 (2-3h) ← 快速完成
2️⃣ 功能 5: 返回設定 (1.5h) ← 快速完成
3️⃣ 功能 2: 完成後返回 (1.5h) ← 快速完成
4️⃣ 功能 3: 讚/倒讚系統 (3-4h) ← 最後攻堅
```

---

## 🎯 功能 5 詳細設計

### UI 選項對比

#### 選項 A: 頂部操作列（推薦）✅
```
優點：
- 清晰可見
- 與「完成點餐」按鈕並列，邏輯清楚
- 固定位置，滾動時也能看到

缺點：
- 佔用垂直空間
```

#### 選項 B: 浮動按鈕
```
優點：
- 不佔版面
- 更有現代感

缺點：
- 可能遮擋內容
- 不夠明顯
```

#### 選項 C: 在標題旁
```
優點：
- 節省空間

缺點：
- 滾動後看不到
- 與標題混在一起不夠突出
```

### 預填功能好處

1. **用戶體驗**：
   - 不需要重新輸入已設定的條件
   - 只需修改想改的部分
   - 節省時間

2. **數據保留**：
   - 餐廳名稱
   - 人數
   - 預算
   - 飲食限制
   - 用餐模式

3. **實作簡單**：
   - 只需在 Input 頁面讀取 URL 參數
   - 自動填入表單

---

## 🧪 更新後的測試計劃

### 功能 5: 返回設定按鈕
- [ ] 點擊「返回設定」按鈕導航到 /input
- [ ] Input 頁面正確預填所有參數
- [ ] 修改預填的值後可以重新搜尋
- [ ] 按鈕在各種螢幕尺寸下都清晰可見
- [ ] 按鈕樣式與整體設計一致

### 功能 4: 移除閒置計時器
- [ ] 不會在 20 秒後自動彈出 Modal
- [ ] 只有完成評分才彈出
- [ ] 點擊「完成點餐」按鈕才彈出
- [ ] 移除所有相關事件監聽器
- [ ] 沒有 memory leak

---

## 📝 總結

### 主要變更
1. ✅ **新增功能 5**：返回設定按鈕（1.5h）
2. ❌ **移除功能 4**：閒置計時器（節省 0.75h）

### 最終功能清單
- 功能 1: 登入狀態顯示 ✅
- 功能 2: 完成後返回搜尋頁 ✅
- 功能 3: 讚/倒讚評分系統 ✅
- ~~功能 4: 閒置自動彈出~~ ❌ 取消
- 功能 5: 返回設定按鈕 ✅ 新增

### 推薦執行順序
**方案 B（按影響力）**最適合當前需求：
1. 功能 3 (3-4h) - 核心改進
2. 功能 1 (2-3h) - 基礎 UX
3. 功能 5 (1.5h) - 用戶控制
4. 功能 2 (1.5h) - 流程優化

**總工時**: 8.5-10 小時
