from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
import datetime

# Import the new, updated schema
from schemas.restaurant_profile import RestaurantProfile
from services import restaurant_aggregator # Import the new aggregator service

router = APIRouter()

@router.get("/restaurant/{place_id}", response_model=RestaurantProfile)
async def get_restaurant_details_by_id(place_id: str, name: str = Query(..., description="The name of the restaurant, required for cold start search.")):
    """
    This is the main endpoint to get a restaurant's complete profile.
    It orchestrates the warm/cold start logic via the aggregator service.
    """
    print(f"Received request for place_id: {place_id}, name: {name}")
    
    profile = await restaurant_aggregator.get_restaurant_data(place_id=place_id, name=name)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Restaurant profile not found or could not be generated.")
        
    return profile
