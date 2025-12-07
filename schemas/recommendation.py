from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

# ----- V1 Schemas (Deprecated) -----

class RecommendationRequest(BaseModel):
    """
    DEPRECATED: This will be replaced by UserInputV2 for a more structured input.
    """
    restaurant_name: str = Field(..., description="Name of the restaurant")
    mode: Literal["sharing", "individual"] = Field(..., description="Dining mode: sharing or individual")
    people: int = Field(..., gt=0, description="Number of people")
    budget: str = Field(..., description="Budget description, e.g., '500-1000 TWD' or 'unlimited'")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions, e.g., 'no beef'")
    user_id: Optional[str] = Field(None, description="User ID for personalization")

class RecommendationItem(BaseModel):
    """
    DEPRECATED: This will be replaced by MenuItemV2.
    """
    id: Optional[str] = Field(None, description="Unique identifier for the item")
    name: str = Field(..., description="Name of the dish")
    price: int = Field(..., description="Price of the dish")
    reason: str = Field(..., description="Reason for recommending this dish (e.g. '45 reviews mentioned...')")
    type: str = Field("Dish", description="Type/Category (e.g. Appetizer, Main, Drink)")
    is_signature: bool = Field(False, description="Is this a signature/popular dish?")
    alternatives: List['RecommendationItem'] = Field(default_factory=list, description="Alternative option for swapping")

class FullRecommendationResponse(BaseModel):
    """
    DEPRECATED: This will be replaced by RecommendationResponseV2.
    """
    recommendation_id: str = Field(..., description="Unique ID for this recommendation session")
    restaurant_name: str
    total_estimated_price: int = Field(..., description="Total estimated price")
    currency: str = Field("TWD", description="Currency")
    summary: str = Field(..., description="Summary of the recommendation")
    recommendations: List[RecommendationItem] = Field(..., description="List of recommended items")
    user_info: Optional[dict] = Field(None, description="User info if logged in")


# ----- V2 Schemas (New and Improved) -----

class BudgetV2(BaseModel):
    type: Literal["Per_Person", "Total"] = Field(..., description="Budget type")
    amount: int = Field(..., description="Budget amount")

class UserInputV2(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant")
    place_id: Optional[str] = Field(None, description="Google Maps Place ID for precise restaurant identification")
    dining_style: Literal["Shared", "Individual"] = Field(..., description="Dining style")
    party_size: int = Field(..., gt=0, description="Number of people")
    budget: Optional[BudgetV2] = None
    dish_count_target: Optional[int] = Field(None, description="Target number of dishes, null if AI should decide")
    preferences: List[str] = Field(default_factory=list, description="List of preference tags (e.g., 'No_Beef', 'Spicy')")
    natural_input: Optional[str] = Field(None, description="User's free-text supplementary description")
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    occasion: Optional[Literal["friends", "family", "date", "business", "fitness", "all_signatures"]] = Field(
        None, 
        description="Dining occasion: friends (聚餐), family (家庭), date (約會), business (商務), fitness (健身減脂), all_signatures (招牌全制霸)"
    )
    language: str = Field("zh-TW", description="User's preferred language (e.g., 'zh-TW', 'en-US', 'ja-JP')")

class MenuItemV2(BaseModel):
    dish_id: Optional[str] = Field(None, description="Corresponding menu item ID")
    dish_name: str = Field(..., description="Name of the dish (User's preferred language)")
    dish_name_local: Optional[str] = Field(None, description="Name of the dish in the restaurant's local language (e.g., Japanese)")
    price: int = Field(..., description="Price of the dish")
    quantity: int = Field(..., description="Quantity of this dish to order", ge=1)
    reason: str = Field(..., description="Reason for recommending this dish")
    category: str = Field(..., description="Dish category (e.g., 冷菜, 熱菜, 刺身, 壽司)")
    review_count: Optional[int] = Field(None, description="Number of reviews mentioning this dish")

class DishSlotResponse(BaseModel):
    category: str = Field(..., description="Category of the dish slot")
    display: MenuItemV2 = Field(..., description="The dish displayed to the user")
    alternatives: List[MenuItemV2] = Field(..., description="Alternative dishes for swapping")

class RecommendationResponseV2(BaseModel):
    recommendation_summary: str = Field(..., description="A warm, professional opening explaining the recommendation")
    items: List[DishSlotResponse]
    total_price: int = Field(..., description="Total estimated price of the recommended items")
    nutritional_balance_note: Optional[str] = Field(None, description="A brief note on the nutritional or flavor balance")
    # Adding fields from V1 for partial compatibility if needed
    recommendation_id: str = Field(..., description="Unique ID for this recommendation session")
    restaurant_name: str
    user_info: Optional[dict] = Field(None, description="User info if logged in")

    # NEW: Dynamic category system
    cuisine_type: str = Field(..., description="Restaurant cuisine type (中式餐館, 日本料理, 美式餐廳, 義式料理, 泰式料理)")
    category_summary: Dict[str, int] = Field(..., description="Count of dishes per category (e.g., {'冷菜': 1, '熱菜': 2})")
    currency: str = Field("TWD", description="Currency code (e.g., TWD, JPY, USD)")

class AddOnRequest(BaseModel):
    category: str = Field(..., description="Requested category for the add-on")
    count: int = Field(1, description="Number of dishes to add", ge=1)

class AddOnResponse(BaseModel):
    new_dishes: List[MenuItemV2] = Field(..., description="List of newly recommended dishes")
