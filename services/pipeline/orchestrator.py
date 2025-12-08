"""
Orchestration Layer - Restaurant data pipeline coordinator
Controls flow, handles fallbacks, and assembles final restaurant profile
"""

import asyncio
from datetime import datetime, timezone
from typing import Optional, Union, List, Callable

from schemas.restaurant_profile import RestaurantProfile, MenuItem
from schemas.pipeline import ParsedMenuItem, PipelineInput
from .providers import UnifiedMapProvider, WebSearchProvider
from .intelligence import MenuParser, InsightEngine, MenuIntelligence


class RestaurantPipeline:
    """
    Main pipeline orchestrator for restaurant data processing
    Coordinates data acquisition, parsing, and fusion
    """

    def __init__(self):
        self.map_provider = UnifiedMapProvider()
        self.web_provider = WebSearchProvider()
        self.menu_parser = MenuParser()
        self.insight_engine = InsightEngine()
        self.menu_intelligence = MenuIntelligence()

    async def process(
        self, 
        input_data: Union[str, PipelineInput],
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Optional[RestaurantProfile]:
        """
        Process a restaurant through the complete pipeline

        Args:
            input_data: Name of the restaurant or PipelineInput object
            progress_callback: Optional callback function(step: int, message: str) for progress updates

        Returns:
            RestaurantProfile or None if processing fails
        """
        try:
            if isinstance(input_data, str):
                restaurant_name = input_data
                place_id = None
            else:
                restaurant_name = input_data.restaurant_name
                place_id = input_data.place_id

            print(f"\n{'='*60}")
            print(f"[Pipeline] Starting processing for: {restaurant_name} (Place ID: {place_id})")
            print(f"{'='*60}\n")

            # STEP 1: Parallel data acquisition
            print("[Pipeline] STEP 1: Fetching data from external sources...")
            if progress_callback:
                progress_callback(1, "正在搜尋餐廳菜單...")

            map_task = self.map_provider.fetch_map_data(restaurant_name, place_id=place_id)
            web_task = self.web_provider.search_and_fetch(restaurant_name)

            map_data, web_content = await asyncio.gather(
                map_task,
                web_task,
                return_exceptions=True
            )

            # Handle exceptions
            if isinstance(map_data, Exception):
                print(f"[Pipeline] Map provider failed: {map_data}")
                map_data = None

            if isinstance(web_content, Exception):
                print(f"[Pipeline] Web provider failed: {web_content}")
                web_content = None

            # Check if we have at least map data
            if not map_data:
                print(f"[Pipeline] CRITICAL: Failed to fetch map data. Cannot proceed.")
                return None

            print(f"[Pipeline] Data acquisition complete:")
            print(f"  - Map data: ✓ ({len(map_data.images)} images, {len(map_data.reviews)} reviews)")
            print(f"  - Web content: {'✓' if web_content else '✗'}")
            
            if progress_callback:
                progress_callback(2, "正在抓取餐廳評論...")

            # STEP 2: Menu extraction strategy
            print(f"\n[Pipeline] STEP 2: Extracting menu...")
            if progress_callback:
                progress_callback(3, "正在解析菜單內容...")

            menu_items: List[ParsedMenuItem] = []
            trust_level = "low"
            menu_source_url = None

            # Strategy 1: Try text parsing first (highest quality)
            if web_content:
                print("[Pipeline] Strategy 1: Parsing menu from web content...")
                menu_items = await self.menu_parser.parse_from_text(web_content.text_content)
                if menu_items and len(menu_items) >= 3:
                    trust_level = "high"
                    menu_source_url = web_content.source_url
                    print(f"[Pipeline] ✓ Text parsing successful ({len(menu_items)} items)")
                else:
                    print(f"[Pipeline] ✗ Text parsing yielded insufficient items ({len(menu_items)} items)")
                    menu_items = []

            # Strategy 2: Extract dishes from reviews (high quality + low cost)
            if not menu_items:
                print("[Pipeline] Strategy 2: Extracting dishes from reviews...")
                menu_items = await self.menu_parser.extract_from_reviews(
                    reviews=map_data.reviews,
                    restaurant_name=restaurant_name
                )
                if menu_items and len(menu_items) >= 3:
                    trust_level = "medium"
                    print(f"[Pipeline] ✓ Review extraction successful ({len(menu_items)} items)")
                else:
                    print(f"[Pipeline] ✗ Review extraction yielded insufficient items ({len(menu_items)} items)")
                    menu_items = []

            # Last resort: create minimal fallback
            if not menu_items:
                print("[Pipeline] All strategies failed. Creating minimal fallback...")
                menu_items = [
                    ParsedMenuItem(
                        name="招牌菜",
                        price=None,
                        category="推薦",
                        description="根據評論，這是餐廳的招牌菜色"
                    )
                ]
                trust_level = "low"

            print(f"[Pipeline] Menu extraction complete: {len(menu_items)} items (trust: {trust_level})")

            # STEP 3: Review fusion
            print(f"\n[Pipeline] STEP 3: Fusing reviews with menu...")
            if progress_callback:
                progress_callback(4, "正在融合評論與菜單...")

            enhanced_menu, review_summary = await self.insight_engine.fuse_reviews(
                menu_items=menu_items,
                reviews=map_data.reviews
            )

            print(f"[Pipeline] ✓ Review fusion complete")

            # STEP 3.5: Generate DishAttributes for recommendation system
            print(f"\n[Pipeline] STEP 3.5: Generating dish attributes for recommendations...")

            final_menu = await self.menu_intelligence.analyze_dish_batch(
                menu_items=enhanced_menu,
                reviews=map_data.reviews
            )

            items_with_analysis = sum(1 for item in final_menu if item.analysis)
            print(f"[Pipeline] ✓ Dish attributes generated for {items_with_analysis}/{len(final_menu)} items")

            # STEP 4: Assemble final profile
            print(f"\n[Pipeline] STEP 4: Assembling restaurant profile...")

            profile = RestaurantProfile(
                place_id=map_data.place_id,
                name=map_data.name,
                address=map_data.address,
                updated_at=datetime.now(timezone.utc),
                trust_level=trust_level,
                menu_source_url=menu_source_url,
                menu_items=final_menu,  # Use final_menu with DishAttributes
                review_summary=review_summary
            )

            print(f"\n{'='*60}")
            print(f"[Pipeline] ✓ Processing complete for: {restaurant_name}")
            print(f"  - Place ID: {profile.place_id}")
            print(f"  - Menu items: {len(profile.menu_items)}")
            print(f"  - Trust level: {profile.trust_level}")
            print(f"{'='*60}\n")

            return profile

        except Exception as e:
            print(f"[Pipeline] CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None


async def test_pipeline():
    """Test function for local development"""
    pipeline = RestaurantPipeline()

    # Test with a known restaurant
    test_restaurant = "四平小館"

    profile = await pipeline.process(test_restaurant)

    if profile:
        print(f"\n=== FINAL RESULT ===")
        print(f"Name: {profile.name}")
        print(f"Address: {profile.address}")
        print(f"Trust Level: {profile.trust_level}")
        print(f"Menu Items: {len(profile.menu_items)}")
        print(f"\nFirst 3 items:")
        for item in profile.menu_items[:3]:
            print(f"  - {item.name}: ${item.price} ({item.category})")
            if item.ai_insight:
                print(f"    Sentiment: {item.ai_insight.sentiment}, Mentions: {item.ai_insight.mention_count}")


if __name__ == "__main__":
    # For local testing
    asyncio.run(test_pipeline())
