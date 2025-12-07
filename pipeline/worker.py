import asyncio
import datetime
import json
import os
from typing import List, Dict, Any, Optional
from google.cloud import firestore
from dotenv import load_dotenv

load_dotenv() # Load .env file for direct script execution

from pipeline.ingestion import call_apify_scraper
from pipeline.vision import image_filter, menu_extractor_ocr
from pipeline.normalization import normalize_price, normalize_category
from pipeline.analysis import perform_keyword_analysis, dish_tagger

from schemas.restaurant_profile import RestaurantProfile, Meta, ProfileStatus, MenuItem, PrecomputedSetItem, Evidence
from services.firestore_service import db # Assuming db is initialized there

async def run_pipeline(place_id: str):
    """
    Orchestrates the entire data pipeline to create a RestaurantProfile using a place_id.
    """
    print(f"--- Starting Profiler Pipeline for '{place_id}' ---")
    
    doc_ref = db.collection('restaurants').document(place_id)

    try:
        # Step 1: Ingestion - Scrape data from Apify using place_id
        print(f"[{place_id}] Step 1: Ingestion - Calling Apify scraper...")
        scraped_data = await call_apify_scraper(place_id)
        if not scraped_data:
            raise Exception("Apify scraper returned no data.")
        
        # Initialize meta info
        profile_meta = Meta(
            name=scraped_data.get("restaurant_name", f"Unknown ({place_id})"),
            place_id=place_id,
            address=scraped_data.get("address"),
            status=ProfileStatus.PENDING,
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )
        initial_profile = RestaurantProfile(meta=profile_meta)
        doc_ref.set(initial_profile.model_dump(by_alias=True, exclude_unset=True))

        # Step 2: Vision - Filter images and extract menu items
        print(f"[{place_id}] Step 2: Vision - Filtering images and extracting menu...")
        all_image_urls = scraped_data.get("images", [])
        menu_images_with_urls = await image_filter(all_image_urls)
        raw_menu_items = await menu_extractor_ocr(menu_images_with_urls)
        
        # Step 3: Normalization - Clean price and standardize category
        print(f"[{place_id}] Step 3: Normalization - Cleaning data...")
        processed_menu_items: List[MenuItem] = []
        for item in raw_menu_items:
            item.price = await normalize_price(item.price)
            item.standard_category = await normalize_category(item.original_category)
            processed_menu_items.append(item)
            
        # Step 4: Analysis - Tagging dishes based on reviews
        print(f"[{place_id}] Step 4: Analysis - Processing reviews and tagging dishes...")
        reviews_text_list = [r.get("text", "") for r in scraped_data.get("reviews", []) if r.get("text")]
        
        final_menu_items: List[MenuItem] = []
        for item in processed_menu_items:
            relevant_snippets = [snippet for snippet in reviews_text_list if item.name in snippet]
            item.tags.extend(await dish_tagger(item.name, relevant_snippets))
            final_menu_items.append(item)

        # Step 5: Final Profile Assembly and Save to Firestore
        profile_meta.status = ProfileStatus.INDEXED
        profile_meta.last_updated = datetime.datetime.now(datetime.timezone.utc)

        final_profile = RestaurantProfile(
            meta=profile_meta,
            menu_items=final_menu_items,
            precomputed_sets={}
        )

        doc_ref.set(final_profile.model_dump(by_alias=True, exclude_unset=True))
        print(f"--- Profiler Pipeline for {place_id} Completed. Status: INDEXED ---")
        return final_profile

    except Exception as e:
        # Update status to ERROR in Firestore
        error_meta = Meta(
            name=f"Error Profile for {place_id}",
            place_id=place_id,
            status=ProfileStatus.ERROR,
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )
        doc_ref.set({"meta": error_meta.model_dump(by_alias=True, exclude_unset=True)}, merge=True)
        print(f"--- Profiler Pipeline for {place_id} Failed. Status: ERROR ---")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    async def test_worker():
        test_place_id = "ChIJ-x-t9W_eQjQRhFjU2g08sHk" # 鼎泰豐 信義店
        
        if not os.getenv("APIFY_API_TOKEN") or not os.getenv("GEMINI_API_KEY"):
            print("Please set APIFY_API_TOKEN and GEMINI_API_KEY in your .env file to run this test.")
            return

        print(f"Running full pipeline test for place_id '{test_place_id}'...")
        try:
            profile = await run_pipeline(test_place_id)
            print("\n--- Full Pipeline Test Result ---")
            print(profile.model_dump_json(indent=2, exclude_unset=True))
            print("\nTest successful!")
        except Exception as e:
            print(f"\nFull Pipeline Test Failed: {e}")
        finally:
            print(f"\nCleaning up test data for {test_place_id}...")
            db.collection('restaurants').document(test_place_id).delete()
            print("Cleanup complete.")

