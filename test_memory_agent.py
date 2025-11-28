"""
Test script for Personal Memory System

This script demonstrates the Memory Agent functionality:
1. Save user feedback (rejected/loved dishes)
2. Retrieve personal memory
3. Test memory integration in recommendations
"""

import asyncio
from agent.memory_agent import MemoryAgent

async def test_memory_system():
    print("="*80)
    print("🧪 Testing Personal Memory System")
    print("="*80)
    
    memory_agent = MemoryAgent()
    test_user_id = "test_user_001"
    
    # Test 1: Save feedback
    print("\n📝 Test 1: Saving User Feedback...")
    print("-"*80)
    
    selected_dishes = [
        {"dish_name": "小籠包", "category": "點心"},
        {"dish_name": "佛跳牆", "category": "湯品"}
    ]
    
    rejected_dishes = [
        {"dish_name": "臭豆腐", "reason": "Too smelly for business occasions"},
        {"dish_name": "蒜泥白肉", "reason": "I don't like garlic"}
    ]
    
    success = await memory_agent.save_feedback(
        user_id=test_user_id,
        recommendation_id="rec_001",
        selected_dishes=selected_dishes,
        rejected_dishes=rejected_dishes,
        occasion="business"
    )
    
    if success:
        print("✅ Feedback saved successfully!")
    else:
        print("❌ Failed to save feedback")
        return
    
    # Test 2: Retrieve memory
    print("\n📚 Test 2: Retrieving Personal Memory...")
    print("-"*80)
    
    memory_context = await memory_agent.get_personal_memory(
        user_id=test_user_id,
        occasion="business"
    )
    
    if memory_context:
        print("✅ Memory retrieved successfully!")
        print("\nMemory Context:")
        print(memory_context)
    else:
        print("⚠️  No memory found (this is expected for new users)")
    
    # Test 3: Update general preferences
    print("\n⚙️  Test 3: Updating General Preferences...")
    print("-"*80)
    
    success = await memory_agent.update_general_preferences(
        user_id=test_user_id,
        preferences={
            "spice_tolerance": "low",
            "portion_preference": "regular",
            "price_sensitivity": "moderate"
        }
    )
    
    if success:
        print("✅ General preferences updated!")
    else:
        print("❌ Failed to update preferences")
    
    # Test 4: Update occasion-specific preference
    print("\n🎯 Test 4: Updating Occasion Preferences...")
    print("-"*80)
    
    success = await memory_agent.update_occasion_preference(
        user_id=test_user_id,
        occasion="business",
        preference_updates={
            "avoid_categories": ["臭豆腐", "大蒜重的菜"],
            "prefer_categories": ["湯品", "海鮮"],
            "notes": "Prefer elegant, easy-to-share dishes"
        }
    )
    
    if success:
        print("✅ Occasion preferences updated!")
    else:
        print("❌ Failed to update occasion preferences")
    
    # Test 5: Retrieve updated memory
    print("\n📚 Test 5: Retrieving Updated Memory...")
    print("-"*80)
    
    memory_context = await memory_agent.get_personal_memory(
        user_id=test_user_id,
        occasion="business"
    )
    
    print("\nUpdated Memory Context:")
    print(memory_context)
    
    # Test 6: Get memory stats
    print("\n📊 Test 6: Memory Statistics...")
    print("-"*80)
    
    stats = await memory_agent.get_memory_stats(user_id=test_user_id)
    
    print(f"Has Memory: {stats.get('has_memory')}")
    print(f"Loved Dishes: {stats.get('loved_count')}")
    print(f"Rejected Dishes: {stats.get('rejected_count')}")
    print(f"Occasions Tracked: {stats.get('occasions_tracked')}")
    
    # Test 7: Test with different occasion
    print("\n🎭 Test 7: Memory for Different Occasion (Date)...")
    print("-"*80)
    
    date_memory = await memory_agent.get_personal_memory(
        user_id=test_user_id,
        occasion="date"
    )
    
    print("Date Occasion Memory:")
    print(date_memory if date_memory else "No specific date preferences yet")
    
    print("\n" + "="*80)
    print("✅ All tests completed!")
    print("="*80)
    
    # Optional: Clean up test data
    print("\n🧹 Cleanup: Do you want to clear test user memory? (This is just a test)")
    print("   (In production, this would be for GDPR compliance)")
    # Uncomment to actually clear:
    # await memory_agent.clear_user_memory(test_user_id)
    # print("✅ Test user memory cleared")

if __name__ == '__main__':
    asyncio.run(test_memory_system())
