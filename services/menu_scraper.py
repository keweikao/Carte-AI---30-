import os
import asyncio
import httpx
import json
from serpapi import GoogleSearch
import google.generativeai as genai
from apify_client import ApifyClientAsync
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any

from schemas.restaurant_profile import MenuItem

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

if not GEMINI_API_KEY or "YOUR_GOOGLE_API_KEY_HERE" in GEMINI_API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY is missing or invalid.")
    GEMINI_API_KEY = None
else:
    print(f"GEMINI_API_KEY loaded: {GEMINI_API_KEY[:5]}... (length: {len(GEMINI_API_KEY)})")

class MenuScraper:
    def __init__(self):
        # API keys are checked at the module level now
        pass

    async def search_menu_url(self, restaurant_name: str) -> Optional[str]:
        if not SERPER_API_KEY:
            print("Warning: SERPER_API_KEY is not set.")
            return None
        print(f"Searching for menu URL for {restaurant_name} using Serper API...")
        try:
            params = {
                "engine": "google",
                "q": f"{restaurant_name} 完整菜單 價格 官方網站 OR uber eats menu", # Refined query
                "api_key": SERPER_API_KEY
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            for result in results.get("organic_results", []):
                title = result.get("title", "").lower()
                link = result.get("link", "").lower()
                # Prioritize links that explicitly mention "menu" and are likely official or delivery
                if ("menu" in title or "menu" in link or "dintaifung" in link) and \
                   ("price" in title or "價格" in title or "uber eats" in link or "ubereats" in link):
                    print(f"Found potential menu URL: {result.get('link')}")
                    return result.get("link")
            # Fallback to any menu link if a specific one with price isn't found
            for result in results.get("organic_results", []):
                link = result.get("link", "").lower()
                if "menu" in link or "dintaifung" in link:
                    print(f"Found fallback menu URL: {result.get('link')}")
                    return result.get("link")
            return None
        except Exception as e:
            print(f"Error searching menu URL with Serper: {e}")
            return None

    async def fetch_and_parse_with_jina(self, url: str) -> Optional[str]:
        if not JINA_API_KEY:
            print("JINA_API_KEY is not set, skipping Jina Reader.")
            return None
        print(f"Fetching content from {url} using Jina Reader...")
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {JINA_API_KEY}"}
                jina_reader_endpoint = f"https://r.jina.ai/{url}"
                response = await client.get(jina_reader_endpoint, headers=headers, timeout=45)
                response.raise_for_status()
                content = response.text
                if content:
                    print(f"Successfully extracted content from {url} via Jina Reader.")
                    return content
                return None
        except Exception as e:
            print(f"Error fetching content with Jina Reader: {e}")
            return None

    async def extract_menu_with_gemini(self, text_content: str) -> List[MenuItem]:
        if not GEMINI_API_KEY:
            print("GEMINI_API_KEY is not set, skipping menu extraction.")
            return []
        print("Extracting menu with Gemini...")
        prompt = f"""
        You are an expert restaurant menu parser. Your goal is to extract individual, specific menu items (dishes) from the provided text, along with their prices and categories. Do NOT list menu sections as items.

        For each individual menu item, provide:
        -   `name`: The exact name of the dish.
        -   `price`: The price as an integer. If a price is clearly stated as a range (e.g., "$100-200") or is unavailable for a dish, set to `null`.
        -   `category`: The category the dish belongs to (e.g., "飯類", "麵點", "湯品"). If not explicitly stated, infer the most suitable category.
        -   `description`: Any brief descriptive text for the dish. Set to `null` if none.
        -   `source_type`: 'dine_in' if it appears to be a standard dine-in menu, 'delivery' if clearly from a delivery platform menu, 'estimated' if price is inferred, 'unknown' otherwise. Prioritize 'dine_in' or 'delivery' if context allows.

        Your output MUST be a valid JSON array of objects, strictly adhering to this Pydantic schema. If no individual menu items can be extracted, return an empty array `[]`.

        Schema for each item:
        ```json
        {{
          "name": "string",
          "price": "integer | null",
          "category": "string",
          "description": "string | null",
          "source_type": "dine_in | delivery | estimated | unknown",
          "is_popular": "boolean" (default false),
          "is_risky": "boolean" (default false),
          "ai_insight": "object | null"
        }}
        ```
        
        Here is the menu text to parse:
        ---
        {text_content}
        ---

        Example of desired output format (if the text content contained "紅燒牛肉麵 $250 招牌麵食", "小籠包 (10顆) $320 經典必點"):
        ```json
        [
          {{
            "name": "紅燒牛肉麵",
            "price": 250,
            "category": "麵點",
            "description": "招牌麵食",
            "source_type": "dine_in",
            "is_popular": false,
            "is_risky": false,
            "ai_insight": null
          }},
          {{
            "name": "小籠包 (10顆)",
            "price": 320,
            "category": "點心",
            "description": "經典必點",
            "source_type": "dine_in",
            "is_popular": false,
            "is_risky": false,
            "ai_insight": null
          }}
        ]
        ```
        """
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = await model.generate_content_async(prompt)
            menu_data_raw = response.text
            if menu_data_raw.startswith("```json"):
                menu_data_raw = menu_data_raw[len("```json"):
].strip()
            if menu_data_raw.endswith("```"):
                menu_data_raw = menu_data_raw[:-len("```")].strip()
            
            menu_items_dicts = json.loads(menu_data_raw)
            parsed_menu_items = [MenuItem(**item) for item in menu_items_dicts]
            print(f"Successfully extracted {len(parsed_menu_items)} menu items with Gemini.")
            return parsed_menu_items
        except Exception as e:
            print(f"An unexpected error occurred during Gemini menu extraction: {e}")
            return []

    async def fetch_restaurant_images(self, place_id: str, restaurant_name: str, max_images: int = 10) -> List[str]:
        """
        Fetches restaurant images from Google Maps using Apify.
        Returns a list of image URLs.
        """
        if not APIFY_API_TOKEN:
            print("Warning: APIFY_API_TOKEN is not set. Cannot fetch images.")
            return []

        print(f"Fetching images for {restaurant_name} (place_id: {place_id}) using Apify...")
        try:
            client = ApifyClientAsync(APIFY_API_TOKEN)
            actor_call = await client.actor("compass~crawler-google-places").call(
                run_input={
                    "startUrls": [{"url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"}],
                    "maxImages": max_images,
                    "maxReviews": 0,  # Don't need reviews here
                    "language": "zh-TW",
                    "scrapePlaceDetailPage": True,
                    "proxyConfiguration": {"useApifyProxy": True},
                }
            )

            list_items = []
            async for item in client.dataset(actor_call["defaultDatasetId"]).iterate_items():
                list_items.append(item)

            if list_items and "imageUrls" in list_items[0]:
                image_urls = list_items[0]["imageUrls"]
                print(f"Successfully fetched {len(image_urls)} images from Apify.")
                return image_urls
            else:
                print("No images found in Apify result.")
                return []
        except Exception as e:
            print(f"Error fetching images from Apify: {e}")
            return []

    async def extract_menu_from_images(self, image_urls: List[str]) -> List[MenuItem]:
        """
        Uses Gemini Vision API to extract menu items from restaurant images.
        """
        if not GEMINI_API_KEY:
            print("GEMINI_API_KEY is not set, skipping Vision API menu extraction.")
            return []

        if not image_urls:
            print("No images provided for Vision API extraction.")
            return []

        print(f"Extracting menu from {len(image_urls)} images using Gemini Vision API...")

        # Limit to first 5 images to avoid excessive API costs
        images_to_process = image_urls[:5]

        try:
            # Download images
            image_data = []
            async with httpx.AsyncClient() as client:
                for idx, url in enumerate(images_to_process):
                    try:
                        print(f"Downloading image {idx+1}/{len(images_to_process)}: {url[:60]}...")
                        response = await client.get(url, timeout=30)
                        response.raise_for_status()
                        image_data.append({
                            'mime_type': 'image/jpeg',
                            'data': response.content
                        })
                    except Exception as e:
                        print(f"Failed to download image {idx+1}: {e}")
                        continue

            if not image_data:
                print("No images could be downloaded.")
                return []

            print(f"Successfully downloaded {len(image_data)} images. Processing with Gemini Vision...")

            # Prepare prompt for Gemini Vision
            prompt = """
            You are an expert at reading restaurant menus from photos. Analyze the provided images and extract menu items.

            For each menu item you can clearly see, provide:
            - `name`: The exact name of the dish
            - `price`: The price as an integer (in TWD). If unclear, set to null
            - `category`: The category (e.g., "飯類", "麵點", "湯品", "小菜", "套餐"). Infer if not stated
            - `description`: Any descriptive text. Set to null if none
            - `source_type`: Set to "dine_in" since these are from photos

            IMPORTANT:
            - Only extract items where BOTH the dish name AND price are clearly visible
            - If a menu section header is visible but individual items aren't clear, skip it
            - If the image is not a menu (e.g., restaurant exterior, food photo), return empty array
            - If text is blurry or unclear, skip that item

            Return a valid JSON array of menu items. If no clear menu items can be extracted, return an empty array [].

            Schema:
            ```json
            [{
              "name": "string",
              "price": "integer | null",
              "category": "string",
              "description": "string | null",
              "source_type": "dine_in",
              "is_popular": false,
              "is_risky": false,
              "ai_insight": null
            }]
            ```
            """

            # Use Gemini Vision API
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Prepare content with images
            content_parts = [prompt]
            for img in image_data:
                content_parts.append({
                    'mime_type': img['mime_type'],
                    'data': img['data']
                })

            response = await model.generate_content_async(content_parts)

            menu_data_raw = response.text
            print(f"Gemini Vision response received. Parsing...")

            # Clean up response
            if menu_data_raw.startswith("```json"):
                menu_data_raw = menu_data_raw[len("```json"):].strip()
            if menu_data_raw.endswith("```"):
                menu_data_raw = menu_data_raw[:-len("```")].strip()

            menu_items_dicts = json.loads(menu_data_raw)

            if not menu_items_dicts:
                print("Gemini Vision returned empty menu items.")
                return []

            # Parse into MenuItem objects
            parsed_menu_items = [MenuItem(**item) for item in menu_items_dicts]
            print(f"Successfully extracted {len(parsed_menu_items)} menu items from images using Gemini Vision.")

            return parsed_menu_items

        except Exception as e:
            print(f"Error during Vision API menu extraction: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def vision_api_fallback(self, place_id: str, restaurant_name: str = "") -> List[MenuItem]:
        """
        Fallback method: Fetches images from Apify and uses Gemini Vision to extract menu.
        """
        print(f"Using Vision API fallback for {restaurant_name or place_id}...")

        # Step 1: Fetch images
        image_urls = await self.fetch_restaurant_images(place_id, restaurant_name or "Restaurant")

        if not image_urls:
            print("No images available. Returning placeholder dish.")
            return [MenuItem(name="Fallback Dish", price=120, category="Special", source_type="estimated")]

        # Step 2: Extract menu from images
        menu_items = await self.extract_menu_from_images(image_urls)

        if not menu_items:
            print("Could not extract menu from images. Returning placeholder dish.")
            return [MenuItem(name="Fallback Dish", price=120, category="Special", source_type="estimated")]

        return menu_items

if __name__ == "__main__":
    async def test_menu_scraper():
        scraper = MenuScraper()
        test_restaurant_name = "鼎泰豐"
        
        print("\n--- Testing search_menu_url ---")
        menu_url = await scraper.search_menu_url(test_restaurant_name)
        
        if menu_url:
            print(f"Serper found URL: {menu_url}")
            print("\n--- Testing fetch_and_parse_with_jina ---")
            jina_content = await scraper.fetch_and_parse_with_jina(menu_url)
            
            if jina_content:
                print("Jina Reader successfully extracted content.")
                print(f"--- Jina Content for Gemini Parsing ---\n{jina_content}\n---------------------------------------")
                print("\n--- Testing extract_menu_with_gemini ---")
                gemini_menu = await scraper.extract_menu_with_gemini(jina_content)
                if gemini_menu:
                    print(f"Gemini successfully extracted {len(gemini_menu)} menu items.")
                    print(json.dumps([item.model_dump() for item in gemini_menu], indent=2, ensure_ascii=False))
                else:
                    print("Gemini failed to extract menu items.")
            else:
                print("Jina Reader failed. Fallback would be used here.")
        else:
            print("Serper failed to find a URL. Fallback would be used here.")
            
    asyncio.run(test_menu_scraper())