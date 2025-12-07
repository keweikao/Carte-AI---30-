# GitHub Actions 設置指南

本專案使用 GitHub Actions 自動部署到 Google Cloud Run。

## 📋 Workflows

### 1. **CI Workflow** (`ci.yml`)
- **觸發時機**: 推送到 `main` 或 `develop` 分支，或創建 Pull Request
- **功能**:
  - ✅ 前端 ESLint 檢查
  - ✅ 後端 Black 和 Flake8 檢查
  - ✅ 前端構建測試

### 2. **Frontend Deployment** (`deploy-frontend.yml`)
- **觸發時機**: 
  - 推送到 `main` 分支且 `frontend/` 目錄有變更
  - 手動觸發 (workflow_dispatch)
- **部署目標**: `dining-frontend` (Cloud Run)
- **環境變數**: 從 Google Secret Manager 獲取

### 3. **Backend Deployment** (`deploy-backend.yml`)
- **觸發時機**: 
  - 推送到 `main` 分支且後端文件有變更
  - 手動觸發 (workflow_dispatch)
- **部署目標**: `dining-backend` (Cloud Run)
- **環境變數**: 從 Google Secret Manager 獲取

## 🔐 必要的 GitHub Secrets

您需要在 GitHub Repository 設置中添加以下 Secret：

### `GCP_SA_KEY`
Google Cloud Service Account 的 JSON 金鑰

#### 創建步驟：

1. **創建 Service Account**
   ```bash
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions Deployer"
   ```

2. **授予權限**
   ```bash
   # Cloud Run Admin
   gcloud projects add-iam-policy-binding gen-lang-client-0415289079 \
     --member="serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com" \
     --role="roles/run.admin"

   # Service Account User
   gcloud projects add-iam-policy-binding gen-lang-client-0415289079 \
     --member="serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"

   ```
   # Secret Manager Secret Accessor
   gcloud projects add-iam-policy-binding gen-lang-client-0415289079 \
     --member="serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"

   # Cloud Build Editor (for building containers)
   gcloud projects add-iam-policy-binding gen-lang-client-0415289079 \
     --member="serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com" \
     --role="roles/cloudbuild.builds.editor"

   # Storage Admin (for Cloud Build artifacts)
   gcloud projects add-iam-policy-binding gen-lang-client-0415289079 \
     --member="serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   ```

3. **創建並下載金鑰**
   ```bash
   gcloud iam service-accounts keys create github-actions-key.json \
     --iam-account=github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com
   ```

4. **添加到 GitHub Secrets**
   - 前往 GitHub Repository → Settings → Secrets and variables → Actions
   - 點擊 "New repository secret"
   - Name: `GCP_SA_KEY`
   - Value: 複製 `github-actions-key.json` 的完整內容
   - 點擊 "Add secret"

5. **刪除本地金鑰文件**
   ```bash
   rm github-actions-key.json
   ```

## 🚀 使用方式

### 自動部署
推送代碼到 `main` 分支時，GitHub Actions 會自動：
1. 運行 CI 檢查（linting 和 build）
2. 如果前端有變更，自動部署前端
3. 如果後端有變更，自動部署後端

### 手動部署
1. 前往 GitHub Repository → Actions
2. 選擇要運行的 workflow（Deploy Frontend 或 Deploy Backend）
3. 點擊 "Run workflow"
4. 選擇分支（通常是 `main`）
5. 點擊 "Run workflow" 確認

## 📊 監控部署

### 查看部署狀態

1. 前往 GitHub Repository → Actions
2. 點擊最近的 workflow run
3. 查看每個步驟的日誌

### 查看部署結果

- **前端**: https://dining-frontend-u33peegeaa-de.a.run.app
- **後端**: https://dining-backend-1045148759148.asia-east1.run.app

### 查看 Cloud Run 日誌

```bash
# 前端日誌
gcloud run services logs read dining-frontend --region=asia-east1 --limit=50

# 後端日誌
gcloud run services logs read dining-backend --region=asia-east1 --limit=50
```

## 🔧 故障排除

### 部署失敗
1. 檢查 GitHub Actions 日誌
2. 確認 Service Account 權限正確
3. 確認 Secret Manager 中的 secrets 存在
4. 檢查 Cloud Run 配額

### Secret 訪問失敗
```bash
# 測試 Service Account 是否能訪問 secrets
gcloud secrets versions access latest --secret='GOOGLE_CLIENT_ID' \
  --impersonate-service-account=github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com
```

### 權限問題
```bash
# 查看 Service Account 的權限
gcloud projects get-iam-policy gen-lang-client-0415289079 \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:github-actions@gen-lang-client-0415289079.iam.gserviceaccount.com"
```

## 📝 最佳實踐

1. **分支策略**
   - `main`: 生產環境，自動部署
   - `develop`: 開發環境，CI 檢查但不部署
   - Feature branches: 創建 PR 到 `develop`

2. **環境變數管理**
   - 所有敏感資訊存儲在 Google Secret Manager
   - 不要在代碼中硬編碼任何 secrets

3. **部署頻率**
   - 小步快跑，頻繁部署
   - 每次部署前確保 CI 通過

4. **回滾策略**
   - Cloud Run 保留舊版本
   - 可以快速回滾到之前的版本

## 🔗 相關資源

- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [Google Cloud Run 文檔](https://cloud.google.com/run/docs)
- [Secret Manager 文檔](https://cloud.google.com/secret-manager/docs)
