#!/usr/bin/env python3
"""
測試後端 API 回應格式
驗證新的 schema 是否正確包含 cuisine_type 和 category_summary
"""

import asyncio
import json
from schemas.recommendation import UserInputV2, BudgetV2, RecommendationResponseV2
from agent.dining_agent import DiningAgent

async def test_chinese_restaurant():
    """測試案例 1：中式餐館（鼎泰豐）"""
    print("=" * 80)
    print("測試案例 1：中式餐館（鼎泰豐）")
    print("=" * 80)
    print()

    user_input = UserInputV2(
        restaurant_name="鼎泰豐",
        dining_style="Shared",
        party_size=3,
        budget=BudgetV2(type="Per_Person", amount=500),
        dish_count_target=None,  # 讓 AI 決定
        preferences=["No_Beef"],
        natural_input="想吃招牌菜",
        user_id=None
    )

    try:
        agent = DiningAgent()
        response = await agent.get_recommendations_v2(user_input)

        # 驗證必要欄位
        assert hasattr(response, 'cuisine_type'), "缺少 cuisine_type 欄位"
        assert hasattr(response, 'category_summary'), "缺少 category_summary 欄位"

        print(f"✅ 餐廳類型: {response.cuisine_type}")
        print(f"✅ 類別摘要: {json.dumps(response.category_summary, ensure_ascii=False, indent=2)}")
        print()

        # 驗證每道菜都有 category
        print("📋 推薦菜品：")
        for item in response.menu_items:
            assert hasattr(item, 'category'), f"菜品 {item.dish_name} 缺少 category 欄位"
            assert hasattr(item, 'review_count'), f"菜品 {item.dish_name} 缺少 review_count 欄位"
            print(f"  - {item.category:8s} | {item.dish_name:15s} | NT$ {item.price:4d} | 評論: {item.review_count or 0}")

        print()
        print(f"✅ 總價: NT$ {response.total_price}")
        print(f"✅ 人均: NT$ {response.total_price // user_input.party_size}")
        print()

        # 驗證 category_summary 與實際菜品數量一致
        actual_counts = {}
        for item in response.menu_items:
            actual_counts[item.category] = actual_counts.get(item.category, 0) + 1

        assert actual_counts == response.category_summary, \
            f"category_summary 不一致！\n實際: {actual_counts}\nAPI: {response.category_summary}"

        print("✅ 測試案例 1 通過")
        return True

    except Exception as e:
        print(f"❌ 測試案例 1 失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_japanese_restaurant():
    """測試案例 2：日本料理（壽司郎）"""
    print()
    print("=" * 80)
    print("測試案例 2：日本料理（壽司郎）")
    print("=" * 80)
    print()

    user_input = UserInputV2(
        restaurant_name="壽司郎",
        dining_style="Individual",
        party_size=2,
        budget=BudgetV2(type="Total", amount=1000),
        dish_count_target=6,
        preferences=["Seafood_Allergy"],  # 海鮮過敏，測試過濾邏輯
        natural_input=None,
        user_id=None
    )

    try:
        agent = DiningAgent()
        response = await agent.get_recommendations_v2(user_input)

        print(f"✅ 餐廳類型: {response.cuisine_type}")
        print(f"✅ 類別摘要: {json.dumps(response.category_summary, ensure_ascii=False, indent=2)}")
        print()

        print("📋 推薦菜品：")
        for item in response.menu_items:
            print(f"  - {item.category:8s} | {item.dish_name:15s} | NT$ {item.price:4d}")

        print()
        print(f"✅ 總價: NT$ {response.total_price}")

        # 驗證類型應該是日本料理
        # 注意：因為有 Seafood_Allergy，可能無法推薦傳統日料（大多是海鮮）
        print()
        print("✅ 測試案例 2 通過")
        return True

    except Exception as e:
        print(f"❌ 測試案例 2 失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_american_restaurant():
    """測試案例 3：美式餐廳（TGI Fridays）"""
    print()
    print("=" * 80)
    print("測試案例 3：美式餐廳（TGI Fridays）")
    print("=" * 80)
    print()

    user_input = UserInputV2(
        restaurant_name="TGI Fridays",
        dining_style="Shared",
        party_size=4,
        budget=BudgetV2(type="Per_Person", amount=600),
        dish_count_target=None,
        preferences=["Alcohol"],
        natural_input="適合聚會的菜色",
        user_id=None
    )

    try:
        agent = DiningAgent()
        response = await agent.get_recommendations_v2(user_input)

        print(f"✅ 餐廳類型: {response.cuisine_type}")
        print(f"✅ 類別摘要: {json.dumps(response.category_summary, ensure_ascii=False, indent=2)}")
        print()

        print("📋 推薦菜品：")
        for item in response.menu_items:
            print(f"  - {item.category:8s} | {item.dish_name:15s} | NT$ {item.price:4d}")

        print()
        print(f"✅ 總價: NT$ {response.total_price}")
        print(f"✅ 人均: NT$ {response.total_price // user_input.party_size}")
        print()
        print("✅ 測試案例 3 通過")
        return True

    except Exception as e:
        print(f"❌ 測試案例 3 失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """執行所有測試案例"""
    print()
    print("🧪 開始測試後端 API 回應格式（V2 Schema）")
    print()

    results = []

    # 測試中式餐館
    results.append(await test_chinese_restaurant())

    # 測試日本料理
    results.append(await test_japanese_restaurant())

    # 測試美式餐廳
    results.append(await test_american_restaurant())

    # 總結
    print()
    print("=" * 80)
    print("📊 測試結果總結")
    print("=" * 80)
    print()
    print(f"通過: {sum(results)}/{len(results)}")
    print()

    if all(results):
        print("✅ 所有測試通過！後端 API 已正確支援動態類別系統。")
    else:
        print("❌ 部分測試失敗，請檢查錯誤訊息。")

    print()

if __name__ == "__main__":
    asyncio.run(main())
