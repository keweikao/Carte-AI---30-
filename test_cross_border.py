import asyncio
import os
from dotenv import load_dotenv
from services.pipeline.providers import WebSearchProvider

# Load environment variables
load_dotenv()

async def test_cross_border_search():
    print("=== Testing Cross-Border Search ===")
    
    provider = WebSearchProvider()
    
    # Test Case 1: Japan Restaurant
    japan_restaurant = "AFURI 原宿"
    print(f"\n[Test] Searching for Japan restaurant: {japan_restaurant}")
    result_jp = await provider.search_and_fetch(japan_restaurant)
    
    if result_jp:
        print(f"✓ Found menu URL: {result_jp.source_url}")
        print(f"✓ Content length: {len(result_jp.text_content)} chars")
        if "tabelog" in result_jp.source_url or "afuri" in result_jp.source_url:
             print("✓ URL matches expected domain (tabelog/afuri)")
    else:
        print("✗ Failed to find menu for Japan restaurant")

    # Test Case 2: Taiwan Restaurant
    taiwan_restaurant = "鼎泰豐 信義店"
    print(f"\n[Test] Searching for Taiwan restaurant: {taiwan_restaurant}")
    result_tw = await provider.search_and_fetch(taiwan_restaurant)
    
    if result_tw:
        print(f"✓ Found menu URL: {result_tw.source_url}")
        print(f"✓ Content length: {len(result_tw.text_content)} chars")
        if "dintaifung" in result_tw.source_url or "ubereats" in result_tw.source_url or "facebook" in result_tw.source_url:
             print("✓ URL matches expected domain")
    else:
        print("✗ Failed to find menu for Taiwan restaurant")

if __name__ == "__main__":
    asyncio.run(test_cross_border_search())
