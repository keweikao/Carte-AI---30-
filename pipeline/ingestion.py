import os
import asyncio
import json
from apify_client import ApifyClientAsync
from apify_client.errors import ApifyClientError
from dotenv import load_dotenv

load_dotenv()

async def call_apify_scraper(place_id: str) -> dict:
    """
    Calls the Apify Google Maps Scraper to fetch restaurant data for a specific place_id.
    """
    apify_api_token = os.getenv("APIFY_API_TOKEN")
    if not apify_api_token:
        print("Error: APIFY_API_TOKEN is not set in environment variables.")
        return {}

    client = ApifyClientAsync(apify_api_token)
    ACTOR_ID = "compass~crawler-google-places"

    run_input = {
        "startUrls": [{"url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"}],
        "maxImages": 10,  # Increased to 10 for better menu detection
        "maxReviews": 10, # Increased to 10 for staging test
        "language": "zh-TW",
        "scrapePlaceDetailPage": True,
        "proxyConfiguration": {"useApifyProxy": True},
    }

    print(f"Calling Apify Google Maps Scraper for place_id: {place_id}...")

    try:
        run = await client.actor(ACTOR_ID).call(run_input=run_input)
        
        list_items = []
        async for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            list_items.append(item)
        
        if list_items:
            restaurant_data = list_items[0]
            
            image_urls = restaurant_data.get("imageUrls") or []
            reviews_data = restaurant_data.get("reviews") or []
            
            print(f"Successfully fetched {len(image_urls)} images and {len(reviews_data)} reviews for {place_id}.")
            return {
                "restaurant_name": restaurant_data.get("title"),
                "address": restaurant_data.get("address"),
                "place_id": restaurant_data.get("placeId"),
                "images": image_urls,
                "reviews": reviews_data
            }
        else:
            print(f"No data found by Apify scraper for {place_id}.")
            return {}

    except ApifyClientError as e:
        print(f"Apify Client Error calling scraper for {place_id}: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while calling Apify scraper for {place_id}: {e}")
        return {}

if __name__ == "__main__":
    # Example usage for testing
    async def test_scraper():
        test_place_id = "ChIJ-x-t9W_eQjQRhFjU2g08sHk" # Example: 鼎泰豐信義店
        
        if not os.getenv("APIFY_API_TOKEN"):
            print("Please set APIFY_API_TOKEN in your .env file to run this test.")
            return

        print(f"Running test for place_id '{test_place_id}'...")
        data = await call_apify_scraper(test_place_id)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        if data:
            print(f"Test successful: Fetched data for {data.get('restaurant_name')}")
        else:
            print("Test failed: No data fetched.")

    asyncio.run(test_scraper())
