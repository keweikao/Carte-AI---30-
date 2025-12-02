# In: schemas/restaurant_profile.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class MenuItemAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(..., description="網友評價摘要，如'肉太柴'")
    mention_count: int = 0

class MenuItem(BaseModel):
    name: str
    price: Optional[int]
    category: str = "其他"
    description: Optional[str] = None
    source_type: Literal["dine_in", "delivery", "estimated", "unknown"] = "unknown"
    is_popular: bool = False
    is_risky: bool = False
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