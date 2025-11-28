import asyncio
import json
from typing import Dict, Any, List
from agent.agents import VisualAgent, ReviewAgent, SearchAgent, AggregationAgent
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from services.firestore_service import get_cached_data, save_restaurant_data

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
        """
        print(f"🕵️ RestaurantProfileAgent: Analyzing {restaurant_name}...")
        
        # 1. Check Cache
        cached_data = None
        try:
            cached_data = get_cached_data(place_id=place_id, restaurant_name=restaurant_name)
        except Exception as e:
            print(f"Warning: Firestore cache read failed. Error: {e}")

        reviews_data = {}
        menu_text = ""

        if cached_data:
            print(f"✓ Using cached data for {restaurant_name}")
            reviews_data = cached_data.get("reviews_data", {})
            menu_text = cached_data.get("menu_text", "")
        else:
            print(f"Fetching live data for {restaurant_name}...")
            
            reviews_task = fetch_place_details(restaurant_name)
            menu_task = fetch_menu_from_search(restaurant_name)
            
            reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)
            
            # Save to cache
            try:
                save_restaurant_data(
                    place_id=place_id,
                    restaurant_name=restaurant_name,
                    reviews_data=reviews_data,
                    menu_text=menu_text
                )
            except Exception as e:
                print(f"Warning: Firestore cache write failed. Error: {e}")

        # --- Multi-Agent Analysis ---
        print("Starting Multi-Agent Analysis...")
        photos_data = reviews_data.get("photos", [])
        
        # Run agents in parallel
        visual_task = self.visual_agent.run(photos_data)
        review_task = self.review_agent.run(reviews_data)
        search_task = self.search_agent.run(restaurant_name)
        
        visual_result, review_result, search_result = await asyncio.gather(visual_task, review_task, search_task)
        agent_results = [visual_result, review_result, search_result]
        
        # Aggregate to get Golden Profile
        golden_profile = await self.aggregator.run(agent_results)
        print(f"✓ Golden Profile generated with {len(golden_profile)} verified items.")
        
        # Combine candidates from Visual and Search for the "Pool"
        # Visual data is usually high quality (OCR)
        # Search data is good for signatures
        candidates = []
        if visual_result.data:
            candidates.extend(visual_result.data)
        if search_result.data:
            # Avoid duplicates if possible, or just dump them in
            candidates.extend(search_result.data)
            
        # If we have no candidates, use the golden profile as candidates
        if not candidates:
            candidates = golden_profile
            
        return {
            "golden_profile": golden_profile,
            "candidates": candidates,
            "reviews_data": reviews_data,
            "agent_results": {
                "visual": visual_result,
                "review": review_result,
                "search": search_result
            }
        }
