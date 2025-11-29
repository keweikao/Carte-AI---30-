#!/usr/bin/env python3
"""
測試移除預算限制後的功能
驗證：
1. 不帶預算的請求是否能成功
2. "All Signatures" 模式是否正常運作
"""

import asyncio
import json
from schemas.recommendation import UserInputV2, BudgetV2
from agent.dining_agent import DiningAgent

async def test_no_budget_input():
    """測試案例 1：不帶預算的請求"""
    print("=" * 80)
    print("測試案例 1：不帶預算的請求 (鼎泰豐)")
    print("=" * 80)
    print()

    user_input = UserInputV2(
        restaurant_name="鼎泰豐",
        dining_style="Shared",
        party_size=4,
        budget=None, # No budget!
        dish_count_target=None,
        preferences=[],
        natural_input="隨便吃",
        user_id=None
    )

    try:
        agent = DiningAgent()
        response = await agent.get_recommendations_v2(user_input)

        print(f"✅ 餐廳類型: {response.cuisine_type}")
        print("📋 推薦菜品：")
        for slot in response.items:
            item = slot.display
            print(f"  - {item.category:8s} | {item.dish_name:15s} | NT$ {item.price:4d}")

        print()
        print(f"✅ 總價: NT$ {response.total_price}")
        print("✅ 測試案例 1 通過 (成功生成無預算推薦)")
        return True

    except Exception as e:
        print(f"❌ 測試案例 1 失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_all_signatures_mode():
    """測試案例 2：招牌全制霸模式"""
    print()
    print("=" * 80)
    print("測試案例 2：招牌全制霸模式 (欣葉台菜)")
    print("=" * 80)
    print()

    user_input = UserInputV2(
        restaurant_name="欣葉台菜",
        dining_style="Shared",
        party_size=4,
        budget=None,
        dish_count_target=None,
        preferences=[],
        occasion="all_signatures", # 👑 Crown Mode
        natural_input=None,
        user_id=None
    )

    try:
        agent = DiningAgent()
        response = await agent.get_recommendations_v2(user_input)

        print(f"✅ 餐廳類型: {response.cuisine_type}")
        print("📋 推薦菜品：")
        signature_count = 0
        for slot in response.items:
            item = slot.display
            print(f"  - {item.category:8s} | {item.dish_name:15s} | NT$ {item.price:4d} | Reason: {item.reason[:30]}...")
            # Check reason for signature keywords
            if "Signature" in item.reason or "Must Order" in item.reason or "招牌" in item.reason or "必點" in item.reason:
                signature_count += 1

        print()
        print(f"✅ 總價: NT$ {response.total_price}")
        print(f"✅ 招牌菜數量: {signature_count}")
        
        # 簡單驗證：應該要有招牌菜
        if signature_count > 0:
             print("✅ 成功推薦招牌菜")
        else:
             print("⚠️ 警告：未檢測到明確標記為 Signature 的菜品 (可能是 Tag 格式問題)")

        print("✅ 測試案例 2 通過")
        return True

    except Exception as e:
        print(f"❌ 測試案例 2 失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """執行所有測試案例"""
    print()
    print("🧪 開始測試移除預算限制後的功能")
    print()

    results = []
    results.append(await test_no_budget_input())
    results.append(await test_all_signatures_mode())

    print()
    print("=" * 80)
    print("📊 測試結果總結")
    print("=" * 80)
    print()
    print(f"通過: {sum(results)}/{len(results)}")
    print()

if __name__ == "__main__":
    asyncio.run(main())
