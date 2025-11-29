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

from agent.skills import MenuExtractionSkill

class VisualAgent(BaseAgent):
    """
    The 'Eye': Extracts structured menu data from images using the MenuExtractionSkill.
    """
    def __init__(self):
        super().__init__(model_name='gemini-2.5-flash')
        self.ocr_skill = MenuExtractionSkill(model_name='gemini-2.5-flash')

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

        # Use the Skill
        extracted_items = await self.ocr_skill.execute(valid_images)
        
        confidence = 0.9 if extracted_items else 0.0
        return AgentResult(source="visual", data=extracted_items, confidence=confidence, metadata={"image_count": len(valid_images), "blobs": valid_images})

class ReviewAgent(BaseAgent):
    """
    The 'Ear': Identifies signature dishes from reviews.
    """
    async def run(self, reviews_data: Dict[str, Any]) -> AgentResult:
        print("ReviewAgent: Analyzing reviews...")
        reviews_text = json.dumps(reviews_data.get("reviews", []), ensure_ascii=False, default=str)
        
        prompt = f"""
        Analyze these restaurant reviews to identify the most popular/signature dishes.
        
        Reviews:
        {reviews_text[:10000]}
        
        Return a JSON list:
        [
            {{"dish_name": "Name", "popularity_score": 1-10, "reason": "Mentioned by 5 users as must-try"}}
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
You are the "Gourmet Insight Hunter," an expert dining analyst with 10 years of experience in keyword marketing and SEO data mining. Your goal is to extract the true "Signature Dishes" and "Unique Selling Points (USP)" of a restaurant from the web, filtering out marketing noise.

# Core Objective
When provided with "{restaurant_name}" in region "{region}", you must analyze the search snippets to find:
1.  **Top 3 Signature Dishes** (Verified by high-frequency mentions in reviews).
2.  **Vibe & Features** (Interior style, view, atmosphere, "Instagrammable" spots).
3.  **Local Reputation** (Authenticity check, queue status, or "CP value").

# Search Snippets Analysis
Analyze these web search results and identify food items appearing near "High Confidence" keywords:

{search_results[:15000]}

# Output Format (Strict JSON)
Return a JSON object with the following structure:

{{
  "restaurant_name": "{restaurant_name}",
  "search_region": "{region}",
  "signature_dishes": [
    {{
      "dish_name": "String (Exact dish name)",
      "confidence_score": "High/Medium (High = mentioned 3+ times, Medium = 1-2 times)",
      "reason": "String (Brief evidence, e.g., 'Mentioned as must-eat in 3 food blogs, praised for crispy skin')"
    }}
  ],
  "features_and_vibe": [
    "String (e.g., 'Rooftop dining with city view')",
    "String (e.g., 'Retro 1980s decor')",
    "String (e.g., 'Instagram-worthy presentation')"
  ],
  "expert_verdict": {{
    "pros": "String (Main strengths based on search consensus)",
    "cons": "String (Any negative patterns found, or 'None detected')",
    "buying_intent": "String (e.g., 'Best for romantic dates', 'Great for large groups', 'Solo dining friendly')"
  }}
}}

**CRITICAL RULES:**
Lint and Test
Process completed with exit code 1.
Lint and Test: frontend/src/app/recommendation/page.tsx#L228
Unexpected any. Specify a different type
Lint and Test: frontend/src/app/recommendation/page.tsx#L11
'getRecommendations' is defined but never used
1. Only include dishes that are EXPLICITLY mentioned in the search results
2. Confidence = "High" only if mentioned 3+ times across different sources
3. If no clear signature dishes found, return empty array for signature_dishes
4. Extract actual quotes or paraphrases for the "reason" field
5. Focus on UNIQUE features, not generic descriptions
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Normalize output for Aggregator
            # Transform the "Gourmet Insight Hunter" format to standard data list
            # Keep the full rich object in 'metadata' for the Aggregator to use
            
            standard_data = []
            if "signature_dishes" in data:
                for dish in data["signature_dishes"]:
                    standard_data.append({
                        "dish_name": dish.get("dish_name"),
                        "price": None, # Search snippets often miss price
                        "reason": dish.get("reason"),
                        "confidence": dish.get("confidence_score")
                    })
            
            # Return both standard format and rich metadata
            return AgentResult(source="search", data=standard_data, confidence=0.8, metadata=data)
            
        except Exception as e:
            print(f"SearchAgent Error: {e}")
            import traceback
            traceback.print_exc()
            return AgentResult(source="search", data=[], confidence=0.0)

class AggregationAgent(BaseAgent):
    """
    The 'Judge': Synthesizes data from all agents using the 'Executive Dining Strategist' persona.
    """
    def __init__(self):
        super().__init__(model_name='gemini-2.5-flash')

    async def run(self, results: List[AgentResult]) -> List[Dict[str, Any]]:
        print("AggregationAgent: Synthesizing results with Executive Strategy...")
        
        # Organize inputs by source
        ocr_data = []
        review_data = []
        search_data = []
        
        for res in results:
            if res.source == "visual":
                ocr_data = res.data
            elif res.source == "review":
                review_data = res.data
            elif res.source == "search":
                search_data = res.data # This is the standard list, metadata has the rich JSON
                # If search agent returns rich metadata, we might want to use that instead for the prompt
                if res.metadata:
                    search_data = res.metadata

        # Construct Prompt Inputs
        prompt_inputs = f"""
        # Source 1: OCR Agent (Official Menu)
        {json.dumps(ocr_data, ensure_ascii=False, indent=2, default=str)}
        
        # Source 2: Review Agent (Google Reviews)
        {json.dumps(review_data, ensure_ascii=False, indent=2, default=str)}
        
        # Source 3: Search Agent (Web/Blogs)
        {json.dumps(search_data, ensure_ascii=False, indent=2, default=str)}
        """

        prompt = f"""
# Role
You are the **"Executive Dining Strategist,"** responsible for synthesizing data from three distinct intelligence sources to construct a "Golden Profile" for the restaurant.

# Input Sources
1.  **OCR Agent:** Official Menu Data (Facts, Prices, Categories).
2.  **Review Agent:** Google Maps Reviews (Mass Sentiment, Service Issues).
3.  **Search Agent:** Blog/Web Articles (Deep Dives, Hidden Gems).

# Data Triangulation Logic (The Source of Truth)

Apply the following weighting logic to resolve conflicts:

## 1. Dish Recommendation Logic (The "Signature Matrix")
* **CONFIRMED STAR:** Highlighted in **OCR** AND praised in **Search** AND high positive volume in **Reviews**.
* **HIDDEN GEM:** NOT in **OCR** highlights but strongly recommended in **Search** and verified by **Reviews**.
* **OVERRATED TRAP:** Highlighted in **OCR** or **Search**, but negative sentiment in **Reviews** (e.g., "Salty," "Dry"). -> *Mark as "Avoid".*

## 2. Price & Value Logic
* **Use OCR** for exact price baseline.
* **Use Reviews** for "Perceived Value" (CP value).
* *Insight:* If OCR price is high but Reviews say "Small portion," flag as "Low CP Value."

## 3. Vibe & Scenario Match
* **Use Search** for visual descriptions (e.g., "Good for dates").
* **Use Reviews** for functional reality (e.g., "Too noisy").

# Processing Instructions
1.  **Map Entities:** Fuzzy match dish names across 3 sources (e.g., "Spicy Beef Noodle" = "Beef Noodles").
2.  **Flag Warnings:** Look for "Hygiene issues" or "Service attitude" in Reviews.

# Input Data
{prompt_inputs}

# Output Format (JSON)

Produce a single JSON object analyzing the restaurant:

{{
  "restaurant_name": "String",
  "overall_verdict": "String (One sentence executive summary, e.g., 'Visual stunner with average food, best for photos not foodies.')",
  "dining_scenario": ["Date Night", "Group Gathering", "Solo"],
  "signature_dishes": [
    {{
      "name": "String",
      "price": "String (From OCR, or 'Unknown')",
      "status": "Must Order / Hidden Gem / Controversial",
      "reasoning": "String (e.g., 'Official recommendation validated by 50+ positive reviews, specifically for the truffle sauce.')"
    }}
  ],
  "avoid_items": [
    {{
      "name": "String",
      "reason": "String (e.g., 'High blog buzz but consistent complaints about being undercooked in recent reviews.')"
    }}
  ],
  "price_analysis": {{
    "average_cost": "String",
    "value_rating": "High/Medium/Low (CP Value)",
    "note": "String (e.g., 'Pricey for the portion size.')"
  }},
  "warnings": ["String (e.g., Cash Only)", "String (e.g., Rude service peak hours)"]
}}

**CRITICAL RULES:**
1. **Fuzzy Match Aggressively**: "小籠包" = "小笼包" = "Xiaolongbao" = "Soup Dumplings"
2. **Triangulation Priority**: OCR (Facts) + Search (Expertise) + Reviews (Reality Check)
3. **Confidence Scoring**: 
   - Must Order = Confirmed in all 3 sources
   - Hidden Gem = Strong in Search + Reviews, weak/missing in OCR
   - Controversial = Mixed signals across sources
4. **Value Analysis**: Compare OCR prices with Review sentiment about portions/quality
5. **Scenario Matching**: Extract dining scenarios from Search metadata (vibe) and Review patterns
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Transform to standard format for the main agent
            final_pool = []
            if "signature_dishes" in data:
                for dish in data["signature_dishes"]:
                    final_pool.append({
                        "dish_name": dish.get("name"),
                        "price": dish.get("price"), # Might be a string like "$100" or "Unknown"
                        "reason": dish.get("reasoning"),
                        "source": "aggregator",
                        "status": dish.get("status"),
                        "confidence_score": 95 if dish.get("status") == "Must Order" else 85
                    })
            
            # We can also return the full analysis in a special way if needed, 
            # but the interface expects List[Dict].
            # Let's attach the full analysis to the first item's metadata or similar if we want to preserve it,
            # or just rely on the high confidence candidates list.
            
            return final_pool
            
        except Exception as e:
            print(f"AggregationAgent Error: {e}")
            # Fallback to simple aggregation if LLM fails
            return []
