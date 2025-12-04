from typing import Optional
from schemas.restaurant_profile import RestaurantProfile
from services import firestore_service
from services.pipeline.orchestrator import RestaurantPipeline
from schemas.pipeline import PipelineInput
from services.mock_service import MockService

class RestaurantService:
    @staticmethod
    async def get_or_create_profile(restaurant_name: str, place_id: Optional[str] = None) -> RestaurantProfile:
        """
        Retrieves a restaurant profile from DB or triggers a cold start pipeline.
        """
        
        # Mock handling
        if place_id == 'mock-place-id':
            return MockService.get_mock_profile(restaurant_name)

        # Step 1: Fetch from DB
        profile_data = None
        if place_id:
            profile_data = firestore_service.get_restaurant_profile(place_id)
        
        if not profile_data:
            print(f"[RestaurantService] Profile not found in DB. Triggering Cold Start for: {restaurant_name}")
            try:
                pipeline = RestaurantPipeline()
                pipeline_input = PipelineInput(
                    restaurant_name=restaurant_name,
                    place_id=place_id
                )
                # Run pipeline (this takes time, e.g. 60-90s)
                profile = await pipeline.process(pipeline_input)
                
                if not profile:
                    raise ValueError(f"Failed to generate profile for '{restaurant_name}'")
                
                return profile
                
            except Exception as e:
                print(f"[RestaurantService] Cold Start failed: {e}")
                raise e
        else:
            return profile_data
