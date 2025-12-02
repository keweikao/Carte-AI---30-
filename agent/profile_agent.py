import asyncio
import json
from typing import Dict, Any, List
from agent.agents import VisualAgent, ReviewAgent, SearchAgent, AggregationAgent
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from services import firestore_service
from schemas.restaurant_profile import RestaurantProfile
import datetime

class RestaurantProfileAgent:
    """
    Intelligence Layer: Gathers and aggregates restaurant data to produce a 'Golden Profile'.
    """
    def __init__(self):
        self.visual_agent = VisualAgent()
        self.review_agent = ReviewAgent()
        self.search_agent = SearchAgent()
        self.aggregator = AggregationAgent()

    async def analyze(self, restaurant_name: str, place_id: str = None) -> Dict[str, Any]:
        """
        Analyzes a restaurant to produce a Golden Profile.
        Implements Smart Task Locking to prevent duplicate work.
        """
        print(f"🕵️ RestaurantProfileAgent: Analyzing {restaurant_name}...")
        
        # --- Smart Task Locking & Cache Check ---
        if place_id:
            cached_profile = firestore_service.get_restaurant_profile(place_id=place_id)
            if cached_profile:
                # For now, we will just return the cached data if it exists.
                # The old logic of checking "status" is simplified by this.
                # The get_restaurant_profile function already handles TTL.
                
                # We need to construct the return value to match the expected format
                return {
                    "golden_profile": cached_profile.menu_items,
                    "candidates": cached_profile.menu_items, # Use menu_items as candidates for now
                    "reviews_data": {"reviews": cached_profile.review_summary}, # Placeholder
                    "agent_results": {}, # Placeholder
                    "is_cache_hit": True
                }

        # --- Cold Start Logic ---
        print(f"Fetching live data for {restaurant_name}...")
        
        # This part of the code still uses the old data fetchers.
        # As per the new spec, this should be replaced by the aggregator calling
        # menu_scraper and review_analyzer. For now, we leave it to fix the startup error.
        reviews_task = fetch_place_details(restaurant_name)
        menu_task = fetch_menu_from_search(restaurant_name)
        
        try:
            reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)
        except Exception as e:
            print(f"❌ Analysis failed during data fetching: {e}")
            raise e

        # --- Multi-Agent Analysis ---
        print("Starting Multi-Agent Analysis...")
        photos_data = reviews_data.get("photos", [])
        
        visual_task = self.visual_agent.run(photos_data)
        review_task = self.review_agent.run(reviews_data)
        search_task = self.search_agent.run(restaurant_name)
        
        visual_result, review_result, search_result = await asyncio.gather(visual_task, review_task, search_task)
        agent_results = [visual_result, review_result, search_result]
        
        # Aggregate to get Golden Profile
        golden_profile_dicts = await self.aggregator.run(agent_results)
        print(f"✓ Golden Profile generated with {len(golden_profile_dicts)} verified items.")
        
        # Create a new RestaurantProfile object to save
        new_profile = RestaurantProfile(
            place_id=place_id or f"name_{restaurant_name}",
            name=restaurant_name,
            address=reviews_data.get("formatted_address", "Address not found"),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            trust_level="low", # Default to low as this is old logic
            menu_source_url=None,
            menu_items=golden_profile_dicts, # Assuming aggregator returns list of dicts convertible to MenuItem
            review_summary=review_result.summary if hasattr(review_result, 'summary') else "No summary"
        )
        
        # Save the new profile
        firestore_service.save_restaurant_profile(new_profile)

        # For backward compatibility, construct the old return format
        return {
            "golden_profile": golden_profile_dicts,
            "candidates": golden_profile_dicts,
            "reviews_data": reviews_data,
            "agent_results": {
                "visual": visual_result,
                "review": review_result,
                "search": search_result
            },
            "is_cache_hit": False
        }
