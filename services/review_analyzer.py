import os
import asyncio
import json
import google.generativeai as genai
# from google.generativeai.client import Client # Removed incorrect import
from dotenv import load_dotenv
from typing import List, Tuple, Dict

from schemas.restaurant_profile import MenuItem

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ReviewAnalyzer:
    def __init__(self):
        # API key checks are now handled at the module level for more direct feedback
        pass

    async def fetch_reviews_apify(self, place_id: str, restaurant_name: str) -> List[Dict]:
        """
        Fetches the latest reviews for a given place_id and restaurant_name using Apify.
        """
        if not APIFY_API_TOKEN:
            return []

        print(f"Fetching reviews for place_id: {place_id}, name: {restaurant_name} using Apify...")
        try:
            client = ApifyClientAsync(APIFY_API_TOKEN)
            actor_call = await client.actor("compass~crawler-google-places").call(
                run_input={
                    "searchStringsArray": [f"{restaurant_name}"], # Use search string
                    "maxReviews": 10, # Limited for initial staging test
                    "language": "zh-TW",
                }
            )
            
            list_items = []
            async for item in client.dataset(actor_call["defaultDatasetId"]).iterate_items():
                list_items.append(item)

            if list_items and "reviews" in list_items[0]:
                reviews = list_items[0]["reviews"]
                print(f"Successfully fetched {len(reviews)} reviews from Apify.")
                return reviews
            else:
                print("No reviews found in Apify result.")
                return []
        except Exception as e:
            print(f"Error fetching reviews from Apify: {e}")
            return []
            
            
            
    async def analyze_and_fuse_reviews(self, reviews: List[Dict], menu_items: List[MenuItem]) -> Tuple[List[MenuItem], str]:
        """
        Analyzes reviews with Gemini and fuses the insights into the menu items.
        """
        if not GEMINI_API_KEY:
            print("GEMINI_API_KEY is not set, skipping review analysis.")
            return menu_items, "Review analysis was skipped due to missing API key."

        print("Analyzing reviews and fusing with menu using Gemini...")
        
        # Prepare data for the prompt
        review_texts = [f"Reviewer: {r.get('name', 'N/A')}, Rating: {r.get('stars', 'N/A')}, Text: {r.get('text', '')}" for r in reviews]
        menu_names = [item.name for item in menu_items]

        prompt = f"""
        You are an expert restaurant analyst. Your task is to analyze customer reviews and map their feedback directly onto a standard menu.

        This is the standard menu:
        ---
        {json.dumps(menu_names, ensure_ascii=False)}
        ---

        Analyze these customer reviews:
        ---
        {json.dumps(review_texts, ensure_ascii=False)}
        ---

        Based on the reviews, perform these actions:
        1. For each review, identify which dishes from the standard menu are being discussed. You must perform fuzzy matching (e.g., a review for "pork chop rice" should match the standard menu item "Fried Pork Chop with Rice").
        2. Aggregate all mentions for each standard menu item. Count how many times each dish was mentioned.
        3. For each mentioned dish, determine the overall sentiment ("positive", "negative", "neutral").
        4. For each mentioned dish, write a one-sentence summary of the feedback (e.g., "Pork chop is crispy and juicy" or "Soup was a bit bland").
        5. Identify if any dish has significant negative feedback that makes it "risky" (e.g., multiple mentions of being "cold", "raw", or "tasted bad").
        6. Generate an overall one-paragraph summary of all reviews.

        Your output MUST be a single, valid JSON object with two keys: "menu_analysis" and "overall_summary".
        The "menu_analysis" key should contain a list of objects, where each object corresponds to a dish from the standard menu that was mentioned in the reviews.

        Example output format:
        {{
          "menu_analysis": [
            {{
              "name": "Fried Pork Chop with Rice",
              "sentiment": "positive",
              "summary": "Most customers find the pork chop crispy and a must-order item.",
              "mention_count": 5,
              "is_risky": false
            }}
          ],
          "overall_summary": "The restaurant is highly praised for its signature pork chop rice and noodle soups. However, some diners mentioned that the appetizers can be inconsistent."
        }}
        """

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = await model.generate_content_async(prompt)
            
            analysis_raw = response.text
            if analysis_raw.startswith("```json"):
                analysis_raw = analysis_raw[len("```json"):].strip()
            if analysis_raw.endswith("```"):
                analysis_raw = analysis_raw[:-len("```")].strip()

            analysis_data = json.loads(analysis_raw)
            
            menu_analysis = analysis_data.get("menu_analysis", [])
            overall_summary = analysis_data.get("overall_summary", "Could not generate summary.")

            # Create a mapping from menu name to analysis result
            analysis_map = {item["name"]: item for item in menu_analysis}

            # Fuse the analysis back into the original menu_items list
            for menu_item in menu_items:
                if menu_item.name in analysis_map:
                    analysis = analysis_map[menu_item.name]
                    menu_item.is_popular = True # If it's mentioned, it's popular
                    menu_item.is_risky = analysis.get("is_risky", False)
                    menu_item.ai_insight = {
                        "sentiment": analysis.get("sentiment", "neutral"),
                        "summary": analysis.get("summary", ""),
                        "mention_count": analysis.get("mention_count", 0)
                    }
            
            print("Successfully analyzed reviews and fused insights into menu.")
            return menu_items, overall_summary

        except Exception as e:
            print(f"An unexpected error occurred during review analysis: {e}")
            return menu_items, f"Error during review analysis: {e}"


if __name__ == '__main__':
    # A dummy test for the ReviewAnalyzer
    async def test_review_analyzer():
        analyzer = ReviewAnalyzer()
        
        # Mock data similar to what the scraper would produce
        mock_menu = [
            MenuItem(name="排骨蛋炒飯", price=280, category="飯類"),
            MenuItem(name="蝦肉紅油抄手", price=190, category="抄手"),
            MenuItem(name="酸辣湯", price=110, category="湯品")
        ]
        
        mock_reviews = [
            {"name": "User A", "stars": 5, "text": "The fried rice with pork chop is amazing, a must-try! The best I've ever had."},
            {"name": "User B", "stars": 2, "text": "My wontons in chili oil were cold and stuck together. Very disappointing. The pork chop rice was good though."},
            {"name": "User C", "stars": 4, "text": "Hot and sour soup was decent, and my friend loved the pork fried rice."}
        ]
        
        enriched_menu, summary = await analyzer.analyze_and_fuse_reviews(mock_reviews, mock_menu)
        
        print("\n--- Review Analysis Summary ---")
        print(summary)
        print("\n--- Enriched Menu Items ---")
        print(json.dumps([item.model_dump() for item in enriched_menu], indent=2, ensure_ascii=False))

    asyncio.run(test_review_analyzer())
