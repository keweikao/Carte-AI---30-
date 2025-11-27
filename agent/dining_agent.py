import os
import json
import asyncio
import uuid
from collections import defaultdict
import google.generativeai as genai
from dotenv import load_dotenv
from schemas.recommendation import UserInputV2, RecommendationResponseV2, MenuItemV2, DishSlotResponse, RecommendationRequest, FullRecommendationResponse
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from agent.prompt_builder import create_prompt_for_gemini_v2
from services.firestore_service import get_cached_data, save_restaurant_data, get_user_profile, save_recommendation_candidates

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class DiningAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def get_recommendations_v2(self, request: UserInputV2) -> RecommendationResponseV2:
        """Orchestrates the V2 recommendation process, creating a candidate pool and forming DishSlots."""
        if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
            print(f"CRITICAL ERROR: GEMINI_API_KEY is missing or invalid. Current value: {GEMINI_API_KEY[:5]}..." if GEMINI_API_KEY else "None")
            raise ValueError("Gemini API Key is not configured.")

        # 1. Fetch Data (Cache or Live)
        cached_data = None
        try:
            cached_data = get_cached_data(request.restaurant_name)
        except Exception as e:
            print(f"Warning: Firestore cache read failed. Proceeding without cache. Error: {e}")

        if cached_data:
            reviews_data, menu_text = cached_data.get("reviews_data", {}), cached_data.get("menu_text", "")
            print("Using cached data.")
        else:
            print("Fetching live data...")
            reviews_task = fetch_place_details(request.restaurant_name)
            menu_task = fetch_menu_from_search(request.restaurant_name)
            reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)
            try:
                save_restaurant_data(request.restaurant_name, reviews_data, menu_text)
            except Exception as e:
                print(f"Warning: Firestore cache write failed. Error: {e}")
        
        reviews_json = json.dumps(reviews_data, ensure_ascii=False)
        menu_json = json.dumps({"menu": menu_text}, ensure_ascii=False)

        # 2. Get User Profile
        user_profile = {}
        if request.user_id:
            try:
                user_profile = get_user_profile(request.user_id)
            except Exception as e:
                print(f"Warning: Failed to get user profile. Proceeding without it. Error: {e}")
        
        # 3. Build V2 Prompt for a large candidate pool
        prompt = create_prompt_for_gemini_v2(request, menu_json, reviews_json, user_profile)
        print(f"Generated V2 Prompt (First 200 chars): {prompt[:200]}...")
        
        # 4. Call Gemini to get the candidate pool
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                print(f"Calling Gemini (Attempt {attempt + 1})...")
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                
                response_text = response.text.strip().removeprefix("```json").removesuffix("```")
                llm_output = json.loads(response_text)
                raw_menu_items = llm_output.get("menu_items", [])
                cuisine_type = llm_output.get("cuisine_type", "中式餐館")

                # --- New Logic: Process raw items into DishSlots ---
                dish_slots, final_menu_items = self._process_llm_candidates(raw_menu_items, request)

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
                }
                
                # --- New: Save the full candidate pool for future 'alternatives' requests ---
                try:
                    # We need the recommendation_id from the response_data
                    recommendation_id = response_data["recommendation_id"]
                    save_recommendation_candidates(recommendation_id, raw_menu_items, cuisine_type)
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

    def _process_llm_candidates(self, raw_items: list, request: UserInputV2) -> (list[DishSlotResponse], list[MenuItemV2]):
        """Helper to process a raw list of menu items into dish slots."""
        
        # 1. Group items by category
        items_by_category = defaultdict(list)
        for item_data in raw_items:
            try:
                item = MenuItemV2.model_validate(item_data)
                items_by_category[item.category].append(item)
            except Exception as e:
                print(f"Skipping invalid item data: {item_data}. Error: {e}")

        # 2. Determine target dish count
        if request.dish_count_target:
            target_count = request.dish_count_target
        else:
            target_count = request.party_size + 1 if request.dining_style == "Shared" else request.party_size

        # 3. Build Dish Slots (simple greedy selection)
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
        
        # This loop creates one slot per available category until the target count is reached
        while len(final_menu_items) < target_count and any(items_by_category.values()):
            for category in sorted_categories:
                if len(final_menu_items) >= target_count:
                    break
                
                if items_by_category[category]:
                    display_dish = items_by_category[category].pop(0)
                    alternatives = items_by_category[category][:2] # Take up to 2 alternatives
                    
                    dish_slots.append(DishSlotResponse(
                        category=category,
                        display=display_dish,
                        alternatives=alternatives
                    ))
                    final_menu_items.append(display_dish)
        
        return dish_slots, final_menu_items

    # --- Deprecated V1 Method ---
    async def get_recommendations(self, request: RecommendationRequest) -> FullRecommendationResponse:
        """DEPRECATED: Orchestrates the original recommendation process."""
        raise NotImplementedError("This V1 method is deprecated. Please use get_recommendations_v2.")
