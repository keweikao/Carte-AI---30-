import asyncio
import os
from dotenv import load_dotenv
from agent.agents import SearchAgent, AggregationAgent, AgentResult

load_dotenv()

async def test_search_agent():
    print("Testing SearchAgent...")
    agent = SearchAgent()
    try:
        # Test with a known restaurant
        result = await agent.run("鼎泰豐")
        print(f"Search Result Confidence: {result.confidence}")
        print(f"Search Result Data: {result.data[:2]}") # Print first 2 items
        return result
    except Exception as e:
        print(f"SearchAgent Failed: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_aggregation_agent(search_result):
    print("\nTesting AggregationAgent...")
    agent = AggregationAgent()
    
    # Mock other results
    visual_result = AgentResult(source="visual", data=[{"dish_name": "小籠包", "price": 250}], confidence=0.9)
    review_result = AgentResult(source="review", data=[{"dish_name": "小籠包", "popularity_score": 10}], confidence=0.8)
    
    results = [visual_result, review_result]
    if search_result:
        results.append(search_result)
        
    try:
        final_list = await agent.run(results)
        print(f"Aggregation Result Count: {len(final_list)}")
        print(f"Top 3 Items: {final_list[:3]}")
    except Exception as e:
        print(f"AggregationAgent Failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    search_res = await test_search_agent()
    await test_aggregation_agent(search_res)

if __name__ == "__main__":
    asyncio.run(main())
