#!/usr/bin/env python3
"""
本地測試 Vision API fallback 實作
測試各個組件是否正常運作

使用方式：
python3 scripts/test_vision_api_local.py
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.menu_scraper import MenuScraper
from services.restaurant_aggregator import _fetch_restaurant_address
from dotenv import load_dotenv

load_dotenv()

async def test_fetch_images():
    """測試圖片抓取功能"""
    print("\n" + "="*60)
    print("測試 1: fetch_restaurant_images()")
    print("="*60)

    scraper = MenuScraper()

    # 測試餐廳：鼎泰豐信義店
    place_id = "ChIJ-x-t9W_eQjQRhFjU2g08sHk"
    restaurant_name = "鼎泰豐"

    print(f"餐廳: {restaurant_name}")
    print(f"Place ID: {place_id}")

    try:
        image_urls = await scraper.fetch_restaurant_images(place_id, restaurant_name, max_images=5)

        if image_urls:
            print(f"✅ 成功抓取 {len(image_urls)} 張圖片")
            for idx, url in enumerate(image_urls[:3], 1):
                print(f"   {idx}. {url[:80]}...")
            if len(image_urls) > 3:
                print(f"   ... 還有 {len(image_urls) - 3} 張圖片")
            return True, image_urls
        else:
            print("❌ 未抓取到圖片")
            return False, []
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False, []


async def test_extract_menu_from_images(image_urls):
    """測試 Vision API 菜單提取"""
    print("\n" + "="*60)
    print("測試 2: extract_menu_from_images()")
    print("="*60)

    if not image_urls:
        print("⚠️  跳過測試（無圖片）")
        return False, []

    scraper = MenuScraper()

    print(f"處理 {len(image_urls)} 張圖片...")

    try:
        menu_items = await scraper.extract_menu_from_images(image_urls)

        if menu_items:
            print(f"✅ 成功提取 {len(menu_items)} 道菜")
            print("\n菜單預覽（前 5 道）：")
            for idx, item in enumerate(menu_items[:5], 1):
                price_str = f"NT$ {item.price}" if item.price else "價格不明"
                print(f"   {idx}. {item.name:20s} | {price_str:12s} | {item.category}")
            if len(menu_items) > 5:
                print(f"   ... 還有 {len(menu_items) - 5} 道菜")
            return True, menu_items
        else:
            print("❌ 未提取到菜單項目")
            return False, []
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False, []


async def test_vision_api_fallback():
    """測試完整的 vision_api_fallback 流程"""
    print("\n" + "="*60)
    print("測試 3: vision_api_fallback() 完整流程")
    print("="*60)

    scraper = MenuScraper()

    # 測試餐廳：欣葉小聚今品
    place_id = "ChIJT_tO6SupQjQRx7bH6OqW0lQ"
    restaurant_name = "欣葉小聚今品"

    print(f"餐廳: {restaurant_name}")
    print(f"Place ID: {place_id}")

    try:
        menu_items = await scraper.vision_api_fallback(place_id, restaurant_name)

        if menu_items:
            print(f"✅ 成功回傳 {len(menu_items)} 道菜")

            # 檢查是否是 Fallback Dish
            if len(menu_items) == 1 and menu_items[0].name == "Fallback Dish":
                print("⚠️  回傳的是 Fallback Dish（表示提取失敗）")
                return False
            else:
                print("\n菜單預覽：")
                for idx, item in enumerate(menu_items[:5], 1):
                    price_str = f"NT$ {item.price}" if item.price else "價格不明"
                    print(f"   {idx}. {item.name:20s} | {price_str:12s} | {item.category}")
                return True
        else:
            print("❌ 未回傳任何菜單")
            return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fetch_address():
    """測試地址抓取功能"""
    print("\n" + "="*60)
    print("測試 4: _fetch_restaurant_address()")
    print("="*60)

    place_id = "ChIJ-x-t9W_eQjQRhFjU2g08sHk"
    restaurant_name = "鼎泰豐"

    print(f"餐廳: {restaurant_name}")
    print(f"Place ID: {place_id}")

    try:
        address = await _fetch_restaurant_address(place_id, restaurant_name)

        if address and address != "Address not available":
            print(f"✅ 成功取得地址: {address}")
            return True
        else:
            print(f"❌ 未取得地址: {address}")
            return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """執行所有測試"""
    print("\n" + "🧪 " * 30)
    print("Vision API Fallback 本地測試")
    print("🧪 " * 30)

    results = {}

    # 測試 1: 抓取圖片
    success1, image_urls = await test_fetch_images()
    results["fetch_images"] = success1

    # 測試 2: 提取菜單（使用測試 1 的圖片）
    if success1:
        success2, menu_items = await test_extract_menu_from_images(image_urls)
        results["extract_menu"] = success2
    else:
        results["extract_menu"] = None  # 跳過

    # 測試 3: 完整 fallback 流程
    success3 = await test_vision_api_fallback()
    results["vision_api_fallback"] = success3

    # 測試 4: 抓取地址
    success4 = await test_fetch_address()
    results["fetch_address"] = success4

    # 總結
    print("\n" + "="*60)
    print("測試總結")
    print("="*60)

    passed = sum(1 for v in results.values() if v is True)
    total = sum(1 for v in results.values() if v is not None)

    for test_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        print(f"{status} | {test_name}")

    print(f"\n通過率: {passed}/{total} ({passed/total*100:.0f}%)" if total > 0 else "\n無有效測試")

    if passed == total and total > 0:
        print("\n🎉 所有測試通過！可以進行部署。")
        return 0
    else:
        print("\n⚠️  部分測試失敗，請修復後再部署。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
