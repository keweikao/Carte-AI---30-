import os
import json
import asyncio
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from agent.data_fetcher import fetch_place_photo, fetch_place_details, fetch_menu_from_search

@dataclass
class AgentResult:
    source: str
    data: List[Dict[str, Any]]
    confidence: float = 0.0
    metadata: Dict[str, Any] = None

class BaseAgent:
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def run(self, *args, **kwargs) -> AgentResult:
        raise NotImplementedError

class VisualAgent(BaseAgent):
    """
    The 'Eye': Extracts structured menu data from images.
    """
    def __init__(self):
        super().__init__(model_name='gemini-2.5-flash') # Or Pro Vision if available/needed

    async def run(self, photos_data: List[Dict[str, Any]]) -> AgentResult:
        print("VisualAgent: Analyzing photos...")
        if not photos_data:
            return AgentResult(source="visual", data=[], confidence=0.0)

        # Fetch photos (limit to top 5 to save time/cost)
        target_photos = photos_data[:5]
        photo_tasks = [fetch_place_photo(photo["photo_reference"]) for photo in target_photos]
        photo_blobs = await asyncio.gather(*photo_tasks)
        
        valid_images = []
        for blob in photo_blobs:
            if blob:
                valid_images.append({
                    "mime_type": "image/jpeg",
                    "data": blob
                })
        
        if not valid_images:
            return AgentResult(source="visual", data=[], confidence=0.0)

        prompt = """
        You are a Menu Transcription Expert. 
        Analyze these restaurant images. Identify ANY menu pages or food items with visible prices.
        
        Extract a JSON list of items found. Format:
        [
            {"dish_name": "Name", "price": 100, "description": "visible text"}
        ]
        
        Rules:
        1. Only extract text that is clearly visible. Do NOT hallucinate.
        2. If price is missing, set price to null.
        3. Ignore non-food text (like phone numbers, addresses).
        """

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt] + valid_images,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            # Basic validation: ensure it's a list
            if isinstance(data, dict) and "menu_items" in data:
                data = data["menu_items"]
            elif not isinstance(data, list):
                data = []
                
            return AgentResult(source="visual", data=data, confidence=0.9, metadata={"image_count": len(valid_images)})
        except Exception as e:
            print(f"VisualAgent Error: {e}")
            return AgentResult(source="visual", data=[], confidence=0.0)

class ReviewAgent(BaseAgent):
    """
    The 'Ear': Identifies signature dishes from reviews.
    """
    async def run(self, reviews_data: Dict[str, Any]) -> AgentResult:
        print("ReviewAgent: Analyzing reviews...")
        reviews_text = json.dumps(reviews_data.get("reviews", []), ensure_ascii=False)
        
        prompt = f"""
        Analyze these restaurant reviews to identify the most popular/signature dishes.
        
        Reviews:
        {reviews_text[:10000]}
        
        Return a JSON list:
        [
            {"dish_name": "Name", "popularity_score": 1-10, "reason": "Mentioned by 5 users as must-try"}
        ]
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return AgentResult(source="review", data=data, confidence=0.7)
        except Exception as e:
            print(f"ReviewAgent Error: {e}")
            return AgentResult(source="review", data=[], confidence=0.0)

class SearchAgent(BaseAgent):
    """
    The 'Explorer': Finds external validation from web search using the 'Gourmet Insight Hunter' persona.
    """
    def _detect_region(self, restaurant_name: str) -> str:
        """Simple heuristic to detect region based on character sets."""
        if any("\u3040" <= c <= "\u30ff" for c in restaurant_name): # Hiragana/Katakana
            return "JP"
        if any("\uac00" <= c <= "\ud7a3" for c in restaurant_name): # Hangul
            return "KR"
        if any("\u4e00" <= c <= "\u9fff" for c in restaurant_name): # CJK Unified Ideographs
            return "TC" # Default to TC for Hanzi (could be SC, but user context is TW)
        return "EN" # Default to English/Global

    def _construct_query(self, restaurant_name: str, region: str) -> str:
        """Constructs a boolean search query based on region."""
        keywords = {
            "TC": {
                "dish": '("必點" OR "招牌" OR "推薦" OR "必吃")',
                "vibe": '("特色" OR "打卡" OR "氛圍" OR "景觀" OR "好拍")',
                "neg": '-site:ubereats.com -site:foodpanda.tw -site:deliveroo.hk'
            },
            "JP": {
                "dish": '("名物" OR "必食" OR "看板メニュー" OR "一番人気")',
                "vibe": '("雰囲気" OR "個室" OR "絶景" OR "隠れ家" OR "インスタ映え")',
                "neg": '-site:ubereats.com -site:demae-can.com'
            },
            "KR": {
                "dish": '("대표메뉴" OR "추천" OR "시그니처" OR "존맛")',
                "vibe": '("분위기" OR "감성" OR "뷰맛집" OR "이색")',
                "neg": '-site:baemin.com -site:yogiyo.co.kr'
            },
            "EN": {
                "dish": '("Must order" OR "Signature dish" OR "Best dish" OR "Highly recommend")',
                "vibe": '("Atmosphere" OR "Vibe" OR "Interior" OR "Hidden gem")',
                "neg": '-site:ubereats.com -site:grubhub.com -site:doordash.com -site:yelp.com'
            }
        }
        
        k = keywords.get(region, keywords["EN"])
        # Combine Dish and Vibe keywords to maximize single API call efficiency
        # Query: "{Name}" ({Dish} OR {Vibe}) {Neg}
        return f'"{restaurant_name}" ({k["dish"]} OR {k["vibe"]}) {k["neg"]}'

    async def run(self, restaurant_name: str) -> AgentResult:
        region = self._detect_region(restaurant_name)
        query = self._construct_query(restaurant_name, region)
        
        print(f"SearchAgent: Searching for {restaurant_name} (Region: {region})...")
        print(f"Query: {query}")
        
        # Fetch max 10 results
        search_results = await fetch_menu_from_search(restaurant_name, query=query, num=10)
        
        prompt = f"""
        # Role
        You are the "Gourmet Insight Hunter," an expert dining analyst.
        
        # Task
        Analyze these search snippets for "{restaurant_name}" ({region}) to extract:
        1. Signature Dishes (Verified by mentions)
        2. Vibe & Features
        3. Expert Verdict
        
        # Search Snippets
        {search_results}
        
        # Output Format (Strict JSON)
        {{
          "restaurant_name": "{restaurant_name}",
          "search_region": "{region}",
          "signature_dishes": [
            {{
              "dish_name": "String",
              "confidence_score": "High/Medium",
              "reason": "Brief quote (e.g., 'Mentioned as must-eat in 3 blogs')"
            }}
          ],
          "features_and_vibe": [
            "String (e.g., Rooftop view)",
            "String (e.g., Retro style)"
          ],
          "expert_verdict": {{
            "pros": "String",
            "cons": "String (if negative keywords found)",
            "buying_intent": "String (e.g., Good for dates, Best for solo dining)"
          }}
        }}
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Normalize output for Aggregator
            # We need to transform the specific "Gourmet" format back to a generic list for the aggregator
            # OR update the aggregator to handle this rich data.
            # For now, let's map 'signature_dishes' to the standard data list 
            # and keep the full rich object in 'metadata'.
            
            standard_data = []
            if "signature_dishes" in data:
                for dish in data["signature_dishes"]:
                    standard_data.append({
                        "dish_name": dish.get("dish_name"),
                        "price": None, # Search snippets often miss price, but that's ok
                        "reason": dish.get("reason"),
                        "confidence": dish.get("confidence_score")
                    })
            
            return AgentResult(source="search", data=standard_data, confidence=0.8, metadata=data)
            
        except Exception as e:
            print(f"SearchAgent Error: {e}")
            return AgentResult(source="search", data=[], confidence=0.0)

class AggregationAgent:
    """
    The 'Judge': Synthesizes data and assigns confidence scores.
    """
    def run(self, results: List[AgentResult]) -> List[Dict[str, Any]]:
        print("AggregationAgent: Synthesizing results...")
        
        # 1. Flatten all items
        all_items = []
        for res in results:
            for item in res.data:
                item["source"] = res.source
                item["base_confidence"] = res.confidence
                all_items.append(item)
        
        # 2. Simple deduplication and scoring (Placeholder logic)
        # In a real implementation, we would use fuzzy matching to merge "Beef Noodle" and "Beef Noodles"
        
        # For now, just pass through with an added 'final_score'
        final_pool = []
        for item in all_items:
            score = item.get("base_confidence", 0.5) * 100
            
            # Boost if price is present
            if item.get("price"):
                score += 10
                
            item["confidence_score"] = min(score, 100)
            final_pool.append(item)
            
        return final_pool
