"""
Data schemas for the restaurant data pipeline.
These are intermediate data structures used between pipeline layers.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RawReview(BaseModel):
    """A single review from Google Maps"""
    text: Optional[str] = None  # Some reviews may not have text
    rating: int = Field(..., ge=1, le=5)
    published_at: Optional[str] = None
    author_name: Optional[str] = None


class MapData(BaseModel):
    """Unified data from Google Maps via Apify"""
    place_id: str
    name: str
    address: str
    phone: Optional[str] = None
    rating: Optional[float] = None
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    reviews: List[RawReview] = Field(default_factory=list, description="List of reviews")


class WebContent(BaseModel):
    """Content from web scraping (menu URLs)"""
    source_url: str
    text_content: str = Field(..., description="Markdown content from Jina Reader")


class ParsedMenuItem(BaseModel):
    """A menu item parsed from text or images"""
    name: str
    price: Optional[int] = None
    category: str = "其他"
    description: Optional[str] = None


class PipelineInput(BaseModel):
    """Input for the pipeline process"""
    restaurant_name: str
    place_id: Optional[str] = None
