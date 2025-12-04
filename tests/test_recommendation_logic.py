import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from agent.recommendation import RecommendationService
from schemas.recommendation import UserInputV2, BudgetV2
from schemas.restaurant_profile import RestaurantProfile, MenuItem, DishAttributes, MenuItemAnalysis

async def test_soft_ranking():
    print("Testing _soft_ranking logic...")
    
    # Mock User Input
    user_input = UserInputV2(
        restaurant_name="Test Restaurant",
        dining_style="Shared",
        party_size=4,
        budget=BudgetV2(type="Total", amount=2000),
        preferences=["Spicy"]
    )
    
    # Mock Profile
    profile = RestaurantProfile(
        place_id="mock-id",
        name="Test Restaurant",
        address="Test Address",
        updated_at=datetime.now(),
        trust_level="high",
        menu_source_url="http://test.com",
        review_summary="Good food",
        menu_items=[
            MenuItem(
                name="Spicy Chicken",
                price=300,
                category="Main",
                description="Spicy chicken dish",
                ai_insight=MenuItemAnalysis(sentiment="positive", summary="Good", mention_count=10),
                analysis=DishAttributes(is_spicy=True, flavors=["spicy"])
            ),
            MenuItem(
                name="Vegetable Stir Fry",
                price=200,
                category="Side",
                description="Fresh vegetables",
                ai_insight=MenuItemAnalysis(sentiment="positive", summary="Healthy", mention_count=5),
                analysis=DishAttributes(is_vegan=True, flavors=["fresh"])
            )
        ]
    )
    
    service = RecommendationService()
    
    # Test _fallback_ranking
    print("\nTesting _fallback_ranking...")
    fallback_result = service._fallback_ranking(profile.menu_items, user_input, profile)
    
    print(f"Fallback Result Items: {len(fallback_result.items)}")
    for item in fallback_result.items:
        print(f"- {item.display.dish_name} (Qty: {item.display.quantity}, Reason: {item.display.reason})")
        
    assert len(fallback_result.items) > 0
    assert fallback_result.items[0].display.quantity == 1
    assert fallback_result.items[0].display.category in ["Main", "Side"]
    
    print("\nTest Passed!")

if __name__ == "__main__":
    asyncio.run(test_soft_ranking())
