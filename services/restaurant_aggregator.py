import asyncio
from typing import Optional
import datetime

from schemas.restaurant_profile import RestaurantProfile
from services import firestore_service
from services.menu_scraper import MenuScraper
from services.review_analyzer import ReviewAnalyzer

async def get_restaurant_data(place_id: str, name: str) -> Optional[RestaurantProfile]:
    """
    Orchestrator function to get restaurant data.
    Handles warm start (cache hit) and cold start (data fetching and processing).
    """
    # 1. Warm Start Check
    print(f"--- Aggregator: Checking cache for place_id: {place_id} ---")
    cached_profile = firestore_service.get_restaurant_profile(place_id=place_id)
    if cached_profile:
        return cached_profile

    # 2. Cold Start Logic
    print(f"--- Aggregator: Cache miss. Starting Cold Start for {name} ---")
    
    # Initialize services
    scraper = MenuScraper()
    analyzer = ReviewAnalyzer()

    # --- Ingestion and Processing ---
    
    # Step 1: Get Menu
    menu_url = await scraper.search_menu_url(name)
    menu_items = []
    trust_level = "low"
    
    if menu_url:
        menu_text = await scraper.fetch_and_parse_with_jina(menu_url)
        if menu_text:
            menu_items = await scraper.extract_menu_with_gemini(menu_text)
            trust_level = "high" if menu_items else "low"
    
    # Fallback if text-based scraping fails
    if not menu_items:
        print("Text-based scraping failed or yielded no results. Using Vision API fallback.")
        # NOTE: The Apify call to get image URLs should be integrated here.
        # For now, we continue to use the placeholder Vision fallback.
        menu_items = await scraper.vision_api_fallback(place_id)
        trust_level = "medium"

    if not menu_items:
        print(f"Could not generate a menu for {name}. Aborting.")
        return None

    # Step 2: Get Reviews and Fuse
    reviews_from_apify = await analyzer.fetch_reviews_apify(place_id=place_id, restaurant_name=name)
    
    final_menu_items, review_summary = await analyzer.analyze_and_fuse_reviews(
        reviews=reviews_from_apify,
        menu_items=menu_items
    )

    # Step 3: Create final profile and persist
    new_profile = RestaurantProfile(
        place_id=place_id,
        name=name,
        address="Address placeholder", # This should come from Apify/Serper
        updated_at=datetime.datetime.now(datetime.timezone.utc),
        trust_level=trust_level,
        menu_source_url=menu_url,
        menu_items=final_menu_items,
        review_summary=review_summary
    )

    # Step 4: Save to Firestore
    firestore_service.save_restaurant_profile(new_profile)

    return new_profile
