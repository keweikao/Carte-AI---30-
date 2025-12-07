#!/bin/bash

echo "🔍 驗證 FE-043 響應式修正"
echo "================================"
echo ""

# 檢查修正的檔案
echo "📝 檢查已修正的檔案..."
files=(
  "src/app/page.tsx"
  "src/components/brand-header.tsx"
  "src/app/input/page.tsx"
  "src/app/recommendation/page.tsx"
  "src/app/menu/page.tsx"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file (未找到)"
  fi
done

echo ""
echo "💾 檢查備份檔案..."
backups=(
  "src/app/input/page.tsx.backup"
  "src/app/recommendation/page.tsx.backup"
  "src/app/menu/page.tsx.backup"
)

for backup in "${backups[@]}"; do
  if [ -f "$backup" ]; then
    echo "✅ $backup"
  else
    echo "⚠️  $backup (未找到)"
  fi
done

echo ""
echo "📄 檢查文檔..."
docs=(
  "RESPONSIVE_TEST_REPORT.md"
  "RESPONSIVE_FIXES_SUMMARY.md"
  "responsive-fixes.md"
  "FE-043-COMPLETION-SUMMARY.md"
)

for doc in "${docs[@]}"; do
  if [ -f "$doc" ]; then
    size=$(ls -lh "$doc" | awk '{print $5}')
    echo "✅ $doc ($size)"
  else
    echo "❌ $doc (未找到)"
  fi
done

echo ""
echo "🔬 驗證關鍵修正..."

# 檢查首頁修正
if grep -q "gap-8 py-12 sm:gap-12 sm:py-16" src/app/page.tsx; then
  echo "✅ 首頁：響應式間距已應用"
else
  echo "⚠️  首頁：響應式間距未找到"
fi

# 檢查品牌標題修正
if grep -q "text-2xl sm:text-3xl" src/components/brand-header.tsx; then
  echo "✅ 品牌標題：響應式文字已應用"
else
  echo "⚠️  品牌標題：響應式文字未找到"
fi

# 檢查輸入頁修正
if grep -q "flex flex-col sm:flex-row" src/app/input/page.tsx; then
  echo "✅ 輸入頁：響應式佈局已應用"
else
  echo "⚠️  輸入頁：響應式佈局未找到"
fi

# 檢查推薦頁修正
if grep -q "px-2 sm:px-4" src/app/recommendation/page.tsx; then
  echo "✅ 推薦頁：響應式間距已應用"
else
  echo "⚠️  推薦頁：響應式間距未找到"
fi

# 檢查菜單頁修正
if grep -q "text-3xl sm:text-4xl" src/app/menu/page.tsx; then
  echo "✅ 菜單頁：響應式文字已應用"
else
  echo "⚠️  菜單頁：響應式文字未找到"
fi

echo ""
echo "📊 統計資訊..."
echo "修正的檔案：$(find src -name "*.tsx" -newer src/app/page.tsx.backup 2>/dev/null | wc -l | tr -d ' ') 個"
echo "備份檔案：$(find . -name "*.backup" | wc -l | tr -d ' ') 個"
echo "文檔檔案：$(ls -1 *.md 2>/dev/null | wc -l | tr -d ' ') 個"

echo ""
echo "✨ 驗證完成！"
