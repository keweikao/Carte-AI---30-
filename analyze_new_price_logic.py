#!/usr/bin/env python3
"""
新的價格邏輯分析：動態總價 = 已選 + 未選
"""

print("=" * 80)
print("💰 新價格邏輯分析報告")
print("=" * 80)
print()

print("## 🎯 核心概念")
print()
print("總價 = 已選菜品總價 + 未選菜品總價")
print()
print("重點：")
print("  1. 總價會隨著「換菜」而改變（因為菜品價格不同）")
print("  2. 總價會隨著「確定」而改變（因為確定後的菜不會再變）")
print("  3. 直到所有類別都選完，總價才固定")
print()

print("=" * 80)
print("📊 實際案例演示")
print("=" * 80)
print()

# 定義初始菜單（按類別分組）
menu = {
    "冷菜": [
        {"name": "涼拌黃瓜", "price": 80, "status": "pending"},
    ],
    "熱菜": [
        {"name": "宮保雞丁", "price": 180, "status": "pending"},
        {"name": "魚香肉絲", "price": 160, "status": "pending"},
    ],
    "主食": [
        {"name": "蛋炒飯", "price": 120, "status": "pending"},
    ],
    "湯品": [
        {"name": "酸辣湯", "price": 100, "status": "pending"},
    ]
}

def calculate_total(menu):
    """計算當前總價"""
    total = 0
    for category, items in menu.items():
        for item in items:
            total += item["price"]
    return total

def get_status_summary(menu):
    """取得選擇狀態摘要"""
    selected = []
    pending = []
    for category, items in menu.items():
        for item in items:
            if item["status"] == "selected":
                selected.append(item["name"])
            else:
                pending.append(item["name"])
    return selected, pending

people = 2

print("### 初始狀態：系統推薦菜單")
print()
for category, items in menu.items():
    print(f"{category}:")
    for item in items:
        print(f"  - {item['name']}: NT$ {item['price']}")
print()

initial_total = calculate_total(menu)
print(f"總價: NT$ {initial_total}")
print(f"人均: NT$ {initial_total // people}")
print()

print("=" * 80)
print("📝 使用者操作流程")
print("=" * 80)
print()

# 情境 1
print("### 情境 1: 使用者在「冷菜」類別點選「我要點這道」")
print()
menu["冷菜"][0]["status"] = "selected"
print("動作: 確定 涼拌黃瓜")
print()

selected, pending = get_status_summary(menu)
total = calculate_total(menu)
print(f"顯示總價: NT$ {total}")
print(f"顯示人均: NT$ {total // people}")
print(f"組成: 已選({len(selected)}道) + 未選({len(pending)}道)")
print(f"  已選: {', '.join(selected)}")
print(f"  未選: {', '.join(pending)}")
print()
print("✅ 總價不變 (830)，因為只是「確定」不是「換菜」")
print()

# 情境 2
print("=" * 80)
print("### 情境 2: 使用者在「熱菜」類別對「宮保雞丁」點選「換一道」")
print()
print("動作: 換掉 宮保雞丁 → 糖醋魚 (NT$ 220)")
print()

# 移除宮保雞丁
menu["熱菜"] = [item for item in menu["熱菜"] if item["name"] != "宮保雞丁"]
# 加入糖醋魚
menu["熱菜"].append({"name": "糖醋魚", "price": 220, "status": "pending"})

selected, pending = get_status_summary(menu)
total = calculate_total(menu)
print(f"顯示總價: NT$ {total}")
print(f"顯示人均: NT$ {total // people}")
print(f"組成: 已選({len(selected)}道) + 未選({len(pending)}道)")
print(f"  已選: {', '.join(selected)}")
print(f"  未選: {', '.join(pending)}")
print()
print("⚠️  總價變為 870 (+40)，因為糖醋魚比宮保雞丁貴 NT$ 40")
print()

# 情境 3
print("=" * 80)
print("### 情境 3: 使用者確定「糖醋魚」")
print()
for item in menu["熱菜"]:
    if item["name"] == "糖醋魚":
        item["status"] = "selected"

selected, pending = get_status_summary(menu)
total = calculate_total(menu)
print(f"顯示總價: NT$ {total}")
print(f"顯示人均: NT$ {total // people}")
print(f"組成: 已選({len(selected)}道) + 未選({len(pending)}道)")
print(f"  已選: {', '.join(selected)}")
print(f"  未選: {', '.join(pending)}")
print()
print("✅ 總價不變 (870)，只是確定不是換菜")
print()

# 情境 4
print("=" * 80)
print("### 情境 4: 繼續確定剩餘菜品")
print()
for category, items in menu.items():
    for item in items:
        if item["status"] == "pending":
            item["status"] = "selected"

selected, pending = get_status_summary(menu)
total = calculate_total(menu)
print(f"最終總價: NT$ {total}")
print(f"最終人均: NT$ {total // people}")
print(f"已選菜品: {', '.join(selected)}")
print()
print("✅ 所有類別選完，總價固定為 NT$ 870")
print()

print("=" * 80)
print("🔑 關鍵實作邏輯")
print("=" * 80)
print()

print("### 1. 總價計算")
print("```typescript")
print("const calculateCurrentTotal = () => {")
print("    // 計算所有當前菜品的總價（無論是否已選）")
print("    return currentItems.reduce((sum, item) => sum + (item.price || 0), 0);")
print("};")
print("```")
print()

print("### 2. 狀態追蹤")
print("```typescript")
print("interface MenuItem {")
print("    name: string;")
print("    price: number;")
print("    category: string;")
print("    status: 'pending' | 'selected';  // 待選擇 或 已確定")
print("}")
print()
print("const [currentItems, setCurrentItems] = useState<MenuItem[]>([]);")
print("```")
print()

print("### 3. 按鈕互動")
print("```typescript")
print("// 點選「我要點這道」")
print("const handleConfirmItem = (itemName: string) => {")
print("    setCurrentItems(prev => prev.map(item => ")
print("        item.name === itemName")
print("            ? { ...item, status: 'selected' }")
print("            : item")
print("    ));")
print("    // 總價不變（因為菜品沒變）")
print("};")
print()
print("// 點選「換一道」")
print("const handleReplaceItem = async (itemName: string, category: string) => {")
print("    // 1. 呼叫 API 取得替代菜品")
print("    const replacement = await fetchReplacement(category);")
print("    ")
print("    // 2. 替換菜品")
print("    setCurrentItems(prev => prev.map(item =>")
print("        item.name === itemName")
print("            ? { ...replacement, status: 'pending' }")
print("            : item")
print("    ));")
print("    // 總價會變（因為新菜品價格可能不同）")
print("};")
print("```")
print()

print("=" * 80)
print("🎨 UI 設計：類別與數量顯示")
print("=" * 80)
print()

print("### 需求：顯示本次菜單的大類別和建議點的菜數")
print()
print("```")
print("┌────────────────────────────────────────┐")
print("│ 本次菜單組成                            │")
print("│                                        │")
print("│ 🥗 冷菜 × 1   🍖 熱菜 × 2              │")
print("│ 🍚 主食 × 1   🍲 湯品 × 1              │")
print("│                                        │")
print("│ 共 5 道 · 總價 NT$ 870 · 人均 $435    │")
print("└────────────────────────────────────────┘")
print("```")
print()

print("### 實作邏輯")
print("```typescript")
print("// 計算每個類別的數量")
print("const categoryStats = useMemo(() => {")
print("    const stats: Record<string, number> = {};")
print("    currentItems.forEach(item => {")
print("        stats[item.category] = (stats[item.category] || 0) + 1;")
print("    });")
print("    return stats;")
print("}, [currentItems]);")
print()
print("// 顯示")
print("<div className='category-chips'>")
print("    {Object.entries(categoryStats).map(([category, count]) => (")
print("        <Badge key={category}>")
print("            {getCategoryIcon(category)} {category} × {count}")
print("        </Badge>")
print("    ))}")
print("</div>")
print("```")
print()

print("=" * 80)
print("✅ 總結：新邏輯的優缺點")
print("=" * 80)
print()

print("### ✅ 優點")
print("1. 簡單直觀：總價就是「當前菜單的總價」")
print("2. 即時反映：換菜立即看到價格變化")
print("3. 符合心智模型：「我的菜單總共多少錢」")
print()

print("### ⚠️  需注意")
print("1. 換菜可能導致價格波動（需要警告使用者）")
print("2. 需要後端支援「根據類別換菜」的 API")
print("3. 需要清楚顯示類別資訊，讓使用者理解菜單結構")
print()

print("### 🔧 建議增強功能")
print("1. 換菜時顯示價格差異（+$40 / -$20）")
print("2. 預算警告（總價超出使用者預算時提示）")
print("3. 類別完成進度條（已選 2/5 類別）")
print()

print("=" * 80)
print("📐 資料結構設計")
print("=" * 80)
print()

print("### 後端 API 回應格式")
print("```json")
print("{")
print('  "recommendation_id": "abc123",')
print('  "items": [')
print("    {")
print('      "name": "涼拌黃瓜",')
print('      "price": 80,')
print('      "category": "冷菜",')
print('      "reason": "清爽開胃...",')
print('      "review_count": 234')
print("    },")
print("    ...")
print("  ],")
print('  "category_summary": {')
print('    "冷菜": 1,')
print('    "熱菜": 2,')
print('    "主食": 1,')
print('    "湯品": 1')
print("  },")
print('  "total_price": 830,')
print('  "per_person": 415')
print("}")
print("```")
print()

print("=" * 80)
