# 修復前端搜尋與 UI 問題規格書

## 1. 問題描述

### 1.1 自動送出問題
- **現狀**: 在輸入頁面輸入餐廳名稱時，每輸入一個字元就會自動觸發跳轉到下一步驟。
- **原因**: `RestaurantSearch` 元件在 `onChange` 事件中直接呼叫 `onSelect`，而父層元件 `InputPage` 在接收到 `onSelect` 後會自動執行 `setStep(2)`。
- **目標**: 使用者應能完整輸入餐廳名稱，並透過點擊「下一步」按鈕或按下 Enter 鍵來確認輸入，而非輸入即送出。

### 1.2 HTTP 422 錯誤
- **現狀**: 提交搜尋後，後端 API 回傳 HTTP 422 Unprocessable Content 錯誤。
- **原因**: 前端傳遞給 `/v2/recommendations` API 的參數格式不符合後端 Pydantic 模型 `UserInputV2` 的要求。
    - `dining_style`: 前端傳遞 "sharing" / "individual" (小寫)，後端要求 "Shared" / "Individual" (首字母大寫)。
- **目標**: 確保前端傳遞的資料完全符合後端 API 規格，成功取得推薦結果。

### 1.3 錯誤頁面 UI 問題
- **現狀**: 錯誤頁面上的「回到首頁」或「返回重新設定」按鈕文字顏色為白色，與背景顏色相同或過於接近，導致無法辨識。
- **原因**: 按鈕樣式與背景顏色的搭配在特定情況下（如錯誤狀態）對比度不足。
- **目標**: 確保錯誤頁面的按鈕文字清晰可見，符合無障礙設計標準。

## 2. 修改規格

### 2.1 `frontend/src/components/restaurant-search.tsx`
- **移除**: `handleChange` 中的 `onSelect` 呼叫。
- **新增**: 僅更新內部 state `value`。
- **新增**: 在 `handleKeyDown` 中，當按下 `Enter` 鍵且有輸入內容時，呼叫 `onSelect`。

### 2.2 `frontend/src/app/input/page.tsx`
- **修改**: `RestaurantSearch` 的 `onSelect` prop 邏輯。
    - 雖然 `RestaurantSearch` 改為只在 Enter 時觸發 `onSelect`，但為了保險起見，`InputPage` 應確保只有在收到有效名稱時才跳轉。
    - 保留原本的 `setTimeout` 自動跳轉邏輯，但現在它只會被 `Enter` 鍵觸發。
    - 使用者主要透過點擊「下一步」按鈕來前進。
- **修改**: `RestaurantSearch` 的 `onChange` 行為（如果需要即時更新父層 state 以啟用「下一步」按鈕）。
    - 由於 `RestaurantSearch` 目前沒有 `onChange` prop，需要新增 `onChange` prop 來將輸入值同步回父層 `formData.restaurant_name`，以便「下一步」按鈕能正確啟用/停用。

### 2.3 `frontend/src/app/recommendation/page.tsx`
- **修改**: 在建構 `requestData` 之前，正確轉換 `dining_style`。
    - 將 URL 參數 `mode` ("sharing", "individual") 映射為 API 枚舉 ("Shared", "Individual")。
- **修改**: `ErrorState` 元件。
    - 為 `Button` 強制指定高對比度的樣式，例如 `variant="default"` 並確保背景色正確。

### 2.4 `frontend/src/app/error.tsx` (Global Error Page)
- **修改**: 檢查並調整按鈕樣式，確保在淺色背景上有深色文字，或深色背景上有淺色文字。建議移除 `variant="outline"` 或明確指定背景色。

## 3. 驗證計畫
1.  **自動送出**: 進入輸入頁，輸入 "M"，確認不會跳轉。輸入 "McDonalds"，確認不會跳轉。點擊「下一步」，確認跳轉。
2.  **API 請求**: 完成輸入並提交，觀察 Network Tab，確認 POST 请求的 payload 中 `dining_style` 為 "Shared" 或 "Individual"。確認 API 回傳 200 OK。
3.  **UI 檢查**: 暫時斷網或模擬 API 錯誤，觸發錯誤頁面，確認按鈕文字清晰可見。
