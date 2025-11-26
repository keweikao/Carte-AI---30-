#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import uuid
from fastapi.testclient import TestClient

# Patch Firestore before anything else is imported to prevent real connection attempts.
# This ensures that when 'main' and 'services.firestore_service' are loaded,
# they use a mock client instead of trying to establish a real connection.
firestore_patch = patch('google.cloud.firestore.Client', new_callable=MagicMock)
mock_firestore_client = firestore_patch.start()

# Now that Firestore is patched, we can safely import our application modules.
from main import app, get_current_user
from schemas.recommendation import RecommendationResponseV2, DishSlotResponse, MenuItemV2

# --- Mock Data ---

FAKE_USER = {"email": "test@example.com", "name": "Test User", "sub": "12345"}
FAKE_REC_ID = str(uuid.uuid4())

MOCK_AGENT_RESPONSE = RecommendationResponseV2(
    recommendation_summary="為您精心挑選以下 2 道菜",
    items=[
        DishSlotResponse(
            category="熱菜",
            display=MenuItemV2(dish_name="宮保雞丁", price=250, reason="招牌菜", category="熱菜"),
            alternatives=[
                MenuItemV2(dish_name="左宗棠雞", price=260, reason="口味相似", category="熱菜"),
                MenuItemV2(dish_name="辣子雞丁", price=270, reason="經典川菜", category="熱菜"),
            ]
        ),
        DishSlotResponse(
            category="主食",
            display=MenuItemV2(dish_name="蛋炒飯", price=120, reason="填飽肚子", category="主食"),
            alternatives=[]
        )
    ],
    total_price=370,
    nutritional_balance_note="葷素搭配",
    recommendation_id=FAKE_REC_ID,
    restaurant_name="測試餐廳",
    user_info=FAKE_USER,
    cuisine_type="中式餐館",
    category_summary={"熱菜": 1, "主食": 1}
)

MOCK_CANDIDATE_POOL = {
    "recommendation_id": FAKE_REC_ID,
    "cuisine_type": "中式餐館",
    "candidates": [
        {"dish_name": "宮保雞丁", "price": 250, "reason": "招牌菜", "category": "熱菜"},
        {"dish_name": "左宗棠雞", "price": 260, "reason": "口味相似", "category": "熱菜"},
        {"dish_name": "辣子雞丁", "price": 270, "reason": "經典川菜", "category": "熱菜"},
        {"dish_name": "魚香肉絲", "price": 240, "reason": "另一選擇", "category": "熱菜"},
        {"dish_name": "蛋炒飯", "price": 120, "reason": "填飽肚子", "category": "主食"},
        {"dish_name": "揚州炒飯", "price": 150, "reason": "廣受好評", "category": "主食"},
    ]
}


class TestUXv3API(unittest.TestCase):
    
    def setUp(self):
        """Set up the test client and override auth before each test."""
        self.client = TestClient(app)
        self.original_overrides = app.dependency_overrides.copy()
        app.dependency_overrides[get_current_user] = lambda: FAKE_USER

    def tearDown(self):
        """Restore original dependency overrides after each test."""
        app.dependency_overrides = self.original_overrides

    @patch('agent.dining_agent.get_cached_data', return_value=None)
    @patch('agent.dining_agent.get_user_profile', return_value={"user_info": FAKE_USER})
    @patch('agent.dining_agent.fetch_place_details', new_callable=AsyncMock, return_value=({"reviews": "..."},))
    @patch('agent.dining_agent.fetch_menu_from_search', new_callable=AsyncMock, return_value=("menu text",))
    @patch('google.generativeai.GenerativeModel.generate_content')
    @patch('main.create_recommendation_session', return_value=True)
    @patch('agent.dining_agent.save_recommendation_candidates', return_value=True)
    def test_01_get_recommendations_v3_format(
        self, 
        mock_save_candidates, 
        mock_create_session, 
        mock_gemini_call,
        mock_fetch_menu,
        mock_fetch_details,
        mock_get_profile,
        mock_get_cache
    ):
        """
        Tests the POST /v2/recommendations endpoint with deep mocking to ensure internal logic is executed.
        """
        import json
        print("\n🧪 Testing POST /v2/recommendations with V3 format (deep mock)...")

        # --- Setup Mocks ---
        mock_gemini_response = MagicMock()
        llm_output_data = {
            "cuisine_type": "中式餐館",
            "menu_items": MOCK_CANDIDATE_POOL["candidates"]
        }
        mock_gemini_response.text = json.dumps(llm_output_data)
        mock_gemini_call.return_value = mock_gemini_response
        
        # --- Make Request ---
        # Set a specific dish_count_target to make the test predictable
        request_payload = {
            "restaurant_name": "測試餐廳", 
            "dining_style": "Shared", 
            "party_size": 2, 
            "budget": {"type": "Total", "amount": 1200},
            "dish_count_target": 2 
        }
        response = self.client.post("/v2/recommendations", json=request_payload, headers={"Authorization": "Bearer fake-token"})
        
        # --- Assertions ---
        self.assertEqual(response.status_code, 200)

        # Check that external and expensive calls were made
        mock_get_cache.assert_called_once()
        mock_get_profile.assert_called_once()
        mock_fetch_menu.assert_awaited_once()
        mock_fetch_details.assert_awaited_once()
        mock_gemini_call.assert_called_once()

        # Check response structure based on our processing of the mocked LLM output
        response_data = response.json()
        self.assertIn("items", response_data)
        self.assertEqual(len(response_data["items"]), 2) # Based on dish_count_target
        
        # The selection logic is simple (sorted by category), so we expect "熱菜" then "主食"
        self.assertEqual(response_data["items"][0]["display"]["dish_name"], "宮保雞丁")
        self.assertEqual(response_data["items"][1]["display"]["dish_name"], "蛋炒飯")
        
        # Check that the candidate pool was saved
        mock_save_candidates.assert_called_once()
        args, kwargs = mock_save_candidates.call_args
        self.assertEqual(len(args), 3) # recommendation_id, candidates_data, cuisine_type
        self.assertEqual(args[2], "中式餐館") # cuisine_type from LLM output
        self.assertEqual(len(args[1]), len(MOCK_CANDIDATE_POOL["candidates"])) # The full raw list

        # Check that the user session was created
        mock_create_session.assert_called_once()

        print("✅ Test Passed: /v2/recommendations with deep mocking.")

    @patch('main.get_recommendation_candidates', return_value=MOCK_CANDIDATE_POOL)
    def test_02_get_alternatives_endpoint(self, mock_get_candidates):
        """
        Tests the GET /v2/recommendations/alternatives endpoint.
        """
        print("\n🧪 Testing GET /v2/recommendations/alternatives...")

        print("  - Case 1: Getting alternatives for '熱菜'")
        params = {"recommendation_id": FAKE_REC_ID, "category": "熱菜", "exclude": ["宮保雞丁"]}
        response = self.client.get("/v2/recommendations/alternatives", params=params, headers={"Authorization": "Bearer fake-token"})
        
        self.assertEqual(response.status_code, 200)
        mock_get_candidates.assert_called_once_with(FAKE_REC_ID)
        
        response_data = response.json()
        print("  Response JSON for '熱菜':", response_data)
        
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data)
, 3)
        
        response_dish_names = {item["dish_name"] for item in response_data}
        self.assertEqual(response_dish_names, {"左宗棠雞", "辣子雞丁", "魚香肉絲"})

        print("\n  - Case 2: Getting alternatives for '主食' with multiple exclusions")
        params = {"recommendation_id": FAKE_REC_ID, "category": "主食", "exclude": ["蛋炒飯", "揚州炒飯"]}
        response = self.client.get("/v2/recommendations/alternatives", params=params, headers={"Authorization": "Bearer fake-token"})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        print("  Response JSON for '主食':", response_data)
        self.assertEqual(response_data, [])

        print("\n  - Case 3: Recommendation ID not found")
        mock_get_candidates.return_value = None
        params = {"recommendation_id": "non_existent_id", "category": "熱菜", "exclude": ["宮保雞丁"]}
        response = self.client.get("/v2/recommendations/alternatives", params=params, headers={"Authorization": "Bearer fake-token"})
        self.assertEqual(response.status_code, 404)

        print("✅ Test Passed: /v2/recommendations/alternatives works as expected.")


if __name__ == "__main__":
    try:
        print("Initializing test environment with 'unittest'...")
        unittest.main()
    finally:
        # Stop the global patch after all tests in the file have run.
        firestore_patch.stop()
        print("\nTest environment shut down.")