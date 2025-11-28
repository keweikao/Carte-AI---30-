import os
import json
import asyncio
import google.generativeai as genai
from typing import List, Dict, Any

class MenuExtractionSkill:
    """
    A reusable skill for extracting structured menu data from images using Gemini Vision.
    """
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def execute(self, images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes the OCR skill on a list of images.
        """
        if not images:
            return []

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
                [prompt] + images,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Basic validation
            if isinstance(data, dict) and "menu_items" in data:
                return data["menu_items"]
            elif isinstance(data, list):
                return data
            else:
                return []
                
        except Exception as e:
            print(f"MenuExtractionSkill Error: {e}")
            return []
