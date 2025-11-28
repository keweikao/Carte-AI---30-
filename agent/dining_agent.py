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
from services.firestore_service import get_cached_data, save_restaurant_data, get_user_profile, save_recommendation_candidates, save_user_activity

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class DiningAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def get_recommendations_v2(self, request: UserInputV2) -> RecommendationResponseV2:
        """Orchestrates the V2 recommendation process, creating a candidate pool and forming DishSlots."""
        if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
            print(f"CRITICAL ERROR: GEMINI_API_KEY is missing or invalid. Current value: {GEMINI_API_KEY[:5]}..." if GEMINI_API_KEY else "None")
            raise ValueError("Gemini API Key is not configured.")

        # Initialize Agents
        from agent.agents import VisualAgent, ReviewAgent, SearchAgent, AggregationAgent
        visual_agent = VisualAgent()
        review_agent = ReviewAgent()
        search_agent = SearchAgent()
        aggregator = AggregationAgent()
        
        search_task = None

        # 1. Fetch Data (Cache or Live)
        cached_data = None
        try:
            # Prioritize place_id for cache lookup, fallback to restaurant_name
            cached_data = get_cached_data(place_id=request.place_id, restaurant_name=request.restaurant_name)
        except Exception as e:
            print(f"Warning: Firestore cache read failed. Proceeding without cache. Error: {e}")

        if cached_data:
            reviews_data, menu_text = cached_data.get("reviews_data", {}), cached_data.get("menu_text", "")
            print(f"Using cached data for {request.place_id or request.restaurant_name}.")
        else:
            print(f"Fetching live data for {request.place_id or request.restaurant_name}...")
            reviews_task = fetch_place_details(request.restaurant_name)
            menu_task = fetch_menu_from_search(request.restaurant_name)
            
            # Start SearchAgent in parallel
            print("Starting SearchAgent early...")
            search_task = asyncio.create_task(search_agent.run(request.restaurant_name))

            reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)
            try:
                # Save with place_id if available
                save_restaurant_data(
                    place_id=request.place_id,
                    restaurant_name=request.restaurant_name,
                    reviews_data=reviews_data,
                    menu_text=menu_text
                )
            except Exception as e:
                print(f"Warning: Firestore cache write failed. Error: {e}")
        
        reviews_json = json.dumps(reviews_data, ensure_ascii=False)
        menu_json = json.dumps({"menu": menu_text}, ensure_ascii=False)

        # 2. Get User Profile
        user_profile = {}
        if request.user_id:
            try:
                user_profile = get_user_profile(request.user_id)
                # Record search activity
                save_user_activity(request.user_id, "search", {
                    "restaurant_name": request.restaurant_name,
                    "place_id": request.place_id,
                    "dining_style": request.dining_style,
                    "party_size": request.party_size,
                    "budget": request.budget.model_dump(),
                    "occasion": request.occasion,
                    "preferences": request.preferences
                })
            except Exception as e:
                print(f"Warning: Failed to get user profile or save activity. Error: {e}")
        
        # --- Multi-Agent Workflow ---
        visual_result = None
        try:
            print("Starting Multi-Agent Analysis...")
            
            # Prepare inputs for agents
            photos_data = reviews_data.get("photos", [])
            
            # Start remaining agents
            visual_task = visual_agent.run(photos_data)
            review_task = review_agent.run(reviews_data)
            
            # If search_task wasn't started (e.g. cached data), start it now
            if not search_task:
                 search_task = asyncio.create_task(search_agent.run(request.restaurant_name))
            
            # Wait for all
            visual_result, review_result, search_result = await asyncio.gather(visual_task, review_task, search_task)
            agent_results = [visual_result, review_result, search_result]
            
            # Aggregate results
            high_confidence_candidates = await aggregator.run(agent_results)
            print(f"Multi-Agent Analysis Complete. Found {len(high_confidence_candidates)} high-confidence items.")
            
            # Inject candidates into user_profile for the prompt
            user_profile["high_confidence_candidates"] = high_confidence_candidates
            
        except Exception as e:
            print(f"CRITICAL ERROR in Multi-Agent Workflow: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: Proceed without high_confidence_candidates
            user_profile["high_confidence_candidates"] = []

        # Inject restaurant types into user_profile for prompt context
        if "types" in reviews_data:
            user_profile["restaurant_types"] = reviews_data["types"]
            
        # 3. Build V2 Prompt (now with Agent insights)
        prompt = create_prompt_for_gemini_v2(request, menu_json, reviews_json, user_profile)
        print(f"Generated V2 Prompt (First 200 chars): {prompt[:200]}...")
        
        # 4. Call Gemini to get the final candidate pool
        # We still pass the top photos to the final Gemini call for "vibe check" and additional context
        # even though VisualAgent has already analyzed them.
        image_parts = []
        # Try to reuse blobs from VisualAgent
        if visual_result and visual_result.metadata and "blobs" in visual_result.metadata:
             print("Reusing image blobs from VisualAgent...")
             image_parts = visual_result.metadata["blobs"][:3]
        elif photos_data:
            # Take top 3 photos (VisualAgent already analyzed top 5, but we pass 3 to the final generator for context)
            top_photos = photos_data[:3]
            photo_tasks = [fetch_place_photo(photo["photo_reference"]) for photo in top_photos]
            photo_blobs = await asyncio.gather(*photo_tasks)
            for blob in photo_blobs:
                if blob:
                    image_parts.append({
                        "mime_type": "image/jpeg",
                        "data": blob
                    })

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                print(f"Calling Gemini (Attempt {attempt + 1})...")
                
                # Combine prompt and images
                content = [prompt] + image_parts
                
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    content,
                    generation_config={"response_mime_type": "application/json"}
                )
                
                response_text = response.text.strip().removeprefix("```json").removesuffix("```")
                llm_output = json.loads(response_text)
                raw_menu_items = llm_output.get("menu_items", [])
                cuisine_type = llm_output.get("cuisine_type", "中式餐館")
                currency = llm_output.get("currency", "TWD")

                # --- New Logic: Process raw items into DishSlots ---
                dish_slots, final_menu_items = self._process_llm_candidates(raw_menu_items, request, currency)

                # 4. Calculate final summary and price
                total_price = sum(item.price for item in final_menu_items)
                category_summary = defaultdict(int)
                for item in final_menu_items:
                    category_summary[item.category] += 1
                
                user_info = user_profile.get("user_info", {})
                
                # 5. Assemble the final response
                response_data = {
                    "recommendation_summary": f"為您從 {request.restaurant_name} 精心挑選了 {len(final_menu_items)} 道佳餚。",
                    "items": dish_slots,
                    "total_price": total_price,
                    "nutritional_balance_note": "菜單組合多樣，兼顧了不同口味與風格。",
                    "recommendation_id": str(uuid.uuid4()),
                    "restaurant_name": request.restaurant_name,
                    "user_info": user_info,
                    "cuisine_type": cuisine_type,
                    "category_summary": dict(category_summary),
                    "currency": currency,
                }

                
                # --- NEW: Update user's dining patterns (Memory System) ---
                user_id = getattr(request, 'user_id', None)
                if user_id:
                    try:
                        from agent.memory_agent import MemoryAgent
                        memory_agent = MemoryAgent()
                        # Run memory update in background
                        asyncio.create_task(memory_agent.update_dining_patterns(
                            user_id=user_id,
                            party_size=request.party_size,
                            dining_style=request.dining_style,
                            occasion=request.occasion or 'casual'
                        ))
                        print(f"  📊 Dining patterns update scheduled for user {user_id}")
                    except Exception as e:
                        print(f"  ⚠️  Could not schedule dining patterns update: {e}")
                
                # --- New: Save the full candidate pool for future 'alternatives' requests ---
                try:
                    # We need the recommendation_id from the response_data
                    recommendation_id = response_data["recommendation_id"]
                    # Run cache save in background (using to_thread since it might be sync)
                    asyncio.create_task(asyncio.to_thread(save_recommendation_candidates, recommendation_id, raw_menu_items, cuisine_type))
                    
                    # Also save recommendation_id to response for frontend to use when submitting feedback
                    response_data["recommendation_id"] = recommendation_id
                    
                except Exception as e:
                    print(f"Warning: Failed to save recommendation candidates to cache. Error: {e}")

                print(f"✓ Successfully processed {len(raw_menu_items)} candidates into {len(dish_slots)} dish slots for {request.restaurant_name}")
                return RecommendationResponseV2.model_validate(response_data)
                
            except Exception as e:
                print(f"Error generating V2 recommendation (Attempt {attempt + 1}): {e}")
                import traceback
                traceback.print_exc()
                if 'response' in locals():
                    try:
                        print(f"Response Text (if any): {response.text}")
                    except:
                        pass
                
                if attempt == max_retries:
                    raise RuntimeError(f"Failed after {max_retries} retries: {e}")
                await asyncio.sleep(1)

    def _process_llm_candidates(self, raw_menu_items: list, request: UserInputV2, currency: str = "TWD") -> (list[DishSlotResponse], list[MenuItemV2]):
        """Helper to process a raw list of menu items into dish slots, respecting budget."""
        
        # 1. Group items by category
        items_by_category = defaultdict(list)
        for item_data in raw_menu_items:
            try:
                item = MenuItemV2.model_validate(item_data)
                items_by_category[item.category].append(item)
            except Exception as e:
                print(f"Skipping invalid item data: {item_data}. Error: {e}")

        # 2. Determine target dish count & Budget
        if request.dish_count_target:
            target_count = request.dish_count_target
        else:
            target_count = request.party_size + 1 if request.dining_style == "Shared" else request.party_size

        # Calculate Budget in Local Currency
        budget_in_twd = request.budget.amount * request.party_size if request.budget.type == "per_person" else request.budget.amount
        exchange_rates = {"JPY": 4.5, "USD": 0.032, "EUR": 0.029, "KRW": 42.0, "TWD": 1.0}
        rate = exchange_rates.get(currency, 1.0)
        target_budget = budget_in_twd * rate
        
        print(f"Budget Target: {target_budget} {currency} (Original: {budget_in_twd} TWD)")

        # 3. Build Dish Slots (Budget-Aware Selection)
        dish_slots = []
        final_menu_items = []
        
        # A more sophisticated category selection logic could be implemented here.
        # Use a predefined order to make recommendations more logical (e.g., mains before staples).
        category_order = [
            # Chinese
            "冷菜", "熱菜", "主食", "點心", "湯品", 
            # Japanese
            "刺身", "壽司", "燒烤", "麵類", "湯物", 
            # American / Italian
            "前菜", "開胃菜", "沙拉", "主餐", "主菜", "義大利麵", "披薩", "配菜", 
            # Thai
            "咖哩", "炒飯麵", "湯類",
            # General
            "甜點", "甜品", "飲料"
        ]
        # Sort available categories based on the predefined order
        sorted_categories = sorted(items_by_category.keys(), key=lambda x: category_order.index(x) if x in category_order else len(category_order))
        
        # Helper to pick a dish
        def pick_dish():
            for category in sorted_categories:
                if items_by_category[category]:
                    display_dish = items_by_category[category].pop(0)
                    alternatives = items_by_category[category][:2] # Take up to 2 alternatives
                    
                    dish_slots.append(DishSlotResponse(
                        category=category,
                        display=display_dish,
                        alternatives=alternatives
                    ))
                    final_menu_items.append(display_dish)
                    return True
            return False

        # Phase 1: Meet Minimum Dish Count
        while len(final_menu_items) < target_count:
            if not pick_dish():
                break
        
        # Phase 2: Budget Expansion (Add more dishes if under budget)
        # Only for Shared style or if explicit budget is high
        current_total = sum(item.price or 0 for item in final_menu_items)
        max_dishes = request.party_size * 2 # Cap to avoid over-ordering
        
        if request.dining_style == "Shared":
            while current_total < target_budget * 0.8 and len(final_menu_items) < max_dishes:
                print(f"  Under budget ({current_total} < {target_budget}). Adding more dishes...")
                if not pick_dish():
                    break
                current_total = sum(item.price or 0 for item in final_menu_items)
        
        return dish_slots, final_menu_items

    # --- Deprecated V1 Method ---
    async def get_recommendations(self, request: RecommendationRequest) -> FullRecommendationResponse:
        """DEPRECATED: Orchestrates the original recommendation process."""
        raise NotImplementedError("This V1 method is deprecated. Please use get_recommendations_v2.")
