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
    The 'Explorer': Finds external validation from web search.
    """
    async def run(self, restaurant_name: str) -> AgentResult:
        print(f"SearchAgent: Searching for {restaurant_name}...")
        search_results = await fetch_menu_from_search(restaurant_name)
        
        prompt = f"""
        Extract dish names and prices from these search snippets.
        
        Snippets:
        {search_results}
        
        Return a JSON list:
        [
            {"dish_name": "Name", "price": 100, "source_snippet": "..."}
        ]
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return AgentResult(source="search", data=data, confidence=0.6)
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
