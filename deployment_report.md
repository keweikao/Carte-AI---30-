# 部署報告 - 忠南飯館測試

**日期**: 2025-12-03 16:20  
**目標**: 部署最新版本到 staging 環境以測試忠南飯館 6 人商務聚餐推薦

---

## ❌ 部署失敗

### 錯誤訊息
```
ERROR: The user-provided container failed to start and listen on the port 
defined provided by the PORT=8080 environment variable within the allocated timeout.
```

### 失敗的 Revision
- **Revision**: `oderwhat-staging-00036-wzn`
- **Build ID**: `0de60398-2b4b-434d-9296-e21a287e8f7e`
- **Image**: `asia-east1-docker.pkg.dev/gen-lang-client-0415289079/oderwhat-staging-repo/oderwhat-staging:0de60398-2b4b-434d-9296-e21a287e8f7e`

### 日誌連結
```
https://console.cloud.google.com/logs/viewer?project=gen-lang-client-0415289079&resource=cloud_run_revision/service_name/oderwhat-staging/revision_name/oderwhat-staging-00036-wzn
```

---

## 🔍 可能原因

### 1. 啟動超時
容器可能需要更長時間來啟動（安裝依賴、初始化服務等）

### 2. 環境變數缺失
根據 `VISION_API_FIX_SUMMARY.md`，需要以下環境變數：
- ✅ `GEMINI_API_KEY` (已設定)
- ✅ `APIFY_API_TOKEN` (已設定)
- ❌ `SERPER_API_KEY` (未在 cloudbuild.yaml 中)
- ❌ `JINA_API_KEY` (未在 cloudbuild.yaml 中)
- ❌ `GOOGLE_API_KEY` (未在 cloudbuild.yaml 中)

### 3. 依賴問題
某些 Python 套件可能無法正確安裝或初始化失敗

---

## 💡 建議修復方案

### 方案 1: 更新 cloudbuild.yaml（推薦）

在 `cloudbuild.yaml` 的 Deploy 步驟中加入所有必要的 secrets：

```yaml
- '--update-secrets'
- 'GEMINI_API_KEY=GEMINI_API_KEY:latest'
- '--update-secrets'
- 'APIFY_API_TOKEN=APIFY_API_TOKEN:latest'
- '--update-secrets'
- 'SERPER_API_KEY=SERPER_API_KEY:latest'
- '--update-secrets'
- 'JINA_API_KEY=JINA_API_KEY:latest'
- '--update-secrets'
- 'GOOGLE_API_KEY=GOOGLE_API_KEY:latest'
```

### 方案 2: 增加啟動超時時間

在 Deploy 步驟中加入：

```yaml
- '--timeout'
- '10m'
```

### 方案 3: 檢查 Cloud Run 日誌

查看詳細的啟動錯誤：

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=oderwhat-staging AND resource.labels.revision_name=oderwhat-staging-00036-wzn" \
  --limit 50 \
  --project=gen-lang-client-0415289079 \
  --format=json
```

---

## 🎯 立即行動建議

### 選項 A: 修復並重新部署

1. 更新 `cloudbuild.yaml` 加入所有 secrets
2. 重新執行部署
3. 監控日誌確認成功

### 選項 B: 使用現有的 staging 環境

如果之前的 revision 還在運行，可以直接使用：

```bash
# 檢查當前運行的 revision
gcloud run revisions list \
  --service=oderwhat-staging \
  --region=asia-east1 \
  --project=gen-lang-client-0415289079

# 如果有舊的 revision 在運行，可以直接測試
curl "https://oderwhat-staging-u33peegeaa-de.a.run.app/health"
```

### 選項 C: 本地測試後再部署

1. 在本地設定所有環境變數
2. 執行 `test_zhongnan_production_flow.py`
3. 確認所有功能正常後再部署

---

## 📝 下一步

請告訴我您想要：

1. **修復 cloudbuild.yaml 並重新部署**
   - 我會更新配置檔案
   - 加入所有必要的 secrets
   - 重新執行部署

2. **查看詳細日誌診斷問題**
   - 我會執行 gcloud logging 命令
   - 分析具體的錯誤原因
   - 提供針對性的修復方案

3. **使用現有環境測試**
   - 如果舊的 revision 還在運行
   - 直接測試忠南飯館案例
   - 產生推薦菜單

請選擇您偏好的方案，我會立即執行！
