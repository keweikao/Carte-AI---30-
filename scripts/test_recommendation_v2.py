"""
Test script for V2 Recommendation System
Tests the complete flow: Pipeline → Firestore → Recommendation API
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pipeline.orchestrator import RestaurantPipeline
from services.firestore_service import save_restaurant_profile, get_restaurant_profile
from agent.recommendation import RecommendationService
from schemas.recommendation import UserInputV2, BudgetV2


async def test_full_pipeline():
    """Test complete pipeline with recommendation"""

    # Test restaurant
    restaurant_name = "四平小館"

    print(f"\n{'='*80}")
    print(f"Testing V2 Recommendation System with: {restaurant_name}")
    print(f"{'='*80}\n")

    # STEP 1: Run pipeline to generate restaurant profile
    print("STEP 1: Running restaurant pipeline...")
    pipeline = RestaurantPipeline()
    profile = await pipeline.process(restaurant_name)

    if not profile:
        print("❌ Pipeline failed to generate profile")
        return

    print(f"✓ Pipeline complete")
    print(f"  - Place ID: {profile.place_id}")
    print(f"  - Menu items: {len(profile.menu_items)}")
    print(f"  - Items with analysis: {sum(1 for item in profile.menu_items if item.analysis)}")

    # STEP 2: Save to Firestore
    print("\nSTEP 2: Saving profile to Firestore...")
    success = save_restaurant_profile(profile)

    if not success:
        print("❌ Failed to save to Firestore")
        return

    print("✓ Profile saved to Firestore")

    # STEP 3: Retrieve from Firestore to verify
    print("\nSTEP 3: Retrieving profile from Firestore...")
    retrieved_profile_dict = get_restaurant_profile(profile.place_id)

    if not retrieved_profile_dict:
        print("❌ Failed to retrieve from Firestore")
        return

    # Count items with analysis in retrieved profile
    retrieved_menu_items = retrieved_profile_dict.get('menu_items', [])
    items_with_analysis = sum(1 for item in retrieved_menu_items if item.get('analysis'))

    print(f"✓ Profile retrieved successfully")
    print(f"  - Menu items: {len(retrieved_menu_items)}")
    print(f"  - Items with analysis: {items_with_analysis}")

    # STEP 4: Test recommendation system
    print("\nSTEP 4: Testing recommendation system...")

    # Test case 1: 2 people, no spicy, budget $300
    print("\n--- Test Case 1: 2 friends, no spicy, budget $300 ---")
    user_input_1 = UserInputV2(
        restaurant_name=profile.name,
        place_id=profile.place_id,
        dining_style="Shared",
        party_size=2,
        preferences=["不辣", "No_Spicy"],
        budget=BudgetV2(total=300)
    )

    rec_service = RecommendationService()

    # Convert dict back to RestaurantProfile for recommendation
    from schemas.restaurant_profile import RestaurantProfile
    profile_for_rec = RestaurantProfile.model_validate(retrieved_profile_dict)

    recommendations = await rec_service.generate_recommendation(
        user_input=user_input_1,
        profile=profile_for_rec
    )

    print(f"\n✓ Generated {len(recommendations.recommendations)} recommendations")
    print(f"  - Total price: ${recommendations.total_estimated_price}")
    print(f"  - Reasoning: {recommendations.reasoning}")

    print("\n  Recommended dishes:")
    for i, rec in enumerate(recommendations.recommendations, 1):
        print(f"    {i}. {rec.dish.name} x{rec.quantity}")
        print(f"       Price: ${rec.dish.price}")
        print(f"       Reason: {rec.reason}")
        if rec.highlight_note:
            print(f"       Note: {rec.highlight_note}")

    # Test case 2: 5 people, anything is fine
    print("\n--- Test Case 2: 5 friends, no restrictions ---")
    user_input_2 = UserInputV2(
        restaurant_name=profile.name,
        place_id=profile.place_id,
        dining_style="Shared",
        party_size=5,
        preferences=[],
        natural_input="我們什麼都吃，想嘗試招牌菜"
    )

    recommendations_2 = await rec_service.generate_recommendation(
        user_input=user_input_2,
        profile=profile_for_rec
    )

    print(f"\n✓ Generated {len(recommendations_2.recommendations)} recommendations")
    print(f"  - Total price: ${recommendations_2.total_estimated_price}")
    print(f"  - Reasoning: {recommendations_2.reasoning}")

    print("\n  Recommended dishes:")
    for i, rec in enumerate(recommendations_2.recommendations, 1):
        print(f"    {i}. {rec.dish.name} x{rec.quantity}")
        print(f"       Price: ${rec.dish.price}")
        print(f"       Reason: {rec.reason}")

    print(f"\n{'='*80}")
    print("✅ All tests completed successfully!")
    print(f"{'='*80}\n")


async def test_cached_restaurant():
    """Test with cached restaurant (faster, doesn't require Apify)"""

    # Use cached 八方雲集 with known place_id
    place_id = "ChIJm8L9_RypQjQRPo-Y6pKHpPM"
    restaurant_name = "八方雲集 烏日溪南店"

    print(f"\n{'='*80}")
    print(f"Testing V2 Recommendation with CACHED restaurant: {restaurant_name}")
    print(f"{'='*80}\n")

    # Retrieve from Firestore
    print("Retrieving cached profile from Firestore...")
    profile_dict = get_restaurant_profile(place_id)

    if not profile_dict:
        print(f"❌ Restaurant {place_id} not found in cache")
        print("   Please run full pipeline test first")
        return

    # Check if it has analysis data
    menu_items = profile_dict.get('menu_items', [])
    items_with_analysis = sum(1 for item in menu_items if item.get('analysis'))

    print(f"✓ Profile found in cache")
    print(f"  - Menu items: {len(menu_items)}")
    print(f"  - Items with analysis: {items_with_analysis}")

    if items_with_analysis == 0:
        print("\n⚠️  WARNING: No items have analysis data!")
        print("   The cached profile needs to be regenerated with new pipeline")
        print("   Recommendations will be limited without DishAttributes")

    # Convert to RestaurantProfile
    from schemas.restaurant_profile import RestaurantProfile
    profile = RestaurantProfile.model_validate(profile_dict)

    # Test recommendation
    print("\n--- Testing Recommendation: 2 people, no spicy ---")
    user_input = UserInputV2(
        restaurant_name=profile.name,
        place_id=profile.place_id,
        dining_style="Shared",
        party_size=2,
        preferences=["不辣"],
        budget=BudgetV2(total=200)
    )

    rec_service = RecommendationService()
    recommendations = await rec_service.generate_recommendation(
        user_input=user_input,
        profile=profile
    )

    print(f"\n✓ Generated {len(recommendations.recommendations)} recommendations")
    print(f"  - Total price: ${recommendations.total_estimated_price}")
    print(f"  - Reasoning: {recommendations.reasoning}")

    if recommendations.recommendations:
        print("\n  Recommended dishes:")
        for i, rec in enumerate(recommendations.recommendations, 1):
            print(f"    {i}. {rec.dish.name} x{rec.quantity}")
            print(f"       Price: ${rec.dish.price}")
            print(f"       Category: {rec.dish.category}")
            print(f"       Reason: {rec.reason}")
            if rec.highlight_note:
                print(f"       Note: {rec.highlight_note}")
    else:
        print("\n⚠️  No recommendations generated")
        print("   This may be due to missing DishAttributes")

    print(f"\n{'='*80}")
    print("✅ Test completed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Test V2 Recommendation System')
    parser.add_argument('--cached', action='store_true',
                       help='Use cached restaurant (faster, no Apify required)')
    parser.add_argument('--full', action='store_true',
                       help='Run full pipeline (requires Apify quota)')

    args = parser.parse_args()

    if args.full:
        asyncio.run(test_full_pipeline())
    elif args.cached:
        asyncio.run(test_cached_restaurant())
    else:
        # Default: run cached test
        print("Running cached test by default (use --full for complete pipeline test)")
        asyncio.run(test_cached_restaurant())
