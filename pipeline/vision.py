import os
import asyncio
import json
import google.generativeai as genai
from typing import List, Dict, Any, Tuple, Optional
from dotenv import load_dotenv
from schemas.restaurant_profile import MenuItem, Evidence
import requests
from PIL import Image
import io
import re

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize models
try:
    FLASH_MODEL = genai.GenerativeModel('gemini-1.5-flash')
    PRO_VISION_MODEL = genai.GenerativeModel('gemini-2.5-flash-image') # Corrected model name for vision tasks
except Exception as e:
    print(f"Error initializing Gemini models: {e}")
    FLASH_MODEL = None
    PRO_VISION_MODEL = None


async def image_filter(image_urls: List[str]) -> List[Tuple[Image.Image, str]]:
    """
    Filters a list of image URLs, returning a list of tuples containing
    PIL Image objects and their original URLs for those identified as restaurant menus.
    """
    if not PRO_VISION_MODEL:
        print("Error: Gemini 1.5 Pro Vision model not initialized for image filtering.")
        return []

    print(f"Filtering {len(image_urls)} images for menus using Gemini 1.5 Pro Vision...")

    async def filter_single_image(url: str) -> Optional[Tuple[Image.Image, str]]:
        prompt = "Is this image a restaurant menu? Answer YES or NO. Only output YES or NO."
        try:
            # Download the image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))
            
            # Send to Gemini
            gemini_response = await PRO_VISION_MODEL.generate_content_async(
                [prompt, img],
                generation_config={"response_mime_type": "text/plain"}
            )
            print(f"Gemini image_filter response for {url}: '{gemini_response.text.strip()}'")
            
            if gemini_response.text and gemini_response.text.strip().upper() == "YES":
                return img, url
        except Exception as e:
            print(f"Error filtering image {url}: {e}")
        return None

    tasks = [filter_single_image(url) for url in image_urls]
    filtered_results = await asyncio.gather(*tasks)
    
    menus = [result for result in filtered_results if result is not None]
    print(f"Identified {len(menus)} menu images.")
    return menus


async def menu_extractor_ocr(menu_images_with_urls: List[Tuple[Image.Image, str]]) -> List[MenuItem]:
    """
    Extracts menu items from a list of PIL Image objects.
    """
    if not PRO_VISION_MODEL: # Using Pro Vision model
        print("Error: Gemini 1.5 Pro Vision model not initialized for OCR.")
        return []
    if not menu_images_with_urls:
        return []

    print(f"Extracting menu items from {len(menu_images_with_urls)} menu images using Gemini 1.5 Pro Vision...")

    all_menu_items: List[MenuItem] = []

    for img, url in menu_images_with_urls:
        prompt = """
        From this restaurant menu image, extract all individual menu items.
        For each item, identify its dish name, price (integer only, if available), and a general category (e.g., Appetizer, Main Course, Drink, Dessert, Soup).
        If a description is available, include it.
        Return the data as a JSON array of objects, where each object has:
        'name': string (dish name),
        'price': integer (price, e.g., 280),
        'category': string (general category),
        'description': string (optional),
        'id': string (a unique identifier for the dish, e.g., "d_01", "d_02").
        
        Example JSON output:
        ```json
        [
          {"id": "d_01", "name": "排骨蛋炒飯", "price": 280, "category": "米食", "description": "店內招牌，酥炸排骨搭配粒粒分明的炒飯"},
          {"id": "d_02", "name": "酸辣湯", "price": 110, "category": "湯品"}
        ]
        ```
        If no menu items can be extracted, return an empty JSON array `[]` wrapped in a markdown code block ````json\n[]\n```.
        """
        try:
            response = await PRO_VISION_MODEL.generate_content_async(
                [prompt, img]
                # Removed generation_config={"response_mime_type": "application/json"}
            )
            
            response_text = response.text
            print(f"Gemini menu_extractor_ocr raw response for {url}: '{response_text.strip()}'")
            json_match = re.search(r"```json\n(.*?)```", response_text, re.DOTALL)
            
            if json_match:
                json_string = json_match.group(1)
                extracted_items_raw = json.loads(json_string)
            else:
                print(f"Warning: No JSON markdown block found in Gemini response: {response_text[:200]}...")
                extracted_items_raw = []
            
            for i, item_raw in enumerate(extracted_items_raw):
                item_raw['id'] = item_raw.get('id') or f"d_{len(all_menu_items) + i + 1:02d}"
                item_raw['price'] = int(item_raw['price']) if 'price' in item_raw else 0
                
                menu_item = MenuItem(
                    name=item_raw['name'],
                    price=item_raw['price'],
                    original_category=item_raw.get('category', '其他'),
                    standard_category=item_raw.get('category', '其他'), # Placeholder
                    description=item_raw.get('description'),
                    tags=[],
                    id=item_raw['id'],
                    evidence=Evidence(image_url=url, ocr_confidence=1.0) # Assume 1.0 confidence
                )
                all_menu_items.append(menu_item)
            
        except Exception as e:
            print(f"Error extracting menu from image: {e}")
    
    print(f"Extracted {len(all_menu_items)} menu items in total.")
    return all_menu_items

if __name__ == "__main__":
    async def test_vision():
        if not os.getenv("GEMINI_API_KEY"):
            print("Please set GEMINI_API_KEY in your .env file to run this test.")
            return
        
        print("Please uncomment and update the test calls in pipeline/vision.py to run live tests.")
        print("Note: Live testing requires actual image URLs and API quota.")
        # Example to test:
        # test_url = "URL_TO_A_MENU_IMAGE"
        # response = requests.get(test_url)
        # img = Image.open(io.BytesIO(response.content))
        # extracted = await menu_extractor_ocr([(img, test_url)])
        # print(extracted)

    asyncio.run(test_vision())