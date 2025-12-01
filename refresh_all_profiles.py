import asyncio
import os
import json
from dotenv import load_dotenv
from google.cloud import firestore
from agent.agents import AggregationAgent, AgentResult

load_dotenv()

# Initialize Firestore
try:
    db = firestore.Client(database="carted-data")
except Exception as e:
    print(f"Error initializing client with database='carted-data': {e}")
    db = firestore.Client()

COLLECTION_NAME = "restaurants"

async def refresh_profile(doc):
    data = doc.to_dict()
    restaurant_name = data.get("name")
    place_id = data.get("place_id", doc.id)
    
    print(f"Processing {restaurant_name} ({place_id})...")
    
    agent_results_dict = data.get("agent_results")
    if not agent_results_dict:
        print(f"  ⚠️  No agent_results found for {restaurant_name}. Skipping.")
        return

    # Reconstruct AgentResult objects
    results = []
    for source, res_data in agent_results_dict.items():
        # Handle case where res_data might be a dict (serialized) or already an object (if local)
        if isinstance(res_data, dict):
            # Ensure 'metadata' is present, even if None
            metadata = res_data.get("metadata")
            # Handle 'blobs' in metadata which might be binary and problematic to pass if not needed
            # AggregationAgent doesn't use blobs, only text data usually.
            # But let's keep it safe.
            
            results.append(AgentResult(
                source=res_data.get("source", source),
                data=res_data.get("data", []),
                confidence=res_data.get("confidence", 0.0),
                metadata=metadata
            ))
        else:
            print(f"  ⚠️  Unexpected format for agent result: {type(res_data)}")

    if not results:
        print(f"  ⚠️  No valid agent results reconstructed for {restaurant_name}. Skipping.")
        return

    # Run AggregationAgent
    aggregator = AggregationAgent()
    try:
        print(f"  🔄 Running AggregationAgent...")
        final_profile = await aggregator.run(results)
        
        # Update Firestore
        # We need to update 'golden_profile'
        # final_profile is the list of dishes (consolidated_menu)
        
        # Wait, AggregationAgent.run returns a List[Dict], which IS the golden profile (consolidated menu) now.
        # But wait, let's check AggregationAgent.run return value in agent/agents.py
        # It returns 'final_pool' which is a list of dicts.
        
        # In profile_agent.py, 'golden_profile' is set to this return value.
        # So we just update 'golden_profile' field.
        
        doc.reference.update({
            "golden_profile": final_profile,
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        print(f"  ✅ Successfully updated Golden Profile for {restaurant_name} with {len(final_profile)} items.")
        
    except Exception as e:
        print(f"  ❌ Error running AggregationAgent for {restaurant_name}: {e}")

async def main():
    print("🚀 Starting Batch Refresh of Restaurant Profiles...")
    
    docs = db.collection(COLLECTION_NAME).stream()
    
    tasks = []
    for doc in docs:
        tasks.append(refresh_profile(doc))
    
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No documents found in 'restaurants' collection.")

    print("✨ Batch Refresh Complete.")

if __name__ == "__main__":
    asyncio.run(main())
