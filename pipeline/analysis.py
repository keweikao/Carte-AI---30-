import os
import asyncio
import json
import google.generativeai as genai
from collections import Counter
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
import re

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Flash model for tagging
try:
    FLASH_MODEL = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error initializing Gemini 1.5 Flash model for analysis: {e}")
    FLASH_MODEL = None

async def perform_keyword_analysis(reviews: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Performs keyword frequency analysis on a list of reviews.
    Currently a simple word counter. Can be expanded with NLP techniques.
    """
    all_text = " ".join([review.get('text', '') for review in reviews if review.get('text')])
    words = re.findall(r'\b\w+\b', all_text.lower()) # Simple word tokenization
    
    # Filter out common stopwords if desired, or focus on multi-word phrases
    # For now, a basic counter
    word_counts = Counter(words)
    
    # Return top N keywords, or process further
    return dict(word_counts.most_common(50)) # Top 50 keywords

async def dish_tagger(dish_name: str, review_snippets: List[str]) -> List[str]:
    """
    Generates descriptive tags for a dish based on relevant review snippets
    using Gemini 1.5 Flash.
    """
    if not FLASH_MODEL:
        print("Error: Gemini 1.5 Flash model not initialized.")
        return []

    if not review_snippets:
        return []

    combined_snippets = "\n".join([f"- {s}" for s in review_snippets])

    prompt = f"""
    Given the dish name "{dish_name}" and the following review snippets related to it:
    {combined_snippets}

    Generate a concise list of 3-5 descriptive tags for this dish.
    Focus on flavor profiles, characteristics, popularity, or specific cooking methods mentioned.
    Avoid tags like "dish" or "food".
    Return the tags as a JSON array of strings.

    Example:
    Dish name: "排骨蛋炒飯"
    Snippets:
    - "鼎泰豐的排骨蛋炒飯真是必點，排骨炸得香酥"
    - "炒飯粒粒分明，排骨很大塊"
    - "每次來都點排骨蛋炒飯，味道一級棒"
    Output: ["必點", "香酥", "粒粒分明", "人氣"]
    """
    try:
        response = await FLASH_MODEL.generate_content_async(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        tags = json.loads(response.text)
        if isinstance(tags, list) and all(isinstance(tag, str) for tag in tags):
            return tags
        else:
            print(f"Warning: Dish tagger returned non-list or non-string tags for {dish_name}: {tags}")
            return []
    except Exception as e:
        print(f"Error calling Gemini Flash for dish tagging {dish_name}: {e}")
        return []

if __name__ == "__main__":
    async def test_analysis():
        if not os.getenv("GEMINI_API_KEY"):
            print("Please set GEMINI_API_KEY in your .env file to run LLM-based analysis tests.")
            return

        print("--- Testing Keyword Analysis (Placeholder) ---")
        sample_reviews = [
            {"text": "這家餐廳的排骨炒飯真是必點，排骨炸得香酥，炒飯粒粒分明，味道一級棒。"},
            {"text": "酸辣湯很開胃，每次來都會點，裡面料很實在。"},
            {"text": "服務很好，環境也很舒適，但排骨炒飯有點油。"}
        ]
        keywords = await perform_keyword_analysis(sample_reviews)
        print(f"Top keywords: {keywords}")

        print("\n--- Testing Dish Tagger ---")
        dish = "排骨蛋炒飯"
        snippets = [
            "排骨炒飯真是必點",
            "排骨炸得香酥",
            "炒飯粒粒分明",
            "每次來都點排骨蛋炒飯",
            "排骨很大塊，吃得很滿足"
        ]
        tags = await dish_tagger(dish, snippets)
        print(f"Tags for '{dish}': {tags}")

        dish = "酸辣湯"
        snippets_soup = [
            "酸辣湯很開胃，料多實在",
            "冬天喝一碗酸辣湯超舒服",
            "酸辣湯有點太酸了"
        ]
        tags_soup = await dish_tagger(dish, snippets_soup)
        print(f"Tags for '{dish_soup}': {tags_soup}")


    asyncio.run(test_analysis())
