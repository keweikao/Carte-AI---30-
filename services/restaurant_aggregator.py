"""
Restaurant Aggregator - Orchestrates the data pipeline
Handles warm start (cache) and cold start (new data fetching)
"""

from typing import Optional

from schemas.restaurant_profile import RestaurantProfile
from services import firestore_service
from services.pipeline import RestaurantPipeline


async def get_restaurant_data(place_id: str, name: str) -> Optional[RestaurantProfile]:
    """
    Main orchestrator function to get restaurant data.
    Handles warm start (cache hit) and cold start (data fetching via new pipeline).

    Args:
        place_id: Google Maps place ID
        name: Restaurant name

    Returns:
        RestaurantProfile or None if processing fails
    """
    # WARM START: Check cache first
    print(f"[Aggregator] Checking cache for place_id: {place_id}")
    cached_profile = firestore_service.get_restaurant_profile(place_id=place_id)

    if cached_profile:
        print(f"[Aggregator] ✓ Cache hit for {name}")
        return cached_profile

    # COLD START: Use new pipeline
    print(f"[Aggregator] Cache miss. Starting cold start for: {name}")

    try:
        # Initialize new pipeline
        pipeline = RestaurantPipeline()

        # Process restaurant through pipeline
        profile = await pipeline.process(restaurant_name=name)

        if not profile:
            print(f"[Aggregator] Pipeline failed to generate profile for {name}")
            return None

        # Update place_id if pipeline found different one
        if profile.place_id and profile.place_id != place_id:
            print(f"[Aggregator] Place ID mismatch: {place_id} -> {profile.place_id}")
            # Use the pipeline's place_id (more accurate from Apify)
        else:
            # Ensure place_id is set
            profile.place_id = place_id

        # Save to Firestore
        print(f"[Aggregator] Saving profile to Firestore...")
        firestore_service.save_restaurant_profile(profile)

        print(f"[Aggregator] ✓ Cold start complete for {name}")
        return profile

    except Exception as e:
        print(f"[Aggregator] ERROR: Failed to process {name}: {e}")
        import traceback
        traceback.print_exc()
        return None
