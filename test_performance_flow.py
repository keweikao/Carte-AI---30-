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
MOCK_PLACE_DETAILS = {
    "name": "葉公館滬菜",
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
紅燒肉 $380
醃篤鮮 $450
清炒蝦仁 $420
蔥油拌麵 $120
小籠包 $180 (8顆)
松鼠黃魚 $880
蟹粉豆腐 $360
東坡肉 $420
上海菜飯 $220
干煸四季豆 $280
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
        docs = db.collection('restaurant_profiles').where('restaurant_name', '==', '葉公館滬菜').stream()
        for doc in docs:
            doc.reference.delete()
            print(f"   Deleted existing profile: {doc.id}")
    except Exception as e:
        print(f"   Cleanup warning: {e}")

    # Prepare User Input
    user_input = UserInputV2(
        restaurant_name="葉公館滬菜",
        place_id="mock_place_id_ye_gong_guan", # Use mock ID
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
        return None

    # Patch the data fetchers
    with patch('agent.profile_agent.fetch_place_details', side_effect=mock_fetch_details), \
         patch('agent.profile_agent.fetch_menu_from_search', side_effect=mock_fetch_menu), \
         patch('agent.data_fetcher.fetch_place_photo', side_effect=mock_fetch_photo):
        
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

if __name__ == "__main__":
    asyncio.run(run_performance_test())
