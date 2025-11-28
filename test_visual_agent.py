import asyncio
import os
from dotenv import load_dotenv
from agent.agents import VisualAgent
from agent.data_fetcher import fetch_place_details

load_dotenv()

async def test_visual_agent():
    print("Testing VisualAgent with real data...")
    
    # 1. Fetch real photos from a known place (Din Tai Fung Xinyi)
    # We need a place that definitely has menu photos or food photos
    restaurant_name = "鼎泰豐 信義店"
    print(f"Fetching details for {restaurant_name}...")
    
    details = await fetch_place_details(restaurant_name)
    
    if "error" in details:
        print(f"Failed to fetch place details: {details['error']}")
        return

    photos = details.get("photos", [])
    print(f"Found {len(photos)} photos.")
    
    if not photos:
        print("No photos found to test.")
        return

    # 2. Run VisualAgent
    agent = VisualAgent()
    try:
        print("Running VisualAgent (this calls Gemini Vision)...")
        result = await agent.run(photos)
        
        print(f"\nVisual Analysis Result:")
        print(f"Confidence: {result.confidence}")
        print(f"Items Found: {len(result.data)}")
        if result.data:
            print("First 3 items:")
            for item in result.data[:3]:
                print(f"- {item}")
        else:
            print("No items extracted. This might be because the top photos aren't menus.")
            
    except Exception as e:
        print(f"VisualAgent Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_visual_agent())
