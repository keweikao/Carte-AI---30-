#!/bin/bash

# GitHub Actions Service Account 設置腳本
# 此腳本會創建 Service Account 並授予必要的權限

set -e

PROJECT_ID="gen-lang-client-0415289079"
SA_NAME="github-actions"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="github-actions-key.json"

echo "🚀 開始設置 GitHub Actions Service Account..."
echo ""

# 檢查是否已登入 gcloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ 請先登入 gcloud: gcloud auth login"
    exit 1
fi

# 設置專案
echo "📋 設置 GCP 專案: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# 創建 Service Account
echo ""
echo "👤 創建 Service Account: $SA_NAME"
if gcloud iam service-accounts describe $SA_EMAIL &>/dev/null; then
    echo "   ℹ️  Service Account 已存在，跳過創建"
else
    gcloud iam service-accounts create $SA_NAME \
        --display-name="GitHub Actions Deployer" \
        --description="Service Account for GitHub Actions CI/CD"
    echo "   ✅ Service Account 創建成功"
fi

# 授予權限
echo ""
echo "🔐 授予必要權限..."

ROLES=(
    "roles/run.admin"
    "roles/iam.serviceAccountUser"
    "roles/secretmanager.secretAccessor"
    "roles/cloudbuild.builds.editor"
    "roles/storage.admin"
)

for ROLE in "${ROLES[@]}"; do
    echo "   📌 授予 $ROLE"
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SA_EMAIL" \
        --role="$ROLE" \
        --quiet > /dev/null
done

echo "   ✅ 所有權限授予完成"

# 創建金鑰
echo ""
echo "🔑 創建 Service Account 金鑰..."
if [ -f "$KEY_FILE" ]; then
    echo "   ⚠️  金鑰文件已存在: $KEY_FILE"
    read -p "   是否覆蓋? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "   ℹ️  跳過金鑰創建"
        KEY_FILE=""
    else
        rm "$KEY_FILE"
    fi
fi

if [ -n "$KEY_FILE" ]; then
    gcloud iam service-accounts keys create $KEY_FILE \
        --iam-account=$SA_EMAIL
    echo "   ✅ 金鑰已創建: $KEY_FILE"
fi

# 顯示後續步驟
echo ""
echo "=" | tr '=' '='
echo "🎉 設置完成！"
echo "=" | tr '=' '='
echo ""
echo "📝 後續步驟："
echo ""
echo "1. 前往 GitHub Repository Settings:"
echo "   https://github.com/keweikao/Carte-AI---30-/settings/secrets/actions"
echo ""
echo "2. 點擊 'New repository secret'"
echo ""
echo "3. 添加 Secret:"
echo "   Name: GCP_SA_KEY"
if [ -n "$KEY_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "   Value: (複製以下內容)"
    echo ""
    echo "   ┌─────────────────────────────────────────┐"
    cat $KEY_FILE
    echo "   └─────────────────────────────────────────┘"
    echo ""
    echo "4. 刪除本地金鑰文件:"
    echo "   rm $KEY_FILE"
else
    echo "   Value: (從現有的 $KEY_FILE 複製內容)"
fi
echo ""
echo "5. 測試 GitHub Actions:"
echo "   - 推送代碼到 main 分支"
echo "   - 或在 GitHub Actions 頁面手動觸發 workflow"
echo ""
echo "🔗 GitHub Actions: https://github.com/keweikao/Carte-AI---30-/actions"
echo ""
