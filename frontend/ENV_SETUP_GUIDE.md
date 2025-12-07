# 環境變數設定指南

本專案使用環境變數來管理敏感資訊和配置。

## 📋 必要的環境變數

### NextAuth 配置

#### `GOOGLE_CLIENT_ID`
- **說明**: Google OAuth 2.0 Client ID
- **取得方式**: 
  1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
  2. 選擇專案或創建新專案
  3. 啟用 Google+ API
  4. 前往「憑證」→「建立憑證」→「OAuth 2.0 用戶端 ID」
  5. 應用程式類型選擇「網頁應用程式」
  6. 複製 Client ID

#### `GOOGLE_CLIENT_SECRET`
- **說明**: Google OAuth 2.0 Client Secret
- **取得方式**: 與 Client ID 一起生成

#### `NEXTAUTH_SECRET`
- **說明**: NextAuth.js 用於加密 session 的密鑰
- **生成方式**: 
  ```bash
  openssl rand -base64 32
  ```

#### `NEXTAUTH_URL`
- **說明**: 應用程式的完整 URL
- **本地開發**: `http://localhost:3000`
- **生產環境**: `https://your-domain.com`

### API 配置

#### `NEXT_PUBLIC_API_URL`
- **說明**: 後端 API 的 URL
- **本地開發**: `http://localhost:8000`
- **生產環境**: `https://dining-backend-1045148759148.asia-east1.run.app`

## 🚀 設定步驟

### 1. 複製範例文件

```bash
cp .env.example .env.local
```

### 2. 填入實際值

編輯 `.env.local` 文件，填入您的實際環境變數值。

### 3. 驗證設定

```bash
npm run dev
```

訪問 `http://localhost:3000` 確認應用程式正常運行。

## 🔒 安全注意事項

1. **絕對不要**將 `.env.local` 提交到 Git
2. `.env.local` 已在 `.gitignore` 中排除
3. 生產環境的環境變數應透過 Cloud Run 或 Secret Manager 設定
4. 定期輪換 `NEXTAUTH_SECRET`

## 📝 環境變數優先級

Next.js 會按以下順序載入環境變數：

1. `.env.local` (優先級最高，本地開發用)
2. `.env.production` (生產環境)
3. `.env.development` (開發環境)
4. `.env` (所有環境)

## 🌐 生產環境部署

### Cloud Run

在 Cloud Run 中設定環境變數：

```bash
gcloud run deploy dining-frontend \
  --set-env-vars="GOOGLE_CLIENT_ID=xxx,GOOGLE_CLIENT_SECRET=xxx,NEXTAUTH_SECRET=xxx,NEXTAUTH_URL=https://your-domain.com,NEXT_PUBLIC_API_URL=https://your-api-url.com"
```

### 使用 Secret Manager

更安全的方式是使用 Google Secret Manager：

```bash
# 創建 secret
gcloud secrets create GOOGLE_CLIENT_ID --data-file=-
# 輸入值後按 Ctrl+D

# 在 Cloud Run 中使用
gcloud run deploy dining-frontend \
  --update-secrets=GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest
```

## 🐛 常見問題

### Q: 為什麼我的 Google 登入失敗？

A: 檢查以下項目：
1. `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 是否正確
2. `NEXTAUTH_URL` 是否與當前 URL 匹配
3. Google Cloud Console 中的「已授權的重新導向 URI」是否包含 `{NEXTAUTH_URL}/api/auth/callback/google`

### Q: API 請求失敗怎麼辦？

A: 確認 `NEXT_PUBLIC_API_URL` 指向正確的後端 URL，並且後端服務正在運行。

### Q: 如何在 Vercel 部署？

A: 在 Vercel Dashboard 的專案設定中添加環境變數，或使用 `vercel env` 命令。

## 📚 相關文檔

- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [NextAuth.js Configuration](https://next-auth.js.org/configuration/options)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
