import re
import asyncio
import os
import json
import google.generativeai as genai
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Flash model for category normalization
try:
    FLASH_MODEL = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error initializing Gemini 1.5 Flash model for normalization: {e}")
    FLASH_MODEL = None

# Standard categories based on common restaurant types and UI needs
STANDARD_CATEGORIES = {
    "主食": "main_course",
    "飯": "main_course",
    "麵": "main_course",
    "點心": "appetizer",
    "小吃": "appetizer",
    "開胃菜": "appetizer",
    "前菜": "appetizer",
    "湯": "soup",
    "湯品": "soup",
    "飲料": "drink",
    "飲品": "drink",
    "甜點": "dessert",
    "冰品": "dessert",
    "沙拉": "salad",
    "蔬菜": "vegetable",
    "青菜": "vegetable",
    "肉": "meat",
    "海鮮": "seafood",
    "酒": "drink",
    "套餐": "set_menu",
    "其他": "other",
    "麵飯": "main_course", # Handle combined categories
    "主菜": "main_course",
    "開胃小點": "appetizer",
    "炸物": "appetizer",
    "烤物": "appetizer",
    "熱炒": "main_course",
    "鍋物": "main_course",
}

async def normalize_price(price_str: str) -> int:
    """
    Cleans a price string and converts it to an integer.
    Removes currency symbols, commas, and other non-digit characters.
    """
    if isinstance(price_str, (int, float)):
        return int(price_str)
    
    clean_str = re.sub(r'[^\d.]', '', price_str) # Remove non-digits except dot
    try:
        # Handle cases like "100.5" or "100"
        return int(float(clean_str))
    except ValueError:
        return 0 # Default to 0 if conversion fails


async def normalize_category(original_category: str) -> str:
    """
    Maps an original category string to a standardized category using a mapping dictionary
    or Gemini Flash as a fallback.
    """
    # Try direct mapping first (case-insensitive)
    for key, value in STANDARD_CATEGORIES.items():
        if key.lower() in original_category.lower():
            return value
    
    # Fallback to LLM if no direct match, for broader category recognition
    if FLASH_MODEL:
        prompt = f"""
        Given the original menu category "{original_category}", map it to one of the following standard categories:
        {json.dumps(list(set(STANDARD_CATEGORIES.values())))} 
        
        If it doesn't fit any, use "other".
        Only output the standard category name.
        Example: "米食" -> "main_course"
        Example: "小菜" -> "appetizer"
        Example: "前菜" -> "appetizer"
        Example: "啤酒" -> "drink"
        Example: "今日推薦" -> "other"
        """
        try:
            response = await FLASH_MODEL.generate_content_async(
                prompt,
                generation_config={"response_mime_type": "text/plain"}
            )
            standardized = response.text.strip().lower()
            if standardized in STANDARD_CATEGORIES.values():
                return standardized
        except Exception as e:
            print(f"Error calling Gemini Flash for category normalization: {e}")
    
    return "other" # Default fallback


if __name__ == "__main__":
    async def test_normalization():
        if not os.getenv("GEMINI_API_KEY"):
            print("Please set GEMINI_API_KEY in your .env file to run LLM-based normalization tests.")
            # return # Do not return, so we can test price normalization
        
        print("--- Testing Price Normalization ---")
        print(f"'NT$ 280' -> {await normalize_price('NT$ 280')}")
        print(f"'120元' -> {await normalize_price('120元')}")
        print(f"'$15.50' -> {await normalize_price('$15.50')}")
        print(f"'免費' -> {await normalize_price('免費')}")
        print(f"100 -> {await normalize_price(100)}")

        print("\n--- Testing Category Normalization ---")
        if FLASH_MODEL:
            print(f"'米食' -> {await normalize_category('米食')}")
            print(f"'開胃小點' -> {await normalize_category('開胃小點')}")
            print(f"'啤酒' -> {await normalize_category('啤酒')}")
            print(f"'本週特餐' -> {await normalize_category('本週特餐')}")
            print(f"'Soups & Salads' -> {await normalize_category('Soups & Salads')}") # Test LLM fallback
            print(f"'Appetizers' -> {await normalize_category('Appetizers')}") # Test LLM fallback
        else:
            print("Gemini Flash model not initialized, skipping LLM category normalization tests.")

    asyncio.run(test_normalization())
