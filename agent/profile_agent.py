import asyncio
import json
from typing import Dict, Any, List
from agent.agents import VisualAgent, ReviewAgent, SearchAgent, AggregationAgent
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from services.firestore_service import get_cached_data, save_restaurant_data, db

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
        
        # --- Smart Task Locking Logic ---
        # If we have a place_id, use it as the lock key. Otherwise use name.
        lock_key = place_id if place_id else f"name_{restaurant_name}"
        doc_ref = db.collection("restaurant_profiles").document(lock_key)
        
        # 1. Check Status
        try:
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                status = data.get("status")
                timestamp = data.get("timestamp") # Datetime object from Firestore
                
                # Case A: Completed & Valid (Simple cache check is done later, but this is fast path)
                if status == "completed":
                    print(f"✓ Task already completed for {restaurant_name}")
                    # We still let the code flow to 'get_cached_data' below for consistency,
                    # or we could return data['result'] here if we structured it that way.
                    # For now, let's just proceed to standard cache check.
                    pass
                
                # Case B: Processing (Wait for it)
                elif status == "processing":
                    import datetime
                    # Check if stale (e.g. > 5 mins old)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    # Ensure timestamp is aware
                    if timestamp and timestamp.tzinfo is None:
                        timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
                        
                    if timestamp and (now - timestamp).total_seconds() < 300:
                        print(f"⚡️ Task is processing by another worker. Entering wait mode...")
                        # Poll for up to 60 seconds
                        for _ in range(60):
                            await asyncio.sleep(1)
                            doc = doc_ref.get()
                            if doc.exists and doc.to_dict().get("status") == "completed":
                                print("✓ Waited task completed!")
                                break
                        # After waiting, proceed to standard cache check
                    else:
                        print("⚠️ Processing task is stale. Taking over.")
        except Exception as e:
            print(f"Warning: Lock check failed: {e}")

        # 2. Standard Cache Check (This will hit if Case A or B succeeded)
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
            # Case C: Run Analysis (Set Lock)
            print(f"Fetching live data for {restaurant_name}...")
            
            # Set Processing Flag
            try:
                import datetime
                doc_ref.set({
                    "status": "processing",
                    "timestamp": datetime.datetime.now(datetime.timezone.utc),
                    "restaurant_name": restaurant_name
                }, merge=True)
            except Exception as e:
                print(f"Warning: Failed to set lock: {e}")
            
            reviews_task = fetch_place_details(restaurant_name)
            menu_task = fetch_menu_from_search(restaurant_name)
            
            try:
                reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)
                
                # Save to cache
                save_restaurant_data(
                    place_id=place_id,
                    restaurant_name=restaurant_name,
                    reviews_data=reviews_data,
                    menu_text=menu_text
                )
                
                # Mark as Completed
                doc_ref.set({"status": "completed"}, merge=True)
                
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
                # Clear lock so others can retry
                doc_ref.set({"status": "failed"}, merge=True)
                raise e

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
