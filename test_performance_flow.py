import os
import time
import asyncio
import json
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# 1. Environment Setup
load_dotenv()
os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0415289079"

# Ensure we have the Gemini Key (critical for Agents)
if not os.getenv("GEMINI_API_KEY"):
    print("⚠️  WARNING: GEMINI_API_KEY not found in environment. Agents may fail.")

# 2. Mock Data for "葉公館滬菜"
TEST_RESTAURANT_NAME = "葉公館滬菜_Test_Fix_Category"
TEST_PLACE_ID = "mock_place_id_ye_gong_guan_fix"

MOCK_PLACE_DETAILS = {
    "name": TEST_RESTAURANT_NAME,
    "rating": 4.5,
    "formatted_address": "台北市大安區安和路二段118號",
    "reviews": [
        {"text": "紅燒肉非常好吃，肥而不膩，必點！", "rating": 5},
        {"text": "醃篤鮮湯頭濃郁，適合多人分享。", "rating": 5},
        {"text": "清炒蝦仁很新鮮，口感彈牙。", "rating": 4},
        {"text": "蔥油拌麵味道道地，價格實惠。", "rating": 4},
        {"text": "小籠包皮薄餡多，不輸鼎泰豐。", "rating": 5},
        {"text": "適合商務聚餐，環境優雅。", "rating": 5}
    ],
    "types": ["restaurant", "food", "point_of_interest", "establishment"],
    "photos": [{"photo_reference": "mock_ref_1"}, {"photo_reference": "mock_ref_2"}]
}

MOCK_MENU_TEXT = """
Title: 葉公館滬菜菜單
Snippet: 
紅燒肉 $480
醃篤鮮 $880
清炒蝦仁 $580
蔥油拌麵 $120
小籠包 $220 (8顆)
松鼠黃魚 $1280
蟹粉豆腐 $460
東坡肉 $520
上海菜飯 $240
干煸四季豆 $320
四喜烤麩 $180
清蒸石斑魚 $1280
清炒時蔬 $280
醉雞 $380
獅子頭 $420
無錫排骨 $560
雪菜百頁 $260
豆沙鍋餅 $280
"""

# 3. Test Logic
async def run_performance_test():
    print("\n🚀 Starting Performance Test for '葉公館滬菜'...")
    print("Scenario: 7 People, Business Dining, No Restrictions")
    
    # Import here to ensure env vars are set before module init
    from agent.dining_agent import DiningAgent
    from schemas.recommendation import UserInputV2, BudgetV2
    from services.firestore_service import db
    
    # Clean up DB before start to ensure Cold Start
    print("🧹 Cleaning up database...")
    try:
        # Try cleaning up by name and mock ID
        docs = db.collection('restaurants').where('name', '==', TEST_RESTAURANT_NAME).stream()
        for doc in docs:
            doc.reference.delete()
            print(f"   Deleted existing profile: {doc.id}")
            
        # Also try direct ID delete
        doc_ref = db.collection('restaurants').document(TEST_PLACE_ID)
        if doc_ref.get().exists:
             doc_ref.delete()
             print(f"   Deleted existing profile by ID: {TEST_PLACE_ID}")

    except Exception as e:
        print(f"   Cleanup warning: {e}")

    # Prepare User Input
    user_input = UserInputV2(
        restaurant_name=TEST_RESTAURANT_NAME,
        place_id=TEST_PLACE_ID, # Use mock ID
        party_size=7,
        occasion="Business",
        dining_style="Shared",
        budget=BudgetV2(type="Total", amount=10000), # High budget for business
        preferences=[],
        language="繁體中文"
    )

    # Define Mock Side Effects with Delay
    async def mock_fetch_details(*args, **kwargs):
        print("   [Crawler] Fetching place details from Google Maps... (Simulated 3s delay)")
        await asyncio.sleep(3)
        return MOCK_PLACE_DETAILS

    async def mock_fetch_menu(*args, **kwargs):
        print("   [Crawler] Searching for menu online... (Simulated 3s delay)")
        await asyncio.sleep(3)
        return MOCK_MENU_TEXT

    async def mock_fetch_photo(*args, **kwargs):
        return b"fake_image_bytes"

    # Mock OCR Result
    async def mock_ocr_execute(images):
        print("   [OCR] Simulating successful menu extraction...")
        return [
            {"dish_name": "紅燒肉", "price": 480, "category": "熱菜", "description": "招牌菜"},
            {"dish_name": "醃篤鮮", "price": 880, "category": "湯品", "description": "濃郁"},
            {"dish_name": "清炒蝦仁", "price": 580, "category": "熱菜", "description": "清爽"},
            {"dish_name": "蔥油拌麵", "price": 120, "category": "主食", "description": "香氣十足"},
            {"dish_name": "小籠包", "price": 220, "category": "點心", "description": "皮薄餡多"},
            {"dish_name": "松鼠黃魚", "price": 1280, "category": "熱菜", "description": "酸甜開胃"},
            {"dish_name": "蟹粉豆腐", "price": 460, "category": "熱菜", "description": "下飯"},
            {"dish_name": "東坡肉", "price": 520, "category": "熱菜", "description": "軟嫩"},
            {"dish_name": "上海菜飯", "price": 240, "category": "主食", "description": "經典"},
            {"dish_name": "干煸四季豆", "price": 320, "category": "熱菜", "description": "夠味"},
            {"dish_name": "四喜烤麩", "price": 180, "category": "冷盤", "description": "傳統"},
            {"dish_name": "清蒸石斑魚", "price": 1280, "category": "熱菜", "description": "新鮮"},
            {"dish_name": "清炒時蔬", "price": 280, "category": "熱菜", "description": "健康"},
            {"dish_name": "醉雞", "price": 380, "category": "冷盤", "description": "酒香"},
            {"dish_name": "獅子頭", "price": 420, "category": "熱菜", "description": "手工"},
            {"dish_name": "無錫排骨", "price": 560, "category": "熱菜", "description": "酥爛"},
            {"dish_name": "雪菜百頁", "price": 260, "category": "熱菜", "description": "清淡"},
            {"dish_name": "豆沙鍋餅", "price": 280, "category": "點心", "description": "甜點"}
        ]

    # Patch the data fetchers AND the OCR skill
    with patch('agent.profile_agent.fetch_place_details', side_effect=mock_fetch_details), \
         patch('agent.profile_agent.fetch_menu_from_search', side_effect=mock_fetch_menu), \
         patch('agent.agents.fetch_menu_from_search', side_effect=mock_fetch_menu), \
         patch('agent.data_fetcher.fetch_place_photo', side_effect=mock_fetch_photo), \
         patch('agent.skills.MenuExtractionSkill.execute', side_effect=mock_ocr_execute):
        
        agent = DiningAgent()

        # --- First Run (Cold Start) ---
        print("\n🔵 [Run 1] Cold Start (Crawling + Analysis)...")
        start_time = time.time()
        
        try:
            result1 = await agent.get_recommendations_v2(user_input)
            duration1 = time.time() - start_time
            print(f"✅ Run 1 Complete in {duration1:.2f} seconds")
            
            # Verify it was a cold start
            if result1.user_info and result1.user_info.get("is_cache_hit"):
                print("   ⚠️  Warning: Agent reported Cache Hit for Run 1 (Unexpected)")
            
            print(f"   Menu Items: {len(result1.items)}")
            print(f"   Total Price: {result1.total_price}")
            
        except Exception as e:
            print(f"❌ Run 1 Failed: {e}")
            import traceback
            traceback.print_exc()
            return

        # --- Second Run (Warm Start) ---
        print("\n🟠 [Run 2] Warm Start (Using Golden Profile)...")
        start_time = time.time()
        
        try:
            result2 = await agent.get_recommendations_v2(user_input)
            duration2 = time.time() - start_time
            print(f"✅ Run 2 Complete in {duration2:.2f} seconds")
            
            print(f"   Menu Items: {len(result2.items)}")
            print(f"   Total Price: {result2.total_price}")
            
        except Exception as e:
            print(f"❌ Run 2 Failed: {e}")
            return

        # --- Summary ---
        print("\n" + "="*40)
        print("📊 Performance Comparison")
        print("="*40)
        print(f"1. Cold Start: {duration1:.2f} s")
        print(f"2. Warm Start: {duration2:.2f} s")
        print(f"🚀 Speedup:    {duration1 / duration2:.1f}x Faster")
        print(f"⏱  Time Saved: {duration1 - duration2:.2f} s")
        print("="*40)
        
        # Show Menu
        print("\n🍽  Recommended Menu (Run 2):")
        for item in result2.items:
            print(f"- {item.display.dish_name} (${item.display.price}) x{item.display.quantity} [{item.display.reason}]")
            print(f"  ↳ Alternatives: {len(item.alternatives)} items found")
            for alt in item.alternatives:
                 print(f"    - {alt.dish_name} (${alt.price}) [{alt.category}]")

if __name__ == "__main__":
    asyncio.run(run_performance_test())
