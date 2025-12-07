import os
import json
import asyncio
import uuid
from collections import defaultdict
import google.generativeai as genai
from dotenv import load_dotenv
from schemas.recommendation import UserInputV2, RecommendationResponseV2, MenuItemV2, DishSlotResponse, RecommendationRequest, FullRecommendationResponse
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search, fetch_place_photo
from agent.prompt_builder import create_prompt_for_gemini_v2


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class DiningAgent:
    def __init__(self):
        from agent.profile_agent import RestaurantProfileAgent
        from agent.recommendation_agents import OrchestratorAgent
        
        self.profiler = RestaurantProfileAgent()
        self.orchestrator = OrchestratorAgent()
        # We might need a model for fallback or small tasks, but the sub-agents handle most LLM calls.
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.is_cache_hit = False

    async def get_recommendations_v2(self, request: UserInputV2) -> RecommendationResponseV2:
        """Orchestrates the V2 recommendation process using the new Multi-Agent Architecture."""
        if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
            print(f"CRITICAL ERROR: GEMINI_API_KEY is missing or invalid.")
            raise ValueError("Gemini API Key is not configured.")

        print(f"🚀 Starting Recommendation Process for {request.restaurant_name}...")

        # 1. Intelligence Layer: Get Restaurant Profile
        # This runs Visual, Review, Search, and Aggregation agents
        profile_data = await self.profiler.analyze(request.restaurant_name, request.place_id)
        
        # Check cache status
        self.is_cache_hit = profile_data.get("is_cache_hit", False)
        
        golden_profile = profile_data["golden_profile"]
        candidates = profile_data["candidates"]
        reviews_data = profile_data["reviews_data"]
        
        # 2. User Profiling & Activity Logging (Temporarily disabled for MVP focus)
        user_profile = {}
        # if request.user_id:
        #     try:
        #         user_profile = get_user_profile(request.user_id)
        #         save_user_activity(request.user_id, "search", {
        #             "restaurant_name": request.restaurant_name,
        #             "place_id": request.place_id,
        #             "dining_style": request.dining_style,
        #             "party_size": request.party_size,
        #             "budget": request.budget.model_dump(),
        #             "occasion": request.occasion,
        #             "preferences": request.preferences
        #         })
        #     except Exception as e:
        #         print(f"Warning: Failed to get user profile or save activity. Error: {e}")
        
        # 3. Strategy Layer: Generate Menu
        # This runs DishSelector, BudgetOptimizer, BalanceChecker, QA agents
        final_menu_dicts = await self.orchestrator.run(request, candidates, golden_profile)
        
        # 4. Format Response (Convert Dicts to Schemas)
        final_menu_items = []
        for item_data in final_menu_dicts:
            try:
                # Data cleaning and validation
                if "quantity" not in item_data: item_data["quantity"] = 1
                
                # Handle price
                price = item_data.get("price") or 0
                if isinstance(price, str):
                    import re
                    nums = re.findall(r'\d+', price)
                    price = int(nums[0]) if nums else 0
                item_data["price"] = price
                
                # Handle category
                if "category" not in item_data: item_data["category"] = "其他"

                menu_item = MenuItemV2.model_validate(item_data)
                final_menu_items.append(menu_item)
            except Exception as e:
                print(f"Skipping invalid item from Orchestrator: {item_data}. Error: {e}")

        # 5. Build Dish Slots (with Alternatives)
        dish_slots = []
        for item in final_menu_items:
            # Simple strategy: Find other items in the same category from the candidate pool
            alts = []
            for cand in candidates:
                # Skip if same name
                if cand.get("dish_name") == item.dish_name:
                    continue
                # Match category
                cand_cat = cand.get("category", "其他")
                if cand_cat == item.category:
                    try:
                        # Clean candidate data
                        cand_copy = cand.copy()
                        if "quantity" not in cand_copy: cand_copy["quantity"] = 1
                        c_price = cand_copy.get("price") or 0
                        if isinstance(c_price, str):
                            import re
                            nums = re.findall(r'\d+', c_price)
                            c_price = int(nums[0]) if nums else 0
                        cand_copy["price"] = c_price
                        if "category" not in cand_copy: cand_copy["category"] = "其他"
                        
                        alts.append(MenuItemV2.model_validate(cand_copy))
                    except:
                        pass
            
            # Sort alternatives by confidence or something?
            # For now just take top 2
            dish_slots.append(DishSlotResponse(
                category=item.category,
                display=item,
                alternatives=alts[:2]
            ))

        # 6. Final Calculations
        total_price = sum((item.price or 0) * item.quantity for item in final_menu_items)
        
        category_summary = defaultdict(int)
        for item in final_menu_items:
            category_summary[item.category] += 1
            
        cuisine_type = "中式餐館" # Default, or extract from reviews/search
        if "types" in reviews_data:
             # simple heuristic
             cuisine_type = reviews_data["types"][0] if reviews_data["types"] else "中式餐館"

        # 7. Construct Response
        recommendation_id = str(uuid.uuid4())
        response_data = {
            "recommendation_summary": f"為您從 {request.restaurant_name} 精心挑選了 {len(final_menu_items)} 道佳餚。",
            "items": dish_slots,
            "total_price": total_price,
            "nutritional_balance_note": "由 AI 智慧主廚為您精心調配的均衡菜單。",
            "recommendation_id": recommendation_id,
            "restaurant_name": request.restaurant_name,
            "user_info": {}, # Temporarily disabled
            "cuisine_type": cuisine_type,
            "category_summary": dict(category_summary),
            "currency": "TWD", # Default for now
        }

        # 8. Background Tasks (Memory & Cache)
        # Save candidates for alternatives/add-ons (Temporarily disabled)
        # try:
        #     asyncio.create_task(asyncio.to_thread(save_recommendation_candidates, recommendation_id, candidates, cuisine_type))
        # except Exception as e:
        #     print(f"Warning: Failed to save candidates. Error: {e}")

        # Update Memory (Temporarily disabled)
        # user_id = getattr(request, 'user_id', None)
        # if user_id:
        #     try:
        #         from agent.memory_agent import MemoryAgent
        #         memory_agent = MemoryAgent()
        #         asyncio.create_task(memory_agent.update_dining_patterns(
        #             user_id=user_id,
        #             party_size=request.party_size,
        #             dining_style=request.dining_style,
        #             occasion=request.occasion or 'casual'
        #         ))
        #     except Exception as e:
        #         print(f"Warning: Failed to update memory. Error: {e}")

        print(f"✓ Recommendation Process Complete. ID: {recommendation_id}")
        return RecommendationResponseV2.model_validate(response_data)

    # --- Deprecated V1 Method ---
    async def get_recommendations(self, request: RecommendationRequest) -> FullRecommendationResponse:
        """DEPRECATED: Orchestrates the original recommendation process."""
        raise NotImplementedError("This V1 method is deprecated. Please use get_recommendations_v2.")
