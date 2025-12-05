#!/bin/bash

# Carte AI 設計遷移快速驗證腳本

echo "🚀 開始 Carte AI 設計遷移驗證..."
echo ""

# 切換到專案目錄
cd "$(dirname "$0")"

# 執行完整性測試
echo "📋 執行完整性測試..."
python3 test_migration_completeness.py

# 檢查測試結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有測試通過!"
    echo ""
    echo "📄 查看詳細報告:"
    echo "   - JSON: test_migration_report.json"
    echo "   - Markdown: docs/MIGRATION_TEST_REPORT.md"
    echo ""
    exit 0
else
    echo ""
    echo "❌ 測試失敗,請檢查上方錯誤訊息"
    echo ""
    exit 1
fi
