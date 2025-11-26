# 錯誤處理系統整合指南

快速開始使用錯誤處理系統的步驟指南。

## 已完成的整合

✅ **Root Layout** (`/src/app/layout.tsx`)
- 已加入 `<NetworkStatus />` 組件 - 自動監控網路狀態
- 已包含 `<Toaster />` 組件 - 顯示錯誤通知

✅ **全域錯誤頁面**
- `/src/app/not-found.tsx` - 404 頁面（自動生效）
- `/src/app/error.tsx` - 500 錯誤頁面（自動生效）

## 需要手動整合的部分

### 1. 在頁面中使用 ErrorBoundary

在需要錯誤處理的頁面加入 ErrorBoundary：

```tsx
// 範例：/src/app/restaurants/page.tsx
import { ErrorBoundary } from "@/components/error-boundary";

export default function RestaurantsPage() {
  return (
    <ErrorBoundary>
      {/* 您的頁面內容 */}
      <RestaurantList />
    </ErrorBoundary>
  );
}
```

**建議在以下頁面加入 ErrorBoundary：**
- `/src/app/input/page.tsx`
- `/src/app/recommendation/page.tsx`
- `/src/app/menu/page.tsx`
- 其他主要功能頁面

### 2. 更新 API 呼叫

使用 `fetchWithErrorHandling` 取代原本的 `fetch`：

```tsx
// 之前
const response = await fetch("/api/restaurants");
const data = await response.json();

// 之後
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

const data = await fetchWithErrorHandling<Restaurant[]>("/api/restaurants");
// 錯誤會自動顯示 Toast 通知
```

**或者建立統一的 API 函數：**

```tsx
// /src/lib/api.ts
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

export async function getRestaurants() {
  return fetchWithErrorHandling<Restaurant[]>("/api/restaurants");
}

export async function getRestaurant(id: string) {
  return fetchWithErrorHandling<Restaurant>(`/api/restaurants/${id}`);
}

export async function createReservation(data: ReservationData) {
  return fetchWithErrorHandling<Reservation>("/api/reservations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}
```

### 3. 處理特定的 404 情況

在動態路由頁面中處理資源不存在的情況：

```tsx
// /src/app/restaurants/[id]/page.tsx
import { notFound } from "next/navigation";
import { getRestaurant } from "@/lib/api";

export default async function RestaurantPage({
  params
}: {
  params: { id: string }
}) {
  const restaurant = await getRestaurant(params.id);

  if (!restaurant) {
    notFound(); // 顯示 404 頁面
  }

  return (
    <div>
      <h1>{restaurant.name}</h1>
      {/* 餐廳詳情 */}
    </div>
  );
}
```

### 4. 使用網路狀態檢查（可選）

在需要檢查網路狀態的組件中：

```tsx
import { useNetworkStatus } from "@/components/network-status";

function MyComponent() {
  const isOnline = useNetworkStatus();

  if (!isOnline) {
    return (
      <div className="text-center py-12">
        <p className="text-terracotta font-display text-xl">
          網路連接中斷，請檢查您的網路設定
        </p>
      </div>
    );
  }

  return (
    <div>
      {/* 正常內容 */}
    </div>
  );
}
```

## 快速整合檢查清單

- [ ] 在主要頁面加入 `<ErrorBoundary>`
  - [ ] `/src/app/input/page.tsx`
  - [ ] `/src/app/recommendation/page.tsx`
  - [ ] `/src/app/menu/page.tsx`

- [ ] 更新 API 呼叫使用 `fetchWithErrorHandling`
  - [ ] 建立 `/src/lib/api.ts` 統一管理 API 呼叫
  - [ ] 更新現有的 fetch 呼叫

- [ ] 在動態路由加入 404 處理
  - [ ] 檢查所有 `[id]` 路由
  - [ ] 加入 `notFound()` 呼叫

- [ ] 測試錯誤處理
  - [ ] 測試 ErrorBoundary（拋出錯誤）
  - [ ] 測試 API 錯誤（呼叫不存在的 endpoint）
  - [ ] 測試網路斷線（開發者工具設為 Offline）
  - [ ] 測試 404 頁面（訪問不存在的 URL）

## 實際應用範例

### 完整的頁面實作

```tsx
// /src/app/restaurants/page.tsx
"use client";

import { useState, useEffect } from "react";
import { ErrorBoundary } from "@/components/error-boundary";
import { useNetworkStatus } from "@/components/network-status";
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

interface Restaurant {
  id: string;
  name: string;
  cuisine: string;
}

function RestaurantListContent() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const isOnline = useNetworkStatus();

  useEffect(() => {
    loadRestaurants();
  }, []);

  async function loadRestaurants() {
    if (!isOnline) return;

    setLoading(true);
    try {
      const data = await fetchWithErrorHandling<Restaurant[]>(
        "/api/restaurants"
      );
      setRestaurants(data);
    } catch (error) {
      // 錯誤已自動處理並顯示 Toast
    } finally {
      setLoading(false);
    }
  }

  if (!isOnline) {
    return (
      <div className="text-center py-12">
        <p className="text-terracotta">請檢查您的網路連接</p>
      </div>
    );
  }

  if (loading) {
    return <div className="text-center py-12">載入中...</div>;
  }

  return (
    <div className="grid gap-4">
      {restaurants.map((restaurant) => (
        <div key={restaurant.id} className="p-4 bg-cream-50 rounded-lg">
          <h3 className="font-display text-xl">{restaurant.name}</h3>
          <p className="text-charcoal/70">{restaurant.cuisine}</p>
        </div>
      ))}
    </div>
  );
}

// 用 ErrorBoundary 包裝
export default function RestaurantsPage() {
  return (
    <ErrorBoundary>
      <div className="container mx-auto px-4 py-8">
        <h1 className="font-display text-4xl mb-8">餐廳列表</h1>
        <RestaurantListContent />
      </div>
    </ErrorBoundary>
  );
}
```

## 常見問題

### Q: ErrorBoundary 和 error.tsx 有什麼差別？

**A:**
- `ErrorBoundary` 是 React 組件，用於捕捉**客戶端組件樹**中的錯誤
- `error.tsx` 是 Next.js 頁面，用於捕捉**整個頁面級別**的錯誤（包括伺服器端錯誤）

建議：兩者都使用，提供雙重保護。

### Q: 為什麼要同時使用 fetchWithErrorHandling 和 try-catch？

**A:**
- `fetchWithErrorHandling` 會**自動顯示 Toast 通知**
- `try-catch` 讓你可以在錯誤發生後**執行額外操作**（例如重設狀態、記錄日誌等）

### Q: Toast 通知會不會太頻繁？

**A:**
根據 `/src/lib/use-toast.ts` 的設定，一次只會顯示一個 Toast，新的會取代舊的。可以調整：
- `TOAST_LIMIT`：同時顯示的 Toast 數量
- `TOAST_REMOVE_DELAY`：Toast 顯示時間

### Q: 如何不顯示自動 Toast？

**A:**
```tsx
const data = await fetchWithErrorHandling(
  "/api/data",
  { method: "GET" },
  false  // 第三個參數設為 false
);
```

## 測試建議

### 1. 開發環境測試

```tsx
// 建立一個測試頁面 /src/app/test-errors/page.tsx
"use client";

import { ErrorBoundary } from "@/components/error-boundary";
import { fetchWithErrorHandling } from "@/lib/api-error-handler";
import { Button } from "@/components/ui/button";

export default function TestErrorsPage() {
  function throwError() {
    throw new Error("測試 ErrorBoundary");
  }

  async function testApiError() {
    await fetchWithErrorHandling("/api/non-existent");
  }

  return (
    <ErrorBoundary>
      <div className="container mx-auto px-4 py-8 space-y-4">
        <h1 className="font-display text-4xl">錯誤處理測試</h1>

        <Button onClick={throwError}>
          測試 ErrorBoundary
        </Button>

        <Button onClick={testApiError}>
          測試 API 錯誤
        </Button>

        <Button onClick={() => window.location.href = "/non-existent"}>
          測試 404 頁面
        </Button>
      </div>
    </ErrorBoundary>
  );
}
```

### 2. 網路狀態測試

1. 打開瀏覽器開發者工具
2. 切換到 Network 面板
3. 選擇 "Offline" 或 "Slow 3G"
4. 測試應用程式的反應

## 需要協助？

查看完整文件：`/ERROR_HANDLING_README.md`

或參考範例程式碼：`/src/lib/error-handling-example.tsx`
