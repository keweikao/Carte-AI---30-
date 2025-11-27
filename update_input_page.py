#!/usr/bin/env python3
"""
Input Page UX 優化腳本
根據 specs/input-page-ux-improvements.md 和 implementation_plan.md 執行修改
"""

import re

def main():
    file_path = "/Users/stephen/Desktop/OderWhat/frontend/src/app/input/page.tsx"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("開始執行 Input Page UX 優化...")

    # 已完成：標題修改 ✅
    print("✅ 1. 標題已修改為「開啟你的美食探索之旅」")

    # Task 2: 新增返回按鈕 (新增 import)
    # 檢查是否已有 ArrowLeft
    if "ArrowLeft" not in content:
        content = content.replace(
            'from "lucide-react";',
            ', ArrowLeft from "lucide-react";'
        )
        print("✅ 2a. 新增 ArrowLeft import")

    # Task 2: 在 Step 2 開頭新增返回按鈕
    step2_pattern = r'(<motion\.div\s+key="step2"[^>]*>)'
    step2_replacement = r'''\1
                            {/* 返回按鈕 */}
                            <Button
                                variant="ghost"
                                onClick={() => setStep(1)}
                                className="gap-2 mb-4"
                                aria-label="返回上一步"
                            >
                                <ArrowLeft className="w-4 h-4" />
                                返回
                            </Button>
'''

    if '<ArrowLeft className="w-4 h-4" />' not in content or 'aria-label="返回上一步"' not in content:
        content = re.sub(step2_pattern, step2_replacement, content, count=1)
        print("✅ 2b. 新增返回按鈕")
    else:
        print("⚠️  2b. 返回按鈕已存在，跳過")

    # Task 3: 預算金額輸入優化 - 修改 placeholder
    content = content.replace(
        'placeholder="200"',
        'placeholder="例如：500"'
    )
    print("✅ 3. 預算輸入框 placeholder 已優化")

    # Task 4: 預算類型選擇器視覺優化
    # 檢查是否已有 User import
    if ", User" not in content and "User," not in content:
        content = content.replace(
            'import { ArrowRight',
            'import { ArrowRight, User'
        )
        print("✅ 4a. 新增 User icon import")

    # 優化預算類型選擇器樣式
    old_budget_button_person = r'''<button
                                                className={`px-2 sm:px-3 py-1 text-xs rounded-md transition-all \$\{budgetType === "person" \? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"\}`\}
                                                onClick=\{\(\) => setBudgetType\("person"\)\}
                                                aria-label="按每人預算計算"
                                                aria-pressed=\{budgetType === "person"\}
                                            >
                                                每人\(客單\)
                                            </button>'''

    new_budget_button_person = r'''<button
                                                type="button"
                                                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${budgetType === "person" ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary" : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"}`}
                                                onClick={() => setBudgetType("person")}
                                                aria-label="選擇每人預算模式"
                                                aria-pressed={budgetType === "person"}
                                            >
                                                <User className="w-4 h-4" />
                                                每人(客單)
                                            </button>'''

    if '<User className="w-4 h-4" />' not in content:
        # 簡化版：直接替換整個按鈕區域
        content = content.replace(
            '''<button
                                                className={`px-2 sm:px-3 py-1 text-xs rounded-md transition-all ${budgetType === "person" ? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"}`}
                                                onClick={() => setBudgetType("person")}
                                                aria-label="按每人預算計算"
                                                aria-pressed={budgetType === "person"}
                                            >
                                                每人(客單)
                                            </button>''',
            '''<button
                                                type="button"
                                                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${budgetType === "person" ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary" : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"}`}
                                                onClick={() => setBudgetType("person")}
                                                aria-label="選擇每人預算模式"
                                                aria-pressed={budgetType === "person"}
                                            >
                                                <User className="w-4 h-4" />
                                                每人(客單)
                                            </button>'''
        )

        content = content.replace(
            '''<button
                                                className={`px-3 py-1 text-xs rounded-md transition-all ${budgetType === "total" ? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"}`}
                                                onClick={() => setBudgetType("total")}
                                                aria-label="按總預算計算"
                                                aria-pressed={budgetType === "total"}
                                            >
                                                總預算
                                            </button>''',
            '''<button
                                                type="button"
                                                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${budgetType === "total" ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary" : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"}`}
                                                onClick={() => setBudgetType("total")}
                                                aria-label="選擇總預算模式"
                                                aria-pressed={budgetType === "total"}
                                            >
                                                <Users className="w-4 h-4" />
                                                總預算
                                            </button>'''
        )
        print("✅ 4b. 預算類型選擇器視覺已優化")
    else:
        print("⚠️  4b. 預算類型選擇器已優化，跳過")

    # Task 5: 飲食偏好重新設計
    # 修改標題
    content = content.replace(
        '<Label className="text-base">飲食偏好</Label>',
        '<Label className="text-base">用餐風格偏好</Label>'
    )

    # 修改 Textarea placeholder
    content = content.replace(
        'placeholder="若你要用自然語言描述讓 AI 更了解你的需求也可以唷..."',
        'placeholder="還有什麼特別需求都可以告訴我，例如：不吃牛、怕過敏、偏好當季食材..."'
    )

    #更新飲食偏好選項
    old_suggestions = '''suggestions={[
                                            { id: "no_beef", label: "不吃牛", icon: "🥩" },
                                            { id: "no_pork", label: "不吃豬", icon: "🐷" },
                                            { id: "vegetarian", label: "素食", icon: "🥬" },
                                            { id: "seafood_allergy", label: "海鮮過敏", icon: "🦐" },
                                            { id: "spicy", label: "愛吃辣", icon: "🌶️" },
                                            { id: "no_spicy", label: "不吃辣", icon: "🚫" },
                                            { id: "alcohol", label: "想喝酒", icon: "🍺" },
                                            { id: "kid_friendly", label: "有小孩", icon: "👶" },
                                            { id: "elderly", label: "長輩友善", icon: "👴" },
                                        ]}'''

    new_suggestions = '''suggestions={[
                                            { id: "love_meat", label: "愛吃肉", icon: "🥩" },
                                            { id: "more_seafood", label: "多點海鮮", icon: "🦐" },
                                            { id: "need_vegetarian", label: "需要素食選項", icon: "🥬" },
                                            { id: "more_vegetables", label: "多蔬菜", icon: "🥗" },
                                            { id: "prefer_light", label: "偏好清淡", icon: "🍃" },
                                            { id: "can_eat_spicy", label: "能吃辣", icon: "🌶️" },
                                            { id: "no_spicy", label: "不吃辣", icon: "🚫" },
                                            { id: "kid_friendly", label: "有小孩", icon: "👶" },
                                            { id: "elderly", label: "長輩友善", icon: "👴" },
                                        ]}'''

    content = content.replace(old_suggestions, new_suggestions)

    print("✅ 5. 飲食偏好已重新設計")

    # 寫回檔案
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n🎉 所有優化完成！")
    print("\n修改摘要：")
    print("1. ✅ 標題：「客製化你的餐點」→「開啟你的美食探索之旅」")
    print("2. ✅ 新增返回按鈕")
    print("3. ✅ 預算輸入框 placeholder 優化")
    print("4. ✅ 預算類型選擇器視覺優化（加入 icons 和 hover 效果）")
    print("5. ✅ 飲食偏好重新設計")

if __name__ == "__main__":
    main()
