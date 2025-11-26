# 🔧 修復 OAuth Redirect URI 錯誤

## ❌ 錯誤訊息
```
Error 400: redirect_uri_mismatch
```

## 🔍 問題原因

Cloud Run 服務有兩個 URL：
1. **自動生成的 URL**: `https://dining-frontend-u33peegeaa-de.a.run.app`
2. **項目專屬 URL**: `https://dining-frontend-1045148759148.asia-east1.run.app`

NextAuth 使用的是自動生成的 URL，但 Google OAuth 設定中可能沒有包含這個 URL。

## ✅ 解決方案

### 步驟 1: 更新 Google OAuth 設定（必須手動完成）

1. **前往 Google Cloud Console**:
   https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0415289079

2. **找到 OAuth 2.0 Client ID**:
   - 點擊名稱為 `1045148759148-u90ianu8j1vvep9nahm3862ee0nva5ps.apps.googleusercontent.com` 的 Client ID

3. **添加授權重新導向 URI**:
   
   在「已授權的重新導向 URI」區域，添加以下 **3 個** URIs：

   ```
   https://dining-frontend-u33peegeaa-de.a.run.app/api/auth/callback/google
   https://dining-frontend-1045148759148.asia-east1.run.app/api/auth/callback/google
   https://www.carte.tw/api/auth/callback/google
   ```

4. **儲存變更**:
   - 點擊「儲存」按鈕
   - ⚠️ **等待 5-10 分鐘**讓 Google 更新設定

### 步驟 2: 驗證環境變數（已完成 ✅）

前端環境變數已更新為：
```bash
NEXTAUTH_URL=https://dining-frontend-u33peegeaa-de.a.run.app
NEXT_PUBLIC_API_URL=https://dining-backend-u33peegeaa-de.a.run.app
GOOGLE_CLIENT_ID=1045148759148-u90ianu8j1vvep9nahm3862ee0nva5ps.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
NEXTAUTH_SECRET=P/L0bkW2BwJhkMczX7VMzMXEWhc8/2qCvxcpyqDEgHo=
```

## 🧪 測試步驟

### 等待 5-10 分鐘後測試

1. **清除瀏覽器快取和 Cookies**
   - Chrome: `Ctrl+Shift+Delete` (Windows) 或 `Cmd+Shift+Delete` (Mac)
   - 選擇「Cookie 和其他網站資料」
   - 點擊「清除資料」

2. **重新訪問網站**:
   https://dining-frontend-u33peegeaa-de.a.run.app
   
   或
   
   https://dining-frontend-1045148759148.asia-east1.run.app

3. **測試登入**:
   - 點擊「使用 Google 登入」
   - 選擇 Google 帳號
   - ✅ 應該成功登入並導向 `/input` 頁面

## 📸 Google Console 設定截圖指南

### 在 OAuth 2.0 Client ID 設定頁面中：

```
已授權的重新導向 URI
┌─────────────────────────────────────────────────────────────────┐
│ https://dining-frontend-u33peegeaa-de.a.run.app/api/auth/cal...│ [X]
│ https://dining-frontend-1045148759148.asia-east1.run.app/api...│ [X]
│ https://www.carte.tw/api/auth/callback/google                  │ [X]
└─────────────────────────────────────────────────────────────────┘
                                                          [+ 新增 URI]
```

## 🔍 驗證設定

### 檢查當前 Redirect URIs

在 Google Cloud Console 中，確認已添加的 URIs：

```bash
# 應該包含以下 3 個 URIs：
✅ https://dining-frontend-u33peegeaa-de.a.run.app/api/auth/callback/google
✅ https://dining-frontend-1045148759148.asia-east1.run.app/api/auth/callback/google
✅ https://www.carte.tw/api/auth/callback/google
```

## ⚠️ 常見問題

### Q: 為什麼有兩個不同的 URL？

A: Cloud Run 提供兩種 URL：
- **自動生成**: `*-u33peegeaa-de.a.run.app` - 每次部署可能改變
- **項目專屬**: `*-1045148759148.asia-east1.run.app` - 固定不變

建議兩個都添加以確保兼容性。

### Q: 添加後還是出現錯誤？

A: 
1. 確認已儲存設定
2. 等待 5-10 分鐘讓 Google 更新
3. 清除瀏覽器快取和 Cookies
4. 使用無痕模式測試

### Q: 如何確認 NEXTAUTH_URL 是否正確？

A: 執行以下命令：
```bash
gcloud run services describe dining-frontend \
  --region=asia-east1 \
  --format="get(spec.template.spec.containers[0].env)" | grep NEXTAUTH_URL
```

應該顯示：
```
{'name': 'NEXTAUTH_URL', 'value': 'https://dining-frontend-u33peegeaa-de.a.run.app'}
```

## 📝 總結

### 已完成 ✅
- ✅ 更新前端環境變數 `NEXTAUTH_URL`
- ✅ 識別正確的 Redirect URIs

### 需要您手動完成 ⚠️
- ⚠️ 在 Google Cloud Console 添加 3 個 Redirect URIs
- ⚠️ 等待 5-10 分鐘
- ⚠️ 清除瀏覽器快取後測試

### 完成後
- ✅ Google SSO 登入應該正常運作
- ✅ 可以開始使用餐廳推薦功能

---

**重要**: 請務必在 Google Cloud Console 中添加所有 3 個 Redirect URIs，否則登入仍會失敗。
