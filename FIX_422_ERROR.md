# 🔧 422 錯誤修復報告

## 問題診斷

### 錯誤訊息
```
POST https://dining-backend-1045148759148.asia-east1.run.app/v2/recommendations 422 (Unprocessable Content)
```

### 根本原因

發現了 **3 個問題**：

#### 1. **預算解析邏輯錯誤** ❌
**問題**: 前端使用滑桿輸入數字（例如 "500"），但 `recommendation/page.tsx` 中的解析邏輯還在使用舊的字串匹配方式。

**舊代碼**:
```typescript
let budgetAmount = 800;
if (budgetStr.includes("500")) budgetAmount = 500;
if (budgetStr.includes("1000")) budgetAmount = 1000;
if (budgetStr.includes("2000")) budgetAmount = 2000;
```

**修復**:
```typescript
const budgetAmount = parseInt(budgetStr) || (dining_style === "Shared" ? 2000 : 500);
```

#### 2. **React 依賴衝突** ❌
**問題**: `react-google-places-autocomplete@4.1.0` 不支援 React 19

**錯誤**:
```
peer react@"^16.8.0 || ^17.0.0 || ^18.0.0" from react-google-places-autocomplete@4.1.0
Conflicting peer dependency: react@18.3.1
```

**修復**:
- 移除 `react-google-places-autocomplete` 依賴
- 創建簡化版的 `RestaurantSearch` 組件

#### 3. **開發 Token 不被接受** ⚠️
**問題**: 後端的 Google Auth 驗證不接受開發 token

**測試結果**:
```
401 Unauthorized
"Token is malformed. Secure verification failed"
```

**說明**: 這是正常的，生產環境必須使用真實的 Google ID Token

---

## 修復內容

### 1. ✅ 更新預算解析邏輯
**文件**: `frontend/src/app/recommendation/page.tsx`

```typescript
// 修復前
let budgetAmount = 800;
if (budgetStr.includes("500")) budgetAmount = 500;
// ...

// 修復後
const budgetAmount = parseInt(budgetStr) || (dining_style === "Shared" ? 2000 : 500);
```

### 2. ✅ 移除不兼容的依賴
**文件**: `frontend/package.json`

```json
// 移除
"react-google-places-autocomplete": "^4.1.0"
```

### 3. ✅ 創建簡化版餐廳搜尋組件
**文件**: `frontend/src/components/restaurant-search.tsx`

```typescript
// 簡化版本，直接使用 Input 組件
export function RestaurantSearch({ onSelect, defaultValue }: RestaurantSearchProps) {
  const [value, setValue] = useState(defaultValue || '');
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    onSelect({ name: newValue });
  };

  return (
    <Input
      type="text"
      placeholder="例如：鼎泰豐、海底撈..."
      value={value}
      onChange={handleChange}
      className="text-lg py-6 bg-background border-border"
      autoFocus
    />
  );
}
```

---

## 部署狀態

### 後端
- ✅ 狀態: 正常運行
- ✅ 版本: `dining-backend-00029-vb7`
- ✅ CORS: 已正確配置

### 前端
- 🔄 狀態: 正在重新部署
- 🔄 修復: 預算解析 + 依賴衝突
- 🔄 預計完成: 5-10 分鐘

---

## 測試計劃

### 部署完成後測試步驟

1. **訪問前端**
   ```
   https://dining-frontend-u33peegeaa-de.a.run.app
   ```

2. **登入**
   - 使用 Google 帳號登入
   - ✅ 應該成功導向 `/input` 頁面

3. **填寫用餐資訊**
   - 餐廳名稱: 小時代牛排
   - 用餐方式: 個人
   - 人數: 1
   - 預算: 使用滑桿調整到 500
   - 點擊「開始生成推薦」

4. **預期結果**
   - ✅ 顯示載入動畫
   - ✅ 成功取得推薦結果
   - ✅ 顯示推薦菜色卡片

---

## 已知限制

### Google Places 自動完成功能暫時移除
由於 `react-google-places-autocomplete` 與 React 19 不兼容，目前使用簡化版的文字輸入。

**未來改進選項**:
1. 等待 `react-google-places-autocomplete` 更新支援 React 19
2. 使用其他兼容的 Google Places 套件
3. 自行實作 Google Places API 整合
4. 降級到 React 18（不推薦）

---

## 修復總結

| 問題 | 狀態 | 說明 |
|------|------|------|
| 預算解析錯誤 | ✅ 已修復 | 更新為 parseInt 解析 |
| React 依賴衝突 | ✅ 已修復 | 移除不兼容套件 |
| 餐廳搜尋組件 | ✅ 已修復 | 創建簡化版本 |
| 前端部署 | 🔄 進行中 | 預計 5-10 分鐘完成 |

---

**下一步**: 等待前端部署完成後進行完整測試
