#!/usr/bin/env python3
"""
展示 Vision API 預期的輸出格式
模擬從餐廳圖片中提取的菜單資料
"""

import json

# 模擬 Vision API 從鼎泰豐圖片提取的菜單
demo_menu_dingtaifung = [
    {
        "name": "小籠包(10顆)",
        "price": 220,
        "category": "點心",
        "description": "招牌必點",
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "蝦肉燒賣(10顆)",
        "price": 240,
        "category": "點心",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "紅油抄手",
        "price": 190,
        "category": "麵點",
        "description": "微辣",
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "蝦仁炒飯",
        "price": 250,
        "category": "飯類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "排骨蛋炒飯",
        "price": 280,
        "category": "飯類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "蝦肉蒸餃(10顆)",
        "price": 240,
        "category": "點心",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "菜肉蒸餃(10顆)",
        "price": 220,
        "category": "點心",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "酸辣湯",
        "price": 110,
        "category": "湯品",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "元盅雞湯",
        "price": 150,
        "category": "湯品",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "絲瓜蝦仁小籠包(10顆)",
        "price": 260,
        "category": "點心",
        "description": "季節限定",
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "蟹粉小籠包(10顆)",
        "price": 320,
        "category": "點心",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "清炒空心菜",
        "price": 180,
        "category": "青菜",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    }
]

# 模擬從欣葉小聚今品圖片提取的菜單
demo_menu_xinye = [
    {
        "name": "松阪豬",
        "price": 380,
        "category": "肉類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "炒豬肝",
        "price": 280,
        "category": "熱炒",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "小卷米粉",
        "price": 350,
        "category": "米粉麵類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "蒜香菲力牛",
        "price": 450,
        "category": "肉類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "菜脯蛋",
        "price": 180,
        "category": "蛋類",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "清蒸魚",
        "price": None,  # 時價
        "category": "海鮮",
        "description": "時價",
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "炒高麗菜",
        "price": 150,
        "category": "青菜",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    },
    {
        "name": "布丁",
        "price": 80,
        "category": "甜點",
        "description": None,
        "source_type": "dine_in",
        "is_popular": False,
        "is_risky": False,
        "ai_insight": None
    }
]

def display_menu(menu_data, restaurant_name):
    """Display menu in a nice format"""
    print(f"\n{'='*70}")
    print(f"🍽️  {restaurant_name} - 模擬 Vision API 提取結果")
    print(f"{'='*70}\n")

    # Group by category
    categories = {}
    for item in menu_data:
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    # Display by category
    for category, items in categories.items():
        print(f"\n📋 {category}")
        print("-" * 70)
        for item in items:
            price_str = f"NT$ {item['price']}" if isinstance(item['price'], int) else str(item['price'])
            desc = f" ({item['description']})" if item['description'] else ""
            print(f"  • {item['name']:25s} {price_str:10s}{desc}")

    print(f"\n{'='*70}")
    print(f"總計: {len(menu_data)} 道菜")
    print(f"Trust Level: medium (從圖片提取)")
    print(f"{'='*70}\n")

def show_comparison():
    """Show before/after comparison"""
    print("\n" + "🔄 " * 35)
    print("Vision API Fallback - Before vs After 比較")
    print("🔄 " * 35 + "\n")

    print("❌ BEFORE (舊版本):")
    print("-" * 70)
    before = {
        "menu_items": [
            {
                "name": "Fallback Dish",
                "price": 120,
                "category": "Special",
                "source_type": "estimated"
            }
        ],
        "trust_level": "medium",
        "address": "Address placeholder"
    }
    print(json.dumps(before, indent=2, ensure_ascii=False))

    print("\n✅ AFTER (新版本 - 鼎泰豐範例):")
    print("-" * 70)
    after = {
        "menu_items": demo_menu_dingtaifung[:3],  # Show first 3
        "trust_level": "medium",
        "address": "台北市信義區信義路二段194號"
    }
    print(json.dumps(after, indent=2, ensure_ascii=False))
    print(f"\n... 還有 {len(demo_menu_dingtaifung) - 3} 道菜")

    print("\n" + "=" * 70)
    print("改善:")
    print("  ✅ 菜單項目: 1 → 12+ 道真實菜品")
    print("  ✅ 價格資訊: 固定120 → 真實價格")
    print("  ✅ 分類: Special → 點心/麵點/飯類/湯品等")
    print("  ✅ 地址: placeholder → 真實地址")
    print("=" * 70 + "\n")

def main():
    print("\n" + "🎨 " * 35)
    print("Vision API 菜單提取 - 預期輸出展示")
    print("🎨 " * 35)

    # Show comparison first
    show_comparison()

    # Display demo menus
    display_menu(demo_menu_dingtaifung, "鼎泰豐 (Din Tai Fung)")

    print("\n" + "─" * 70 + "\n")

    display_menu(demo_menu_xinye, "欣葉小聚今品")

    # Show JSON structure
    print("\n" + "=" * 70)
    print("📄 完整 JSON 結構範例")
    print("=" * 70 + "\n")

    full_response = {
        "place_id": "ChIJ-x-t9W_eQjQRhFjU2g08sHk",
        "name": "鼎泰豐",
        "address": "台北市信義區信義路二段194號",
        "trust_level": "medium",
        "menu_source_url": None,
        "menu_items": demo_menu_dingtaifung[:2],  # Show 2 items
        "review_summary": "餐廳評價良好，小籠包和蝦仁炒飯特別受歡迎..."
    }

    print(json.dumps(full_response, indent=2, ensure_ascii=False))
    print(f"\n... menu_items 還有 {len(demo_menu_dingtaifung) - 2} 道菜")

    # Show key features
    print("\n" + "=" * 70)
    print("🎯 Vision API 提取特點")
    print("=" * 70)
    print("""
1. ✅ 只提取同時有菜名和價格的項目
2. ✅ 自動分類（點心、麵點、飯類、湯品等）
3. ✅ 保留描述資訊（如「季節限定」、「微辣」）
4. ✅ 過濾非菜單圖片（外觀、食物照片）
5. ✅ source_type 設為 "dine_in"
6. ✅ trust_level 設為 "medium"

處理流程:
  📷 Google Maps 圖片 (Apify)
   ↓
  🤖 Gemini Vision API (OCR)
   ↓
  📋 結構化菜單資料 (JSON)
   ↓
  💾 儲存到 Firestore
    """)

    print("\n" + "=" * 70)
    print("📊 預期效果")
    print("=" * 70)
    print("""
Before:
  - 菜單抓取成功率: 0%
  - 只有 "Fallback Dish"

After:
  - 菜單抓取成功率: 80%+
  - 10-20 道真實菜品
  - 完整價格和分類資訊
  - 真實餐廳地址
    """)

    print("=" * 70 + "\n")
    print("💡 提示: 這些是模擬資料，實際結果取決於：")
    print("   - Google Maps 圖片品質")
    print("   - 菜單在圖片中的清晰度")
    print("   - Gemini Vision 的辨識能力")
    print("\n")

if __name__ == "__main__":
    main()
