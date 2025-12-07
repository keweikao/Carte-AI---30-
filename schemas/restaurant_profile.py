# In: schemas/restaurant_profile.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class DishAttributes(BaseModel):
    """AI-generated dish attributes for filtering and ranking"""

    # Hard Filter Attributes (絕對過濾條件)
    is_spicy: bool = False
    is_vegan: bool = False
    contains_beef: bool = False
    contains_pork: bool = False
    contains_seafood: bool = False
    allergens: List[str] = Field(default_factory=list, description="e.g., ['nuts', 'shrimp', 'milk']")

    # Soft Ranking Attributes (排序參考)
    flavors: List[str] = Field(default_factory=list, description="e.g., ['sour', 'garlic_heavy', 'sweet']")
    textures: List[str] = Field(default_factory=list, description="e.g., ['crispy', 'soup', 'chewy']")
    temperature: Literal["hot", "cold", "room"] = "hot"
    cooking_method: str = "unknown"
    suitable_occasions: List[str] = Field(default_factory=list, description="e.g., ['date', 'group_share', 'alcohol_pairing']")

    # Value Attributes (價值標記)
    is_signature: bool = False
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0)
    highlight_review: Optional[str] = None


class MenuItemAnalysis(BaseModel):
    """Legacy structure - will be deprecated in favor of DishAttributes"""
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(..., description="網友評價摘要，如'肉太柴'")
    mention_count: int = 0


class MenuItem(BaseModel):
    id: str = Field(default="", description="Unique dish ID")
    name: str
    price: Optional[int]
    category: str = "其他"
    description: Optional[str] = None
    image_url: Optional[str] = None
    source_type: Literal["dine_in", "delivery", "estimated", "unknown"] = "unknown"
    is_popular: bool = False
    is_risky: bool = False

    # New: AI-generated attributes
    analysis: Optional[DishAttributes] = None

    # Legacy: Keep for backward compatibility
    ai_insight: Optional[MenuItemAnalysis] = None

class RestaurantProfile(BaseModel):
    place_id: str
    name: str
    address: str
    updated_at: datetime
    trust_level: Literal["high", "medium", "low"]
    menu_source_url: Optional[str]
    menu_items: List[MenuItem]
    review_summary: str # 整體評價摘要