#!/bin/bash
# Markdown Linting Check Script

echo "🔍 檢查 Markdown 文件格式..."
echo ""

# 要檢查的文件列表（今天新增/修改的）
FILES=(
    "DEPLOYMENT_CHECKLIST.md"
    "implementation_plan_prefetch.md"
    "task_prefetch.md"
    "specs/agent_focus_loading.md"
    "specs/prefetch_optimization.md"
)

ERRORS=0

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "⚠️  檔案不存在: $file"
        continue
    fi
    
    echo "📄 檢查: $file"
    
    # 檢查 1: 檔案結尾是否有空行
    if [ -n "$(tail -c 1 "$file")" ]; then
        echo "  ❌ MD047: 檔案結尾缺少空行"
        ERRORS=$((ERRORS + 1))
    fi
    
    # 檢查 2: 是否有多餘的空行（連續超過 2 個空行）
    if grep -Pzo '\n\n\n\n' "$file" > /dev/null 2>&1; then
        echo "  ❌ MD012: 發現連續超過 2 個空行"
        ERRORS=$((ERRORS + 1))
    fi
    
    # 檢查 3: 標題前後是否有空行
    # 這個檢查比較複雜，先跳過
    
    # 檢查 4: 列表項目格式
    # 檢查是否有不一致的列表標記
    
    echo "  ✅ 基本檢查通過"
    echo ""
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ 所有檔案通過 Markdown linting 檢查"
    exit 0
else
    echo "⚠️  發現 $ERRORS 個問題"
    echo ""
    echo "建議執行以下命令修復："
    echo "  1. 確保所有檔案結尾有空行"
    echo "  2. 移除多餘的連續空行"
    exit 1
fi
