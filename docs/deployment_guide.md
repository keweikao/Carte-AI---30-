# Cloud Run Deployment Guide (with Secret Manager)

是的，將 API Key 存放在 Google Secret Manager 並在 Cloud Run 中掛載是**最佳實踐**。這樣可以避免將敏感資訊寫入程式碼或 Docker 映像檔中。

## 1. 準備工作

確保您已經安裝 `gcloud` CLI 並已登入。

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

## 2. 設定 Secret Manager

將您的 API Key 儲存到 Secret Manager。

```bash
# 啟用 Secret Manager API
gcloud services enable secretmanager.googleapis.com

# 建立 Secret (如果尚未建立)
gcloud secrets create gemini-api-key --replication-policy="automatic"

# 新增 Secret 版本 (將您的真實 API Key 放入)
echo -n "YOUR_ACTUAL_GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=-
```

重複上述步驟為其他敏感變數建立 Secret (例如 `GOOGLE_API_KEY`, `GOOGLE_CLIENT_ID` 等)。

## 3. 授權 Cloud Run 存取 Secret

Cloud Run 預設使用 Compute Engine default service account。您需要授權該帳號讀取 Secret。

```bash
# 取得 Project Number
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")

# 授權讀取 gemini-api-key
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## 4. 部署到 Cloud Run

使用 `gcloud run deploy` 並透過 `--set-secrets` 參數將 Secret 掛載為環境變數。

```bash
gcloud run deploy ai-dining-backend \
    --source . \
    --region asia-east1 \
    --allow-unauthenticated \
    --set-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
    --set-env-vars="GOOGLE_CLIENT_ID=your_client_id,SEARCH_ENGINE_ID=your_search_engine_id"
```

*   `GEMINI_API_KEY=gemini-api-key:latest`: 將 Secret `gemini-api-key` 的最新版本映射到環境變數 `GEMINI_API_KEY`。
*   非敏感變數 (如 `SEARCH_ENGINE_ID`) 可以直接用 `--set-env-vars` 設定。

## 5. 前端部署 (Next.js)

如果前端也部署到 Cloud Run，您需要建立另一個 `Dockerfile` (在 `frontend/` 目錄下)，並執行類似的部署步驟。

注意：前端的環境變數 (如 `NEXT_PUBLIC_API_URL`) 通常在 Build Time 就需要，或者在 Runtime 透過 `publicRuntimeConfig` 注入。如果是 Server Component 使用的 API Key，則同樣可以使用 Secret Manager。
