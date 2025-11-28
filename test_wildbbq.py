import asyncio
import os
import json
from dotenv import load_dotenv
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from agent.agents import SearchAgent, ReviewAgent, AggregationAgent

load_dotenv()

async def debug_wildbbq():
    restaurant_name = "路邊烤肉wildbbq 羅東"
    print(f"Debugging data for: {restaurant_name}")

    # 1. Fetch Place Details (Reviews & Photos)
    print("Fetching Place Details...")
    reviews_data = await fetch_place_details(restaurant_name)
    if "error" in reviews_data:
        print(f"Error fetching details: {reviews_data['error']}")
        return

    print(f"Place Name: {reviews_data.get('name')}")
    print(f"Rating: {reviews_data.get('rating')}")
    print(f"Total Reviews: {len(reviews_data.get('reviews', []))}")
    
    # 2. Run Search Agent
    print("\nRunning Search Agent...")
    search_agent = SearchAgent()
    search_result = await search_agent.run(restaurant_name)
    print(f"Search Confidence: {search_result.confidence}")
    print("Search Data (Top 3):")
    for item in search_result.data[:3]:
        print(f"- {item}")

    # 3. Run Review Agent
    print("\nRunning Review Agent...")
    review_agent = ReviewAgent()
    review_result = await review_agent.run(reviews_data)
    print("Review Data (Top 3):")
    for item in review_result.data[:3]:
        print(f"- {item}")

    # 4. Run Aggregation Agent
    print("\nRunning Aggregation Agent...")
    aggregator = AggregationAgent()
    # Mock visual result for now as we can't easily debug visual here without cost
    from agent.agents import AgentResult
    visual_result = AgentResult(source="visual", data=[], confidence=0.0) 
    
    results = [visual_result, review_result, search_result]
    final_candidates = await aggregator.run(results)
    
    print("\nFinal Aggregated Candidates (Top 5):")
    for item in final_candidates[:5]:
        print(f"- {item['dish_name']} ({item['status']}): {item['reason']}")

if __name__ == "__main__":
    asyncio.run(debug_wildbbq())
