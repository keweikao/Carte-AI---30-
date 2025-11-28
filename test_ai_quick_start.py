
import sys
import os

# Ensure the current directory is in the python path
sys.path.append(os.getcwd())

from ai_dining_agent import DiningAgent

def test_quick_start():
    print("🚀 Starting Quick Start Automated Test...")

    # Initialize DiningAgent with some dummy data
    agent = DiningAgent(
        restaurant_name="鼎泰豐",
        total_budget=2000,
        mode="sharing",
        tags=["不吃辣"],
        note="家庭聚餐"
    )

    print("\n🏃 Running DiningAgent...")
    # Execute the agent
    result = agent.run()

    print("\n📊 Checking Optimization Stats (as per quick_start_for_ai.md)...")
    
    # Check Token Optimization Stats
    token_stats = result.get('token_optimization_stats')
    print(f"Token Optimization Stats: {token_stats}")
    
    # Check API Cache Stats
    api_stats = result.get('api_cache_stats')
    print(f"API Cache Stats: {api_stats}")

    # Validation
    if token_stats and api_stats:
        print("\n✅ Test Passed: Optimization stats are present.")
    else:
        print("\n❌ Test Failed: Missing optimization stats.")
        sys.exit(1)

if __name__ == "__main__":
    test_quick_start()
