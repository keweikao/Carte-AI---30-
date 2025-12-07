# Google SSO 錯誤診斷報告

## 🔍 問題診斷

### 發現的問題

1. **❌ NEXTAUTH_URL 配置錯誤**
   - **當前值**: `SERVICE_URL` (字串常量)
   - **應該是**: `https://dining-frontend-1045148759148.asia-east1.run.app`
   - **影響**: NextAuth.js 無法正確處理 OAuth 回調，導致登入失敗

2. **⚠️ 環境變數未使用 Secret Manager**
   - 當前使用 `--set-env-vars` 直接設定明文值
   - 應該使用 `--set-secrets` 從 Secret Manager 掛載

### 當前配置

```bash
# 當前前端環境變數
GOOGLE_CLIENT_ID=1045148759148-u90ianu8j1vvep9nahm3862ee0nva5ps.apps.googleusercontent.com
NEXTAUTH_URL=SERVICE_URL  # ❌ 錯誤！
NEXTAUTH_SECRET=P/L0bkW2BwJhkMczX7VMzMXEWhc8/2qCvxcpyqDEgHo=
GOOGLE_CLIENT_SECRET=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
```

## 🔧 修復方案

### 方案 A：快速修復（推薦）

使用提供的腳本重新部署：

```bash
cd /Users/stephen/Desktop/OderWhat/frontend
./fix_oauth_deployment.sh
```

這個腳本會：
1. ✅ 從 Secret Manager 讀取所有敏感資訊
2. ✅ 自動取得當前服務 URL
3. ✅ 正確設定 `NEXTAUTH_URL`
4. ✅ 重新部署前端服務

### 方案 B：手動修復

```bash
# 1. 取得服務 URL
SERVICE_URL=$(gcloud run services describe dining-frontend \
  --region=asia-east1 \
  --format="value(status.url)")

# 2. 從 Secret Manager 取得環境變數
GOOGLE_CLIENT_ID=$(gcloud secrets versions access latest --secret="GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=$(gcloud secrets versions access latest --secret="GOOGLE_CLIENT_SECRET")
NEXTAUTH_SECRET=$(gcloud secrets versions access latest --secret="NEXTAUTH_SECRET")

# 3. 重新部署
cd /Users/stephen/Desktop/OderWhat/frontend

gcloud run deploy dining-frontend \
  --source . \
  --region=asia-east1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET,NEXTAUTH_SECRET=$NEXTAUTH_SECRET,NEXTAUTH_URL=$SERVICE_URL,NEXT_PUBLIC_API_URL=https://dining-backend-1045148759148.asia-east1.run.app"
```

### 方案 C：使用 Secret Manager（最佳實踐）

```bash
cd /Users/stephen/Desktop/OderWhat/frontend

gcloud run deploy dining-frontend \
  --source . \
  --region=asia-east1 \
  --allow-unauthenticated \
  --set-secrets="GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest,GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest,NEXTAUTH_SECRET=NEXTAUTH_SECRET:latest" \
  --set-env-vars="NEXTAUTH_URL=https://dining-frontend-1045148759148.asia-east1.run.app,NEXT_PUBLIC_API_URL=https://dining-backend-1045148759148.asia-east1.run.app"
```

## 📋 部署後檢查清單

### 1. 驗證環境變數

```bash
gcloud run services describe dining-frontend \
  --region=asia-east1 \
  --format="get(spec.template.spec.containers[0].env)"
```

應該看到：
- ✅ `NEXTAUTH_URL` = 實際的服務 URL
- ✅ `GOOGLE_CLIENT_ID` = 正確的 Client ID
- ✅ `GOOGLE_CLIENT_SECRET` = 正確的 Secret
- ✅ `NEXTAUTH_SECRET` = 正確的 Secret

### 2. 檢查 Google OAuth 設定

前往 [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)

確認 OAuth 2.0 Client ID 的**授權重新導向 URI** 包含：

```
https://dining-frontend-1045148759148.asia-east1.run.app/api/auth/callback/google
```

如果有自訂網域：
```
https://www.carte.tw/api/auth/callback/google
```

### 3. 測試登入流程

1. 訪問 https://dining-frontend-1045148759148.asia-east1.run.app
2. 點擊「使用 Google 登入」
3. 選擇 Google 帳號
4. 應該成功重新導向到 `/input` 頁面

## 🐛 餐廳搜尋錯誤

### 可能原因

1. **後端 API 錯誤**
   - 檢查後端日誌：
     ```bash
     gcloud run services logs read dining-backend --region=asia-east1 --limit=50
     ```

2. **API Key 問題**
   - 檢查後端環境變數：
     ```bash
     gcloud run services describe dining-backend \
       --region=asia-east1 \
       --format="get(spec.template.spec.containers[0].env)"
     ```

3. **CORS 問題**
   - 確認後端 `main.py` 的 CORS 設定包含前端 URL

### 檢查步驟

```bash
# 1. 檢查後端服務狀態
gcloud run services describe dining-backend --region=asia-east1

# 2. 查看最近的錯誤日誌
gcloud run services logs read dining-backend \
  --region=asia-east1 \
  --limit=100 \
  --format="table(timestamp,severity,textPayload)"

# 3. 測試後端 API
curl -X POST https://dining-backend-1045148759148.asia-east1.run.app/recommendations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_GOOGLE_ID_TOKEN" \
  -d '{
    "restaurant_name": "鼎泰豐",
    "party_size": 2,
    "dining_style": "Shared",
    "budget": {"type": "Total", "amount": 1000}
  }'
```

## 📝 總結

### 主要問題
1. ❌ `NEXTAUTH_URL=SERVICE_URL` 導致 OAuth 回調失敗
2. ⚠️ 未使用 Secret Manager 最佳實踐

### 修復步驟
1. 執行 `./fix_oauth_deployment.sh`
2. 驗證環境變數配置
3. 檢查 Google OAuth 重新導向 URI
4. 測試登入流程
5. 如果餐廳搜尋仍有問題，檢查後端日誌

### 預期結果
- ✅ Google SSO 登入成功
- ✅ 可以進入 `/input` 頁面
- ✅ 可以提交餐廳搜尋
- ✅ 可以看到推薦結果
