#!/usr/bin/env python3
"""
動態類別系統設計：根據餐廳類型自動調整
"""

print("=" * 80)
print("🍽️  動態類別系統設計")
print("=" * 80)
print()

# 定義不同餐廳類型的類別對應
category_mapping = {
    "中式餐館": {
        "categories": ["冷菜", "熱菜", "主食", "湯品", "點心"],
        "icons": {
            "冷菜": "🥗",
            "熱菜": "🍖",
            "主食": "🍚",
            "湯品": "🍲",
            "點心": "🥟"
        }
    },
    "日本料理": {
        "categories": ["刺身", "壽司", "燒烤", "麵類", "湯物"],
        "icons": {
            "刺身": "🍣",
            "壽司": "🍱",
            "燒烤": "🔥",
            "麵類": "🍜",
            "湯物": "🥘"
        }
    },
    "美式餐廳": {
        "categories": ["前菜", "主餐", "配菜", "甜點", "飲料"],
        "icons": {
            "前菜": "🥖",
            "主餐": "🥩",
            "配菜": "🥔",
            "甜點": "🍰",
            "飲料": "🥤"
        }
    },
    "義式料理": {
        "categories": ["前菜", "義大利麵", "披薩", "主菜", "甜點"],
        "icons": {
            "前菜": "🥗",
            "義大利麵": "🍝",
            "披薩": "🍕",
            "主菜": "🍖",
            "甜點": "🍮"
        }
    },
    "泰式料理": {
        "categories": ["開胃菜", "咖哩", "炒飯麵", "湯類", "甜品"],
        "icons": {
            "開胃菜": "🥟",
            "咖哩": "🍛",
            "炒飯麵": "🍜",
            "湯類": "🥘",
            "甜品": "🍧"
        }
    }
}

print("## 📋 支援的餐廳類型與類別")
print()

for cuisine, data in category_mapping.items():
    print(f"### {cuisine}")
    print(f"類別：{', '.join(data['categories'])}")
    icons_display = ' '.join([f"{data['icons'][cat]} {cat}" for cat in data['categories']])
    print(f"圖示：{icons_display}")
    print()

print("=" * 80)
print("🔧 實作邏輯")
print("=" * 80)
print()

print("### 1. 後端 API：根據餐廳自動判斷類型")
print()
print("```python")
print("def detect_cuisine_type(restaurant_name: str) -> str:")
print("    '''")
print("    根據餐廳名稱或菜單內容判斷餐廳類型")
print("    '''")
print("    keywords_map = {")
print("        '中式餐館': ['川菜', '粵菜', '湘菜', '魯菜', '炒', '燉'],")
print("        '日本料理': ['壽司', '刺身', '拉麵', '丼飯', '居酒屋'],")
print("        '美式餐廳': ['漢堡', '牛排', '炸雞', 'BBQ'],")
print("        '義式料理': ['義大利', 'pasta', '披薩', 'pizza'],")
print("        '泰式料理': ['泰式', '酸辣', '椰奶', '咖哩']")
print("    }")
print("    ")
print("    for cuisine, keywords in keywords_map.items():")
print("        if any(kw in restaurant_name for kw in keywords):")
print("            return cuisine")
print("    ")
print("    return '中式餐館'  # 預設")
print("```")
print()

print("### 2. API 回應格式")
print()
print("```json")
print("{")
print('  "recommendation_id": "abc123",')
print('  "restaurant_info": {')
print('    "name": "鼎泰豐",')
print('    "cuisine_type": "中式餐館"')
print("  },")
print('  "items": [')
print("    {")
print('      "name": "小籠包",')
print('      "price": 200,')
print('      "category": "點心",  // 動態類別')
print('      "reason": "鮮甜多汁...",')
print('      "review_count": 342')
print("    },")
print("    {")
print('      "name": "紅油抄手",')
print('      "price": 180,')
print('      "category": "冷菜",')
print('      "reason": "麻辣香濃...",')
print('      "review_count": 156')
print("    }")
print("  ],")
print('  "category_summary": {')
print('    "冷菜": 1,')
print('    "點心": 1,')
print('    "熱菜": 2,')
print('    "主食": 1')
print("  }")
print("}")
print("```")
print()

print("=" * 80)
print("💻 前端實作")
print("=" * 80)
print()

print("### 1. 類別圖示映射（TypeScript）")
print()
print("```typescript")
print("// src/lib/category-config.ts")
print()
print("type CuisineType = '中式餐館' | '日本料理' | '美式餐廳' | '義式料理' | '泰式料理';")
print()
print("interface CategoryConfig {")
print("    categories: string[];")
print("    icons: Record<string, string>;")
print("}")
print()
print("export const CATEGORY_CONFIGS: Record<CuisineType, CategoryConfig> = {")
print("    '中式餐館': {")
print("        categories: ['冷菜', '熱菜', '主食', '湯品', '點心'],")
print("        icons: {")
print("            '冷菜': '🥗',")
print("            '熱菜': '🍖',")
print("            '主食': '🍚',")
print("            '湯品': '🍲',")
print("            '點心': '🥟'")
print("        }")
print("    },")
print("    '日本料理': {")
print("        categories: ['刺身', '壽司', '燒烤', '麵類', '湯物'],")
print("        icons: {")
print("            '刺身': '🍣',")
print("            '壽司': '🍱',")
print("            '燒烤': '🔥',")
print("            '麵類': '🍜',")
print("            '湯物': '🥘'")
print("        }")
print("    },")
print("    // ... 其他類型")
print("};")
print()
print("export function getCategoryIcon(category: string, cuisineType: CuisineType): string {")
print("    const config = CATEGORY_CONFIGS[cuisineType];")
print("    return config?.icons[category] || '🍽️';")
print("}")
print("```")
print()

print("### 2. 組件實作")
print()
print("```typescript")
print("// src/app/recommendation/page.tsx")
print()
print("interface RecommendationData {")
print("    recommendation_id: string;")
print("    restaurant_info: {")
print("        name: string;")
print("        cuisine_type: CuisineType;")
print("    };")
print("    items: MenuItem[];")
print("    category_summary: Record<string, number>;")
print("}")
print()
print("export default function RecommendationPage() {")
print("    const [data, setData] = useState<RecommendationData | null>(null);")
print("    ")
print("    // 取得當前餐廳類型")
print("    const cuisineType = data?.restaurant_info.cuisine_type || '中式餐館';")
print("    ")
print("    // 計算類別統計")
print("    const categoryStats = useMemo(() => {")
print("        if (!data) return {};")
print("        return data.category_summary;")
print("    }, [data]);")
print("    ")
print("    return (")
print("        <div>")
print("            {/* 類別摘要卡片 */}")
print("            <div className='category-summary'>")
print("                <h3>本次菜單組成</h3>")
print("                <div className='category-chips'>")
print("                    {Object.entries(categoryStats).map(([category, count]) => (")
print("                        <Badge key={category}>")
print("                            {getCategoryIcon(category, cuisineType)} {category} × {count}")
print("                        </Badge>")
print("                    ))}")
print("                </div>")
print("            </div>")
print("        </div>")
print("    );")
print("}")
print("```")
print()

print("=" * 80)
print("🎨 UI 設計範例")
print("=" * 80)
print()

print("### 範例 1：中式餐館（鼎泰豐）")
print()
print("```")
print("┌────────────────────────────────────────┐")
print("│ 本次菜單組成                            │")
print("├────────────────────────────────────────┤")
print("│ 🥗 冷菜 × 1   🍖 熱菜 × 2              │")
print("│ 🍚 主食 × 1   🥟 點心 × 2              │")
print("├────────────────────────────────────────┤")
print("│ 共 6 道 · 總價 NT$ 1,200 · 人均 $400  │")
print("└────────────────────────────────────────┘")
print("```")
print()

print("### 範例 2：日本料理（壽司郎）")
print()
print("```")
print("┌────────────────────────────────────────┐")
print("│ 本次菜單組成                            │")
print("├────────────────────────────────────────┤")
print("│ 🍣 刺身 × 2   🍱 壽司 × 3              │")
print("│ 🍜 麵類 × 1   🥘 湯物 × 1              │")
print("├────────────────────────────────────────┤")
print("│ 共 7 道 · 總價 NT$ 1,500 · 人均 $500  │")
print("└────────────────────────────────────────┘")
print("```")
print()

print("### 範例 3：美式餐廳（TGI Fridays）")
print()
print("```")
print("┌────────────────────────────────────────┐")
print("│ 本次菜單組成                            │")
print("├────────────────────────────────────────┤")
print("│ 🥖 前菜 × 1   🥩 主餐 × 2              │")
print("│ 🥔 配菜 × 2   🥤 飲料 × 2              │")
print("├────────────────────────────────────────┤")
print("│ 共 7 道 · 總價 NT$ 1,800 · 人均 $600  │")
print("└────────────────────────────────────────┘")
print("```")
print()

print("=" * 80)
print("🔄 換菜 API 設計")
print("=" * 80)
print()

print("### API 端點")
print()
print("```")
print("POST /api/recommendations/{recommendation_id}/replace")
print()
print("Request:")
print("{")
print('  "item_name": "宮保雞丁",')
print('  "category": "熱菜"')
print("}")
print()
print("Response:")
print("{")
print('  "replacement": {')
print('    "name": "糖醋魚",')
print('    "price": 220,')
print('    "category": "熱菜",')
print('    "reason": "酸甜可口...",')
print('    "review_count": 189')
print("  }")
print("}")
print("```")
print()

print("### 後端實作邏輯")
print()
print("```python")
print("def get_replacement_dish(category: str, excluded_items: list) -> dict:")
print("    '''")
print("    根據類別取得替代菜品")
print("    excluded_items: 已經被排除的菜品名稱列表")
print("    '''")
print("    # 1. 從該類別的候選菜品中過濾")
print("    candidates = get_dishes_by_category(category)")
print("    candidates = [d for d in candidates if d['name'] not in excluded_items]")
print("    ")
print("    # 2. 根據評分排序")
print("    candidates.sort(key=lambda x: x['rating'], reverse=True)")
print("    ")
print("    # 3. 返回最佳候選")
print("    return candidates[0] if candidates else None")
print("```")
print()

print("=" * 80)
print("✅ 動態類別系統總結")
print("=" * 80)
print()

print("### 核心特性")
print("1. ✅ 自動偵測餐廳類型（中式/日式/美式/義式/泰式）")
print("2. ✅ 動態載入對應的類別與圖示")
print("3. ✅ 保持 API 回應格式統一")
print("4. ✅ 前端組件可擴充新類型")
print()

print("### 擴充性")
print("- 新增餐廳類型：只需在 CATEGORY_CONFIGS 新增定義")
print("- 新增類別圖示：修改 icons 映射")
print("- 後端判斷邏輯：更新 detect_cuisine_type() 函數")
print()

print("### 優先級")
print("1. 🔴 優先支援：中式、日式、美式（最常見）")
print("2. 🟡 次要支援：義式、泰式、韓式")
print("3. 🟢 未來擴充：其他小眾菜系")
print()

print("=" * 80)
