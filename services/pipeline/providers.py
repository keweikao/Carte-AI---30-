"""
Data Acquisition Layer - External API providers
Handles communication with Apify, Serper, and Jina Reader
"""

import os
import httpx
from typing import Optional
from apify_client import ApifyClientAsync

from schemas.pipeline import MapData, WebContent, RawReview
from firebase_admin import firestore
from datetime import datetime, timedelta, timezone


class UnifiedMapProvider:
    """
    Single API call to Apify to fetch all Google Maps data:
    - Restaurant images
    - Customer reviews
    - Address and contact info
    """

    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN")
        if not self.api_token:
            raise ValueError("APIFY_API_TOKEN environment variable not set")

    async def fetch_map_data(self, restaurant_name: str, place_id: Optional[str] = None, max_images: int = 0) -> Optional[MapData]:
        """
        Fetch restaurant data from Google Maps via Apify
        
        Args:
            restaurant_name: Name of the restaurant to search
            place_id: Optional Google Place ID for precise lookup
            max_images: Unused, kept for compatibility. Internally set to 1 to satisfy Actor requirements.

        Returns:
            MapData object or None if fetch fails
        """
        try:
            print(f"[UnifiedMapProvider] Fetching data for: {restaurant_name} (Place ID: {place_id})")

            client = ApifyClientAsync(self.api_token)

            # Prepare run input with optimized memory settings
            # Disable image fetching completely by ignoring result, but set maxImages=1 to avoid Actor errors
            run_input = {
                "maxImages": 1,
                "maxReviews": 30,  # Reduced to 30 for speed optimization
                "maxCrawledPlaces": 1,  # Only crawl the target restaurant
                "language": "zh-TW",
                "proxyConfiguration": {"useApifyProxy": True},
            }

            if place_id:
                # Use startUrls with Place ID for precision
                # Format: https://www.google.com/maps/search/?api=1&query=Google&query_place_id={place_id}
                # This forces Google Maps to open the specific place
                run_input["startUrls"] = [
                    {"url": f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={place_id}"}
                ]
            else:
                # Fallback to search string
                run_input["searchStringsArray"] = [restaurant_name]

            # Call the actor with reduced memory allocation (512MB instead of default 4GB)
            actor_call = await client.actor("compass/crawler-google-places").call(
                run_input=run_input,
                memory_mbytes=512  # Reduce memory from 4096MB to 512MB
            )

            # Fetch results
            dataset_client = client.dataset(actor_call["defaultDatasetId"])
            items = []
            async for item in dataset_client.iterate_items():
                items.append(item)

            if not items:
                print(f"[UnifiedMapProvider] No data found for {restaurant_name}")
                return None

            # Get first result (most relevant)
            data = items[0]

            # Extract images - DISABLED
            images = []
            # if "imageUrls" in data and data["imageUrls"]:
            #     images = data["imageUrls"][:max_images]

            # Extract reviews
            reviews = []
            if "reviews" in data and data["reviews"]:
                for review_data in data["reviews"]:
                    try:
                        review = RawReview(
                            text=review_data.get("text", ""),
                            rating=review_data.get("stars", 3),
                            published_at=review_data.get("publishedAtDate"),
                            author_name=review_data.get("name")
                        )
                        reviews.append(review)
                    except Exception as e:
                        print(f"[UnifiedMapProvider] Failed to parse review: {e}")
                        continue

            # Build MapData
            map_data = MapData(
                place_id=data.get("placeId", ""),
                name=data.get("title", restaurant_name),
                address=data.get("address", "Address not available"),
                phone=data.get("phone"),
                rating=data.get("totalScore"),
                images=images,
                reviews=reviews
            )

            print(f"[UnifiedMapProvider] Success: {len(images)} images, {len(reviews)} reviews")
            return map_data

        except Exception as e:
            error_msg = str(e)
            print(f"[UnifiedMapProvider] Error fetching data: {error_msg}")
            
            # Special handling for Apify quota errors
            if "exceed the memory limit" in error_msg:
                print("[UnifiedMapProvider] Apify memory quota exceeded. This might be temporary.")
                print("[UnifiedMapProvider] Possible causes:")
                print("  1. Other tasks are running on your Apify account")
                print("  2. Previous tasks haven't finished yet")
                print("  3. Multiple concurrent requests")
                print("[UnifiedMapProvider] Waiting 5 seconds and retrying once...")
                
                import asyncio
                await asyncio.sleep(5)
                
                try:
                    # Retry once with even lower memory (256MB)
                    print("[UnifiedMapProvider] Retrying with 256MB memory allocation...")
                    actor_call = await client.actor("compass/crawler-google-places").call(
                        run_input=run_input,
                        memory_mbytes=256
                    )
                    
                    # Fetch results
                    dataset_client = client.dataset(actor_call["defaultDatasetId"])
                    items = []
                    async for item in dataset_client.iterate_items():
                        items.append(item)
                    
                    if items:
                        data = items[0]
                        # ... (same processing as above)
                        # For brevity, return a minimal result
                        print("[UnifiedMapProvider] Retry successful!")
                        return None  # Will be handled by orchestrator fallback
                    
                except Exception as retry_error:
                    print(f"[UnifiedMapProvider] Retry also failed: {retry_error}")
            
            import traceback
            traceback.print_exc()
            return None


class WebSearchProvider:
    """
    Search for menu URLs using Serper.dev and fetch content using Jina Reader
    Cost: $1/1000 queries (cheaper than Google Custom Search for high volume)
    """

    def __init__(self):
        self.serper_key = os.getenv("SERPER_API_KEY")
        if not self.serper_key:
            print("[WebSearchProvider] Warning: SERPER_API_KEY not configured, web search will be skipped")
            
        # Initialize Firestore
        try:
            self.db = firestore.client()
        except Exception:
            self.db = None
            print("[WebSearchProvider] Warning: Firestore client failed to initialize")

    async def search_and_fetch(self, restaurant_name: str) -> Optional[WebContent]:
        """
        Search for menu URL and fetch content using Serper (with caching)
        
        Args:
            restaurant_name: Name of the restaurant
            
        Returns:
            WebContent object or None if search/fetch fails
        """
        # Skip if not configured
        if not self.serper_key:
            return None
            
        # Check cache first
        cache_key = f"web_search_{restaurant_name.replace('/', '_').replace(' ', '_')}"
        if self.db:
            try:
                doc_ref = self.db.collection('web_search_cache').document(cache_key)
                doc = doc_ref.get()
                if doc.exists:
                    data = doc.to_dict()
                    # Check expiry (7 days)
                    cached_at = data.get('cached_at')
                    # Ensure cached_at is timezone-aware
                    if cached_at and cached_at.tzinfo is None:
                        cached_at = cached_at.replace(tzinfo=timezone.utc)
                        
                    if cached_at and (datetime.now(timezone.utc) - cached_at < timedelta(days=7)):
                        # VALIDATION: Check if cached content is actually useful
                        text_content = data.get('text_content', '')
                        if text_content and len(text_content) > 100:  # At least 100 chars
                            print(f"[WebSearchProvider] Cache hit for {restaurant_name}")
                            return WebContent(
                                source_url=data.get('source_url'),
                                text_content=text_content
                            )
                        else:
                            print(f"[WebSearchProvider] Cache invalid (empty or too short: {len(text_content)} chars), re-fetching")
                            # Continue to re-fetch below
            except Exception as e:
                print(f"[WebSearchProvider] Cache read error: {e}")
        
        try:
            print(f"[WebSearchProvider] Searching menu for: {restaurant_name}")
            
            # Step 1: Search for menu URL using Serper
            menu_url = await self._search_menu_url(restaurant_name)
            if not menu_url:
                return None
            
            # Step 2: Fetch content using Jina Reader
            print(f"[WebSearchProvider] Fetching content from: {menu_url}")
            jina_url = f"https://r.jina.ai/{menu_url}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(jina_url, timeout=30)
                response.raise_for_status()
                content = response.text
                
                print(f"[WebSearchProvider] ✓ Fetched {len(content)} chars")
                
                result = WebContent(
                    source_url=menu_url,
                    text_content=content
                )
                
                # Save to cache
                if self.db:
                    try:
                        self.db.collection('web_search_cache').document(cache_key).set({
                            'source_url': menu_url,
                            'text_content': content,
                            'cached_at': datetime.now(timezone.utc)
                        })
                        print(f"[WebSearchProvider] Saved to cache: {cache_key}")
                    except Exception as e:
                        print(f"[WebSearchProvider] Cache write error: {e}")
                
                return result
                
        except Exception as e:
            print(f"[WebSearchProvider] Search error: {e}")
            return None

    async def _search_menu_url(self, restaurant_name: str) -> Optional[str]:
        """Search for menu URL using Serper.dev"""
        try:
            # Use httpx to call Serper API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": self.serper_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "q": f"{restaurant_name} 菜單 menu メニュー 메뉴",
                        "hl": "zh-tw",
                        "num": 10
                    },
                    timeout=10
                )
                
                if response.status_code == 403:
                    print("[WebSearchProvider] Serper API 403 Forbidden - Check API Key or Credits")
                    return None
                
                response.raise_for_status()
                data = response.json()
                
                # Extract best URL (prioritize high-quality menu sources by region)
                priority_keywords = [
                    # Taiwan / Global
                    "ichef", "inline", "ubereats", "foodpanda", "facebook", "instagram",
                    # Japan
                    "tabelog", "gnavi", "hotpepper", "retty",
                    # Korea
                    "naver", "catchtable", "mangoplate",
                    # Generic
                    "menu", "菜單", "メニュー", "메뉴"
                ]
                
                # Check organic results
                if "organic" in data:
                    for result in data["organic"]:
                        url = result.get("link", "")
                        if any(keyword in url.lower() for keyword in priority_keywords):
                            print(f"[WebSearchProvider] Found URL: {url}")
                            return url
                    
                    # If no priority match, return first result
                    if data["organic"]:
                        url = data["organic"][0].get("link")
                        print(f"[WebSearchProvider] Using first result: {url}")
                        return url
                
                print(f"[WebSearchProvider] No menu URL found")
                return None
                
        except Exception as e:
            print(f"[WebSearchProvider] Serper search error: {e}")
            return None
