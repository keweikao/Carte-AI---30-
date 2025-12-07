# 錯誤處理系統文件

這份文件說明如何在 Carte 應用程式中使用錯誤處理系統。

## 目錄

1. [概述](#概述)
2. [檔案結構](#檔案結構)
3. [功能說明](#功能說明)
4. [使用指南](#使用指南)
5. [整合方式](#整合方式)

---

## 概述

本錯誤處理系統提供完整的錯誤處理方案，包括：

- **React Error Boundary**：捕捉 React 組件錯誤
- **API 錯誤處理**：統一的 API 錯誤處理和提示
- **網路狀態監控**：自動偵測網路連線狀態
- **錯誤頁面**：404 和 500 錯誤頁面
- **Toast 通知**：友善的錯誤訊息提示

所有錯誤頁面和組件都採用雜誌風格設計，符合應用程式的整體美學。

---

## 檔案結構

```
frontend/
├── src/
│   ├── components/
│   │   ├── error-boundary.tsx          # ErrorBoundary 組件
│   │   └── network-status.tsx          # 網路狀態監控組件
│   ├── lib/
│   │   ├── api-error-handler.ts        # API 錯誤處理工具
│   │   └── error-handling-example.tsx  # 使用範例（參考用）
│   └── app/
│       ├── not-found.tsx               # 404 頁面
│       ├── error.tsx                   # 500 錯誤頁面
│       └── layout.tsx                  # 已整合 NetworkStatus
```

---

## 功能說明

### 1. ErrorBoundary 組件

**位置**：`/src/components/error-boundary.tsx`

捕捉 React 組件樹中的錯誤，顯示友善的錯誤訊息。

**特點**：
- 自動捕捉 React 組件錯誤
- 提供重試功能
- 支援自訂錯誤頁面
- 開發模式顯示詳細錯誤資訊
- 雜誌風格設計

**基本使用**：
```tsx
import { ErrorBoundary } from "@/components/error-boundary";

function MyPage() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

**使用 HOC**：
```tsx
import { withErrorBoundary } from "@/components/error-boundary";

function MyComponent() {
  return <div>內容</div>;
}

export default withErrorBoundary(MyComponent);
```

**自訂錯誤頁面**：
```tsx
import { ErrorBoundary, ErrorFallbackProps } from "@/components/error-boundary";

function CustomErrorFallback({ error, resetError }: ErrorFallbackProps) {
  return (
    <div>
      <h1>自訂錯誤訊息</h1>
      <p>{error.message}</p>
      <button onClick={resetError}>重試</button>
    </div>
  );
}

function MyPage() {
  return (
    <ErrorBoundary fallback={CustomErrorFallback}>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

---

### 2. API 錯誤處理

**位置**：`/src/lib/api-error-handler.ts`

提供統一的 API 錯誤處理機制。

**特點**：
- 自動分類錯誤類型
- 顯示友善的中文錯誤訊息
- 支援自動 Toast 通知
- 包含網路錯誤處理
- TypeScript 類型安全

**錯誤類型**：
```typescript
enum ErrorType {
  NETWORK = "NETWORK",           // 網路錯誤
  VALIDATION = "VALIDATION",     // 驗證錯誤
  AUTHENTICATION = "AUTHENTICATION", // 認證錯誤
  AUTHORIZATION = "AUTHORIZATION",   // 授權錯誤
  NOT_FOUND = "NOT_FOUND",       // 404 錯誤
  SERVER = "SERVER",             // 伺服器錯誤
  UNKNOWN = "UNKNOWN",           // 未知錯誤
}
```

**fetchWithErrorHandling 使用**：
```tsx
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

async function loadRestaurants() {
  try {
    const data = await fetchWithErrorHandling<Restaurant[]>(
      "/api/restaurants",
      { method: "GET" }
    );
    return data;
  } catch (error) {
    // 錯誤已自動顯示為 Toast
    console.error("載入失敗:", error);
  }
}
```

**不顯示自動 Toast**：
```tsx
const data = await fetchWithErrorHandling<Restaurant[]>(
  "/api/restaurants",
  { method: "GET" },
  false // 第三個參數設為 false
);
```

**手動顯示錯誤 Toast**：
```tsx
import { showErrorToast } from "@/lib/api-error-handler";

try {
  // 可能會拋出錯誤的程式碼
} catch (error) {
  showErrorToast(error);
}
```

**使用 withErrorHandling 包裝函數**：
```tsx
import { withErrorHandling } from "@/lib/api-error-handler";

const loadData = withErrorHandling(async (id: string) => {
  const response = await fetch(`/api/data/${id}`);
  if (!response.ok) throw new Error("Failed to fetch");
  return response.json();
});

// 使用 - 自動顯示錯誤 Toast
await loadData("123");
```

**建立自訂 API 錯誤**：
```tsx
import { ApiError, ErrorType } from "@/lib/api-error-handler";

throw new ApiError(
  "找不到餐廳資料",
  404,
  ErrorType.NOT_FOUND
);
```

---

### 3. 網路狀態監控

**位置**：`/src/components/network-status.tsx`

自動偵測網路連線狀態並顯示通知。

**特點**：
- 自動偵測網路狀態變化
- 顯示連線/斷線 Toast 通知
- 提供 Hook 供組件使用
- 已整合到應用程式根布局

**NetworkStatus 組件**：

已自動整合到 `/src/app/layout.tsx`，無需額外設置。

**useNetworkStatus Hook**：
```tsx
import { useNetworkStatus } from "@/components/network-status";

function MyComponent() {
  const isOnline = useNetworkStatus();

  if (!isOnline) {
    return (
      <div className="text-center py-8">
        <p className="text-terracotta">您目前離線，請檢查網路連接</p>
      </div>
    );
  }

  return <div>正常內容</div>;
}
```

**在 API 呼叫前檢查網路**：
```tsx
import { useNetworkStatus } from "@/components/network-status";
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

function RestaurantList() {
  const isOnline = useNetworkStatus();

  async function loadRestaurants() {
    if (!isOnline) {
      // 網路斷線時不發送請求
      return;
    }

    const data = await fetchWithErrorHandling("/api/restaurants");
    // 處理資料...
  }

  return <div>...</div>;
}
```

---

### 4. 錯誤頁面

#### 404 Not Found 頁面

**位置**：`/src/app/not-found.tsx`

當使用者訪問不存在的頁面時自動顯示。

**特點**：
- 雜誌風格設計
- 提供返回首頁和返回上一頁按鈕
- 建議用戶下一步操作
- 裝飾性引言

**觸發方式**：
- Next.js 自動處理 404 錯誤
- 或手動調用：
```tsx
import { notFound } from "next/navigation";

function MyPage({ params }: { params: { id: string } }) {
  const restaurant = await getRestaurant(params.id);

  if (!restaurant) {
    notFound(); // 顯示 404 頁面
  }

  return <div>...</div>;
}
```

#### 500 錯誤頁面

**位置**：`/src/app/error.tsx`

捕捉應用程式中未處理的錯誤。

**特點**：
- 雜誌風格設計
- 重試功能
- 開發模式顯示錯誤詳情
- 提供可能原因和解決方案
- 支援資訊連結

**觸發方式**：
- Next.js 自動捕捉頁面級錯誤
- 伺服器端錯誤
- 未被 ErrorBoundary 捕捉的錯誤

---

## 使用指南

### 完整的錯誤處理實作範例

```tsx
"use client";

import { useState } from "react";
import { ErrorBoundary } from "@/components/error-boundary";
import { useNetworkStatus } from "@/components/network-status";
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

interface Restaurant {
  id: string;
  name: string;
}

function RestaurantList() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const isOnline = useNetworkStatus();

  async function loadRestaurants() {
    // 檢查網路狀態
    if (!isOnline) {
      return; // NetworkStatus 組件會自動顯示 Toast
    }

    setLoading(true);
    try {
      // 使用 fetchWithErrorHandling 自動處理錯誤
      const data = await fetchWithErrorHandling<Restaurant[]>(
        "/api/restaurants",
        { method: "GET" }
      );
      setRestaurants(data);
    } catch (error) {
      // 錯誤已由 fetchWithErrorHandling 處理
      // 這裡可以做額外處理，例如重設狀態
    } finally {
      setLoading(false);
    }
  }

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
      {loading && <div>載入中...</div>}
      {restaurants.map((restaurant) => (
        <div key={restaurant.id}>{restaurant.name}</div>
      ))}
    </div>
  );
}

// 使用 ErrorBoundary 包裝
export default function RestaurantPage() {
  return (
    <ErrorBoundary>
      <RestaurantList />
    </ErrorBoundary>
  );
}
```

---

## 整合方式

### 已完成的整合

1. **Root Layout** (`/src/app/layout.tsx`)
   - 已加入 `<NetworkStatus />` 組件
   - 已包含 `<Toaster />` 組件

### 建議的整合步驟

#### 1. 在頁面組件中使用 ErrorBoundary

```tsx
// /src/app/restaurants/page.tsx
import { ErrorBoundary } from "@/components/error-boundary";
import RestaurantList from "@/components/restaurant-list";

export default function RestaurantsPage() {
  return (
    <ErrorBoundary>
      <RestaurantList />
    </ErrorBoundary>
  );
}
```

#### 2. 在 API 呼叫中使用錯誤處理

```tsx
// /src/lib/api.ts
import { fetchWithErrorHandling } from "@/lib/api-error-handler";

export async function getRestaurants() {
  return fetchWithErrorHandling<Restaurant[]>("/api/restaurants");
}

export async function getRestaurant(id: string) {
  return fetchWithErrorHandling<Restaurant>(`/api/restaurants/${id}`);
}
```

#### 3. 在組件中檢查網路狀態

```tsx
import { useNetworkStatus } from "@/components/network-status";

function MyComponent() {
  const isOnline = useNetworkStatus();

  // 使用 isOnline 狀態...
}
```

#### 4. 處理 404 錯誤

```tsx
// /src/app/restaurants/[id]/page.tsx
import { notFound } from "next/navigation";

export default async function RestaurantPage({ params }: { params: { id: string } }) {
  const restaurant = await getRestaurant(params.id);

  if (!restaurant) {
    notFound(); // 顯示 404 頁面
  }

  return <div>...</div>;
}
```

---

## 測試錯誤處理

### 測試 ErrorBoundary

```tsx
function ThrowErrorComponent() {
  throw new Error("測試錯誤");
  return <div>不會顯示</div>;
}

function TestPage() {
  return (
    <ErrorBoundary>
      <ThrowErrorComponent />
    </ErrorBoundary>
  );
}
```

### 測試 API 錯誤

```tsx
// 模擬 API 錯誤
async function testApiError() {
  try {
    await fetchWithErrorHandling("/api/non-existent-endpoint");
  } catch (error) {
    console.log("錯誤已被處理");
  }
}
```

### 測試網路斷線

在瀏覽器開發者工具中：
1. 打開 Network 面板
2. 選擇 "Offline" 選項
3. 應用程式應顯示網路斷線 Toast

---

## 開發模式 vs 生產模式

### 開發模式
- 顯示詳細錯誤訊息
- 顯示 Error Stack Trace
- 顯示 Error Digest
- Console 會記錄錯誤

### 生產模式
- 顯示友善的錯誤訊息
- 隱藏技術細節
- 可整合錯誤追蹤服務（如 Sentry）

---

## 注意事項

1. **ErrorBoundary 只能捕捉子組件的錯誤**
   - 無法捕捉自身錯誤
   - 無法捕捉事件處理器中的錯誤（需要 try-catch）
   - 無法捕捉非同步程式碼中的錯誤（需要 try-catch）

2. **網路狀態監控**
   - 只能偵測瀏覽器報告的網路狀態
   - 無法偵測網路速度過慢

3. **Toast 通知**
   - 一次只顯示一個 Toast（根據 use-toast.ts 設定）
   - 可調整 TOAST_LIMIT 和 TOAST_REMOVE_DELAY

---

## 進階功能

### 整合錯誤追蹤服務

在 `error-boundary.tsx` 和 `api-error-handler.ts` 中，您可以整合像 Sentry 這樣的錯誤追蹤服務：

```tsx
// error-boundary.tsx
componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
  // 記錄到 Sentry
  if (process.env.NODE_ENV === "production") {
    Sentry.captureException(error, { extra: errorInfo });
  }
}
```

```tsx
// api-error-handler.ts
export function showErrorToast(error: ApiError | Error | unknown) {
  // 記錄到 Sentry
  if (process.env.NODE_ENV === "production") {
    Sentry.captureException(error);
  }

  // 顯示 Toast...
}
```

---

## 支援

如有問題或建議，請聯繫開發團隊。

---

## 版本資訊

- **版本**: 1.0.0
- **建立日期**: 2025-11-26
- **最後更新**: 2025-11-26
