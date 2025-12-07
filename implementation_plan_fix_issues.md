# 修復前端搜尋與 UI 問題實作計畫

## 階段一：修復自動送出問題

1.  **修改 `frontend/src/components/restaurant-search.tsx`**:
    *   新增 `onChange` prop: `(value: string) => void`。
    *   在內部的 `handleChange` 中呼叫 `props.onChange(newValue)`。
    *   **移除** `handleChange` 中對 `onSelect` 的呼叫。
    *   保留 `handleKeyDown` 中的 `Enter` 觸發 `onSelect`。

2.  **修改 `frontend/src/app/input/page.tsx`**:
    *   更新 `RestaurantSearch` 的使用方式：
        *   傳遞 `onChange` prop，用來更新 `formData.restaurant_name`。
        *   保留 `onSelect` prop，但它現在只會在使用者按下 Enter 時觸發，邏輯保持為「更新名稱並跳轉」。

## 階段二：修復 API 422 錯誤

1.  **修改 `frontend/src/app/recommendation/page.tsx`**:
    *   在 `fetchData` 函數中，增加 `mapDiningStyle` 輔助邏輯。
    *   將 `searchParams.get("mode")` 的值轉換為 `"Shared"` 或 `"Individual"`。
    *   更新 `requestData` 物件使用轉換後的值。

## 階段三：修復錯誤頁面 UI

1.  **修改 `frontend/src/app/recommendation/page.tsx`**:
    *   定位到 `ErrorState` 元件。
    *   為 `Button` 新增明確的 `className`，確保背景色和文字顏色對比度（例如使用 `bg-primary text-primary-foreground` 並確認這些變數的值）。

2.  **修改 `frontend/src/app/error.tsx`**:
    *   將「返回首頁」按鈕的 `variant="outline"` 改為 `variant="secondary"` 或移除 variant 並手動設定高對比樣式。

## 階段四：驗證

1.  手動測試輸入流程。
2.  驗證 API 請求 payload。
3.  檢查錯誤頁面樣式。
