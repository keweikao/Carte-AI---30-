#!/bin/bash

# 測試 Staging 環境的 Vision API fallback
# 透過觀察回應內容來驗證功能

STAGING_URL="https://oderwhat-staging-u33peegeaa-de.a.run.app"

echo "==========================================="
echo "Staging Vision API Fallback 測試"
echo "==========================================="
echo ""

# 測試案例 1: 欣葉小聚今品
echo "測試 1: 欣葉小聚今品"
echo "-------------------------------------------"
PLACE_ID="ChIJT_tO6SupQjQRx7bH6OqW0lQ"
NAME="%E6%AC%A3%E8%91%89%E5%B0%8F%E8%81%9A%E4%BB%8A%E5%93%81"  # URL encoded

echo "發送請求..."
RESPONSE=$(curl -s -X GET "${STAGING_URL}/api/v1/restaurant/${PLACE_ID}?name=${NAME}")
echo "原始回應:"
echo "$RESPONSE"
echo "$RESPONSE" | python3 -m json.tool > /tmp/test_result_1.json

echo ""
echo "📊 回應摘要："
echo "-------------------------------------------"

# 提取關鍵資訊
MENU_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('menu_items', [])))")
FIRST_ITEM=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); items=data.get('menu_items', []); print(items[0]['name'] if items else 'None')")
TRUST_LEVEL=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('trust_level', 'unknown'))")
ADDRESS=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('address', 'N/A'))")

echo "菜單項目數量: $MENU_COUNT"
echo "第一道菜: $FIRST_ITEM"
echo "Trust Level: $TRUST_LEVEL"
echo "地址: $ADDRESS"
echo ""

if [ "$FIRST_ITEM" = "Fallback Dish" ]; then
    echo "⚠️  仍然是 Fallback Dish - Vision API 可能未成功"
else
    echo "✅ 成功提取真實菜單！"
    echo ""
    echo "菜單預覽（前 5 道）："
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('menu_items', [])
for i, item in enumerate(items[:5], 1):
    name = item.get('name', 'N/A')
    price = item.get('price', 'N/A')
    category = item.get('category', 'N/A')
    print(f'{i}. {name:25s} | NT\$ {price:4s} | {category}')
"
fi

echo ""
echo "完整回應已儲存至: /tmp/test_result_1.json"
echo ""

# 測試案例 2: 新餐廳（強制 cold start）
echo "==========================================="
echo "測試 2: 八雲韓國烤肉 (新餐廳)"
echo "-------------------------------------------"
PLACE_ID2="dummy-place-id-$(date +%s)"
NAME2="%E5%85%AB%E9%9B%B2%E9%9F%93%E5%9C%8B%E7%83%A4%E8%82%89-%E6%96%B0%E9%AE%AE%E6%B8%AC%E8%A9%A6_$(date +%s)" # URL encoded + unique timestamp

echo "發送請求..."
RESPONSE2=$(curl -s -X GET "${STAGING_URL}/api/v1/restaurant/${PLACE_ID2}?name=${NAME2}")
echo "$RESPONSE2" | python3 -m json.tool > /tmp/test_result_2.json

echo ""
echo "📊 回應摘要："
echo "-------------------------------------------"

MENU_COUNT2=$(echo "$RESPONSE2" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('menu_items', [])))")
FIRST_ITEM2=$(echo "$RESPONSE2" | python3 -c "import sys, json; data=json.load(sys.stdin); items=data.get('menu_items', []); print(items[0]['name'] if items else 'None')")
TRUST_LEVEL2=$(echo "$RESPONSE2" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('trust_level', 'unknown'))")
ADDRESS2=$(echo "$RESPONSE2" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('address', 'N/A'))")

echo "菜單項目數量: $MENU_COUNT2"
echo "第一道菜: $FIRST_ITEM2"
echo "Trust Level: $TRUST_LEVEL2"
echo "地址: $ADDRESS2"
echo ""

if [ "$FIRST_ITEM2" = "Fallback Dish" ]; then
    echo "⚠️  仍然是 Fallback Dish"
else
    echo "✅ 成功提取真實菜單！"
fi

echo ""
echo "完整回應已儲存至: /tmp/test_result_2.json"

echo ""
echo "==========================================="
echo "測試完成"
echo "==========================================="
echo "檢查完整結果："
echo "  cat /tmp/test_result_1.json"
echo "  cat /tmp/test_result_2.json"
