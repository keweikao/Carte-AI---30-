from pydantic import BaseModel, Field
from typing import List, Optional

class FeedbackRequest(BaseModel):
    recommendation_id: str = Field(..., description="ID of the recommendation being rated")
    selected_items: List[str] = Field(..., description="List of item IDs that the user actually selected")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, description="Optional feedback comment")
