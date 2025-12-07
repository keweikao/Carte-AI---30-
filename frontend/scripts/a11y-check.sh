#!/bin/bash

# Accessibility Check Script
# This script provides a quick checklist for accessibility testing

echo "============================================"
echo "   無障礙性快速檢查清單"
echo "============================================"
echo ""

echo "📋 手動測試項目："
echo ""

echo "1. 鍵盤導航測試"
echo "   [ ] 按 Tab 鍵可以導航所有互動元素"
echo "   [ ] 焦點指示器清晰可見"
echo "   [ ] 可以用 Enter 鍵確認按鈕"
echo "   [ ] 可以用 Escape 鍵關閉對話框"
echo ""

echo "2. 螢幕閱讀器測試 (VoiceOver)"
echo "   [ ] 啟動 VoiceOver (⌘ + F5)"
echo "   [ ] 頁面標題正確朗讀"
echo "   [ ] 按鈕和連結有描述性文字"
echo "   [ ] 表單欄位有關聯的標籤"
echo "   [ ] 動態內容更新有通知"
echo ""

echo "3. 視覺測試"
echo "   [ ] 文字在 200% 縮放下仍可讀"
echo "   [ ] 顏色對比度足夠 (檢查淺色文字)"
echo "   [ ] 沒有僅依賴顏色的資訊"
echo ""

echo "4. 動畫測試"
echo "   [ ] 在系統設定中啟用「減少動態效果」"
echo "   [ ] 確認動畫已停用或大幅減少"
echo ""

echo "============================================"
echo "   自動化測試建議"
echo "============================================"
echo ""

echo "推薦使用以下工具："
echo "1. Lighthouse (Chrome DevTools)"
echo "   - 打開 DevTools (F12)"
echo "   - 切換到 Lighthouse 標籤"
echo "   - 勾選 'Accessibility'"
echo "   - 執行報告"
echo ""

echo "2. axe DevTools (瀏覽器擴充套件)"
echo "   - 安裝: https://www.deque.com/axe/devtools/"
echo "   - 在每個頁面上執行掃描"
echo ""

echo "3. WAVE (Web Accessibility Evaluation Tool)"
echo "   - 線上工具: https://wave.webaim.org/"
echo "   - 或安裝瀏覽器擴充套件"
echo ""

echo "============================================"
echo "   測試頁面清單"
echo "============================================"
echo ""
echo "請測試以下頁面："
echo "  • http://localhost:3000/ (首頁)"
echo "  • http://localhost:3000/input (輸入頁)"
echo "  • http://localhost:3000/recommendation (推薦頁)"
echo "  • http://localhost:3000/menu (菜單頁)"
echo ""

echo "============================================"
echo "詳細的測試指南請參閱 ACCESSIBILITY.md"
echo "============================================"
