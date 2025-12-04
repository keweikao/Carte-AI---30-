from datetime import datetime
from schemas.restaurant_profile import RestaurantProfile, MenuItem, DishAttributes, MenuItemAnalysis
from schemas.recommendation import RecommendationResponseV2, DishSlotResponse, MenuItemV2
import uuid

class MockService:
    @staticmethod
    def get_mock_profile(restaurant_name: str) -> RestaurantProfile:
        """Returns a mock restaurant profile for testing"""
        print(f"[MockService] Generating mock profile for {restaurant_name}")
        return RestaurantProfile(
            place_id="mock-place-id",
            name=restaurant_name,
            address="測試地址",
            updated_at=datetime.now(),
            trust_level="high",
            menu_source_url="https://example.com",
            review_summary="測試餐廳評價",
            menu_items=[
                MenuItem(
                    name="宮保雞丁", 
                    price=300, 
                    category="熱菜", 
                    description="Spicy chicken",
                    analysis=DishAttributes(
                        is_spicy=True, 
                        contains_beef=False, 
                        contains_pork=False, 
                        contains_seafood=False,
                        is_vegan=False,
                        allergens=["peanuts"],
                        flavors=["spicy"],
                        textures=["tender"],
                        temperature="hot",
                        cooking_method="stir-fry",
                        suitable_occasions=["casual"],
                        is_signature=True,
                        sentiment_score=0.8,
                        highlight_review="Great!"
                    ),
                    ai_insight=MenuItemAnalysis(
                        sentiment="positive",
                        summary="Good",
                        mention_count=10
                    ),
                    is_popular=True,
                    is_risky=False
                ),
                MenuItem(
                    name="炒青菜", 
                    price=150, 
                    category="蔬菜", 
                    description="Stir-fried vegetables",
                    analysis=DishAttributes(
                        is_spicy=False,
                        is_vegan=True,
                        allergens=[],
                        flavors=["salty"],
                        textures=["crispy"],
                        temperature="hot",
                        cooking_method="stir-fry",
                        suitable_occasions=["casual"],
                        is_signature=False,
                        sentiment_score=0.7,
                        highlight_review="Fresh"
                    ),
                    ai_insight=MenuItemAnalysis(
                        sentiment="positive",
                        summary="Healthy",
                        mention_count=5
                    ),
                    is_popular=False,
                    is_risky=False
                )
            ]
        )

    @staticmethod
    def get_mock_recommendation(restaurant_name: str) -> RecommendationResponseV2:
        """Returns a mock recommendation response for testing"""
        print(f"[MockService] Generating mock recommendation for {restaurant_name}")
        return RecommendationResponseV2(
            recommendation_id=str(uuid.uuid4()),
            restaurant_name=restaurant_name,
            recommendation_summary="Mock recommendation summary",
            total_price=450,
            cuisine_type="中式餐館",
            category_summary={"熱菜": 1, "蔬菜": 1},
            items=[
                DishSlotResponse(
                    category="熱菜",
                    display=MenuItemV2(
                        dish_name="宮保雞丁",
                        price=300,
                        quantity=1,
                        reason="經典川菜，香辣可口",
                        category="熱菜",
                        review_count=10
                    ),
                    alternatives=[]
                ),
                DishSlotResponse(
                    category="蔬菜",
                    display=MenuItemV2(
                        dish_name="炒青菜",
                        price=150,
                        quantity=1,
                        reason="新鮮健康",
                        category="蔬菜",
                        review_count=5
                    ),
                    alternatives=[]
                )
            ]
        )
