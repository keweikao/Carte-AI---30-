# 部署指南 - 避免專案混淆

## 問題說明

當管理多個 Google Cloud 專案時，容易發生以下問題：
1. 部署到錯誤的專案
2. 使用錯誤的服務帳號
3. Artifact Registry 路徑錯誤

## 當前專案架構

### 專案 1: sales-ai-automation-v2 (497329205771)
- **用途**: 主要開發和測試環境
- **服務**:
  - `dining-backend`: https://dining-backend-497329205771.asia-east1.run.app
  - `dining-agent-service`: https://dining-agent-service-497329205771.asia-east1.run.app
- **Artifact Registry**: `asia-east1-docker.pkg.dev/sales-ai-automation-v2/sales-ai-automation-v2`
- **服務帳號**: `497329205771-compute@developer.gserviceaccount.com`

### 專案 2: gen-lang-client-0415289079 (1045148759148)
- **用途**: 生產環境（前端配置指向此處）
- **服務**:
  - `dining-backend`: https://dining-backend-1045148759148.asia-east1.run.app
  - `dining-frontend`: https://dining-frontend-1045148759148.asia-east1.run.app
- **服務帳號**: `1045148759148-compute@developer.gserviceaccount.com`

## 解決方案

### 方案 1：使用專案特定的配置文件（推薦）

創建兩個獨立的配置文件：

#### `cloudbuild-prod-backend-v2.yaml` (for sales-ai-automation-v2)
```yaml
# 明確標註專案
# TARGET PROJECT: sales-ai-automation-v2 (497329205771)

steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'asia-east1-docker.pkg.dev/sales-ai-automation-v2/sales-ai-automation-v2/dining-backend-prod:$BUILD_ID', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'asia-east1-docker.pkg.dev/sales-ai-automation-v2/sales-ai-automation-v2/dining-backend-prod:$BUILD_ID']
  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'dining-backend'
      - '--image'
      - 'asia-east1-docker.pkg.dev/sales-ai-automation-v2/sales-ai-automation-v2/dining-backend-prod:$BUILD_ID'
      - '--region'
      - 'asia-east1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '2Gi'
      - '--timeout'
      - '300s'
      - '--service-account'
      - '497329205771-compute@developer.gserviceaccount.com'
      - '--set-secrets'
      - 'SERPER_API_KEY=SERPER_API_KEY:latest,JINA_API_KEY=JINA_API_KEY:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest,APIFY_API_TOKEN=APIFY_API_TOKEN:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest'
```

#### `cloudbuild-prod-backend-gen.yaml` (for gen-lang-client-0415289079)
```yaml
# 明確標註專案
# TARGET PROJECT: gen-lang-client-0415289079 (1045148759148)

steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'asia-east1-docker.pkg.dev/gen-lang-client-0415289079/dining-backend/prod:$BUILD_ID', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'asia-east1-docker.pkg.dev/gen-lang-client-0415289079/dining-backend/prod:$BUILD_ID']
  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'dining-backend'
      - '--image'
      - 'asia-east1-docker.pkg.dev/gen-lang-client-0415289079/dining-backend/prod:$BUILD_ID'
      - '--region'
      - 'asia-east1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '2Gi'
      - '--timeout'
      - '300s'
      - '--service-account'
      - '1045148759148-compute@developer.gserviceaccount.com'
      - '--set-secrets'
      - 'SERPER_API_KEY=SERPER_API_KEY:latest,JINA_API_KEY=JINA_API_KEY:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest,APIFY_API_TOKEN=APIFY_API_TOKEN:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest'
```

### 方案 2：使用部署腳本

創建 `deploy.sh` 腳本：

```bash
#!/bin/bash

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 顯示當前專案
echo -e "${YELLOW}當前 gcloud 專案:${NC}"
CURRENT_PROJECT=$(gcloud config get-value project)
echo -e "${GREEN}$CURRENT_PROJECT${NC}"
echo ""

# 選擇部署目標
echo "請選擇部署目標:"
echo "1) sales-ai-automation-v2 (開發/測試)"
echo "2) gen-lang-client-0415289079 (生產環境)"
read -p "輸入選項 (1 或 2): " choice

case $choice in
  1)
    PROJECT="sales-ai-automation-v2"
    CONFIG="cloudbuild-prod-backend-v2.yaml"
    ;;
  2)
    PROJECT="gen-lang-client-0415289079"
    CONFIG="cloudbuild-prod-backend-gen.yaml"
    ;;
  *)
    echo -e "${RED}無效選項${NC}"
    exit 1
    ;;
esac

# 確認
echo -e "${YELLOW}即將部署到:${NC} ${GREEN}$PROJECT${NC}"
echo -e "${YELLOW}使用配置:${NC} ${GREEN}$CONFIG${NC}"
read -p "確認繼續? (y/n): " confirm

if [ "$confirm" != "y" ]; then
  echo "已取消"
  exit 0
fi

# 執行部署
echo -e "${GREEN}開始部署...${NC}"
gcloud builds submit --config=$CONFIG . --project=$PROJECT
```

### 方案 3：在命令中明確指定專案

每次部署時都明確指定專案：

```bash
# 部署到 sales-ai-automation-v2
gcloud builds submit \
  --config=cloudbuild-prod-backend.yaml \
  --project=sales-ai-automation-v2 \
  .

# 部署到 gen-lang-client-0415289079
gcloud builds submit \
  --config=cloudbuild-prod-backend.yaml \
  --project=gen-lang-client-0415289079 \
  .
```

## 最佳實踐

1. **在配置文件頂部添加註釋**，明確標註目標專案
2. **使用不同的配置文件名稱**，例如 `-v2.yaml` 和 `-gen.yaml`
3. **創建部署腳本**，在部署前顯示確認訊息
4. **設置 gcloud 配置**：
   ```bash
   # 創建專案特定的配置
   gcloud config configurations create sales-ai-v2
   gcloud config set project sales-ai-automation-v2
   
   gcloud config configurations create gen-lang-prod
   gcloud config set project gen-lang-client-0415289079
   
   # 切換配置
   gcloud config configurations activate sales-ai-v2
   gcloud config configurations activate gen-lang-prod
   ```

5. **在 CI/CD 中使用環境變數**，明確指定專案

## 當前建議

基於您的前端配置指向 `https://dining-backend-1045148759148.asia-east1.run.app`，建議：

1. **統一使用 `sales-ai-automation-v2` 專案**
2. **更新前端配置**，指向 `https://dining-backend-497329205771.asia-east1.run.app`
3. **或者**，在 `gen-lang-client-0415289079` 專案中創建必要的 Artifact Registry

## 快速檢查清單

部署前檢查：
- [ ] 確認當前 gcloud 專案：`gcloud config get-value project`
- [ ] 確認配置文件中的專案 ID
- [ ] 確認 Artifact Registry 路徑
- [ ] 確認服務帳號
- [ ] 確認 Secret Manager 權限已設置
