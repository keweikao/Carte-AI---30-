#!/usr/bin/env python3
"""
驗證 Input 頁面 UX 優化是否正確實作
"""

import re

def check_file_changes():
    """檢查檔案修改是否正確"""
    file_path = "/Users/stephen/Desktop/OderWhat/frontend/src/app/input/page.tsx"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 60)
    print("Input 頁面 UX 優化驗證報告")
    print("=" * 60)
    print()

    checks = []

    # 1. 檢查標題
    print("1. 標題檢查")
    if "開啟你的美食探索之旅" in content:
        print("   ✅ 標題已更新為「開啟你的美食探索之旅」")
        checks.append(True)
    else:
        print("   ❌ 標題未更新")
        checks.append(False)
    print()

    # 2. 檢查返回按鈕
    print("2. 返回按鈕檢查")
    if 'aria-label="返回上一步"' in content and '<ArrowLeft className="w-4 h-4" />' in content:
        print("   ✅ 返回按鈕已新增")
        if 'onClick={() => setStep(1)}' in content:
            print("   ✅ 返回邏輯正確（返回步驟一）")
            checks.append(True)
        else:
            print("   ⚠️  返回邏輯可能不正確")
            checks.append(False)
    else:
        print("   ❌ 返回按鈕未新增")
        checks.append(False)
    print()

    # 3. 檢查 imports
    print("3. Icon Imports 檢查")
    imports_ok = True
    if "ArrowLeft" in content.split('\n')[13]:  # import 語句所在行
        print("   ✅ ArrowLeft icon 已匯入")
    else:
        print("   ❌ ArrowLeft icon 未匯入")
        imports_ok = False

    if "User" in content.split('\n')[13]:
        print("   ✅ User icon 已匯入")
    else:
        print("   ❌ User icon 未匯入")
        imports_ok = False

    checks.append(imports_ok)
    print()

    # 4. 檢查預算類型選擇器
    print("4. 預算類型選擇器檢查")
    if '<User className="w-4 h-4" />' in content:
        print("   ✅ 每人預算按鈕有 User icon")
        checks.append(True)
    else:
        print("   ❌ 每人預算按鈕缺少 User icon")
        checks.append(False)

    if '<Users className="w-4 h-4" />' in content:
        print("   ✅ 總預算按鈕有 Users icon")
    else:
        print("   ❌ 總預算按鈕缺少 Users icon")

    # 檢查 hover 效果
    if "hover:bg-white/50" in content:
        print("   ✅ 未選中狀態有 hover 效果")
    else:
        print("   ⚠️  未選中狀態可能缺少 hover 效果")

    # 檢查選中狀態樣式
    if "border-2 border-primary" in content:
        print("   ✅ 選中狀態有明顯邊框")
    else:
        print("   ⚠️  選中狀態可能缺少邊框")
    print()

    # 5. 檢查預算輸入框
    print("5. 預算輸入框檢查")
    if 'placeholder="例如：500"' in content:
        print("   ✅ Placeholder 已更新為「例如：500」")
        checks.append(True)
    else:
        print("   ❌ Placeholder 未更新")
        checks.append(False)
    print()

    # 6. 檢查飲食偏好
    print("6. 飲食偏好檢查")
    dietary_ok = True

    # 檢查標題
    if '<Label className="text-base">用餐風格偏好</Label>' in content:
        print("   ✅ 標題已更新為「用餐風格偏好」")
    else:
        print("   ❌ 標題未更新")
        dietary_ok = False

    # 檢查新選項
    new_options = [
        "愛吃肉",
        "多點海鮮",
        "需要素食選項",
        "多蔬菜",
        "偏好清淡",
        "能吃辣"
    ]

    missing_options = []
    for option in new_options:
        if option not in content:
            missing_options.append(option)

    if not missing_options:
        print(f"   ✅ 所有新選項已新增（{len(new_options)} 個）")
    else:
        print(f"   ❌ 缺少選項：{', '.join(missing_options)}")
        dietary_ok = False

    # 檢查 Textarea placeholder
    if "還有什麼特別需求都可以告訴我" in content:
        print("   ✅ 自由輸入框 placeholder 已優化")
    else:
        print("   ❌ 自由輸入框 placeholder 未更新")
        dietary_ok = False

    checks.append(dietary_ok)
    print()

    # 7. 檢查 budget_type 參數傳遞
    print("7. URL 參數傳遞檢查")
    budget_type_count = content.count('budget_type: budgetType')
    if budget_type_count >= 2:
        print(f"   ✅ budget_type 參數在 {budget_type_count} 處正確傳遞")
        checks.append(True)
    else:
        print(f"   ⚠️  budget_type 參數只在 {budget_type_count} 處傳遞（應該至少 2 處）")
        checks.append(False)
    print()

    # 總結
    print("=" * 60)
    print("測試總結")
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100

    print(f"通過：{passed}/{total} ({percentage:.1f}%)")
    print()

    if passed == total:
        print("🎉 所有檢查通過！UX 優化已正確實作")
        return True
    else:
        print("⚠️  部分檢查未通過，請檢查上述項目")
        return False

def check_responsive_breakpoints():
    """檢查響應式設計的斷點"""
    file_path = "/Users/stephen/Desktop/OderWhat/frontend/src/app/input/page.tsx"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\n" + "=" * 60)
    print("響應式設計檢查")
    print("=" * 60)
    print()

    # 檢查 Tailwind 響應式 class
    responsive_classes = ["sm:", "md:", "lg:", "xl:"]
    found_responsive = []

    for cls in responsive_classes:
        count = content.count(cls)
        if count > 0:
            found_responsive.append(f"{cls} ({count} 處)")

    if found_responsive:
        print(f"✅ 發現響應式 class：{', '.join(found_responsive)}")
    else:
        print("⚠️  未發現響應式 class")

    # 檢查特定的響應式設計
    if "sm:px-" in content or "sm:gap-" in content:
        print("✅ 有針對小螢幕的 padding/gap 調整")

    if "sm:flex-row" in content:
        print("✅ 有針對小螢幕的 flex 方向調整")

    print()

def generate_test_checklist():
    """生成人工測試檢查清單"""
    print("=" * 60)
    print("人工測試檢查清單")
    print("=" * 60)
    print()
    print("請在瀏覽器中開啟 http://localhost:3000/input 並檢查：")
    print()
    print("□ 1. 標題顯示「開啟你的美食探索之旅」")
    print("□ 2. 步驟二有返回按鈕，點擊可返回步驟一")
    print("□ 3. 預算類型選擇器：")
    print("   □ 每人(客單) 有 👤 icon")
    print("   □ 總預算 有 👥 icon")
    print("   □ 未選中時 hover 有半透明白底")
    print("   □ 選中時有白底 + 陰影 + 邊框")
    print("□ 4. 預算輸入框 placeholder 顯示「例如：500」")
    print("□ 5. 飲食偏好標題顯示「用餐風格偏好」")
    print("□ 6. 飲食偏好選項包含：愛吃肉、多點海鮮、需要素食選項等")
    print("□ 7. 自由輸入框提示「還有什麼特別需求都可以告訴我...」")
    print("□ 8. 手機版（縮小視窗 <640px）所有元素正常顯示")
    print()

if __name__ == "__main__":
    # 執行檔案檢查
    all_pass = check_file_changes()

    # 檢查響應式設計
    check_responsive_breakpoints()

    # 生成人工測試清單
    generate_test_checklist()

    print("=" * 60)
    print("開發伺服器資訊")
    print("=" * 60)
    print("URL: http://localhost:3000/input")
    print("請使用瀏覽器開啟上述 URL 進行視覺測試")
    print("=" * 60)
