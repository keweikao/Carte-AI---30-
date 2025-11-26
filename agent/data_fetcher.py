import os
import httpx
from dotenv import load_dotenv
import asyncio

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

async def fetch_place_details(restaurant_name: str) -> dict:
    """
    Fetches place details (reviews, rating) from Google Places API.
    Note: This is a simplified implementation using Text Search to find the place first.
    """
    if not GOOGLE_API_KEY:
        return {"error": "Missing GOOGLE_API_KEY"}

    async with httpx.AsyncClient() as client:
        # 1. Find Place ID
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": restaurant_name,
            "key": GOOGLE_API_KEY,
            "language": "zh-TW"
        }
        try:
            response = await client.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return {"error": "Restaurant not found"}
            
            place_id = data["results"][0]["place_id"]
            
            # 2. Get Details (Reviews)
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "name,rating,reviews,formatted_address",
                "key": GOOGLE_API_KEY,
                "language": "zh-TW"
            }
            details_resp = await client.get(details_url, params=details_params)
            details_resp.raise_for_status()
            return details_resp.json().get("result", {})
            
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return {"error": str(e)}

async def fetch_menu_from_search(restaurant_name: str) -> str:
    """
    Searches for menu or food reviews using Google Custom Search API.
    Returns a concatenated string of snippets.
    """
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        return "Google Search API not configured."

    async with httpx.AsyncClient() as client:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": f"{restaurant_name} 菜單 食記 推薦",
            "num": 5
        }
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            snippets = []
            if "items" in data:
                for item in data["items"]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    snippets.append(f"Title: {title}\nSnippet: {snippet}\n")
            
            return "\n".join(snippets) if snippets else "No menu information found."
            
        except Exception as e:
            print(f"Error fetching menu from search: {e}")
            return f"Error fetching menu: {str(e)}"

async def fetch_place_autocomplete(input_text: str) -> list:
    """
    Fetches place autocomplete suggestions from Google Places API.
    """
    if not GOOGLE_API_KEY:
        return []

    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": input_text,
            "key": GOOGLE_API_KEY,
            "language": "zh-TW",
            "types": "establishment"  # Limit to businesses
        }
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            suggestions = []
            if "predictions" in data:
                for prediction in data["predictions"]:
                    suggestions.append({
                        "description": prediction["description"],
                        "place_id": prediction["place_id"],
                        "main_text": prediction["structured_formatting"]["main_text"],
                        "secondary_text": prediction["structured_formatting"].get("secondary_text", "")
                    })
            return suggestions
            
        except Exception as e:
            print(f"Error fetching autocomplete suggestions: {e}")
            return []
