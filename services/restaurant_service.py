from typing import Optional
from schemas.restaurant_profile import RestaurantProfile
from services import firestore_service
from services.pipeline.orchestrator import RestaurantPipeline
from schemas.pipeline import PipelineInput
from services.mock_service import MockService

class RestaurantService:
    @staticmethod
    async def get_or_create_profile(
        restaurant_name: str, 
        place_id: Optional[str] = None,
        job_id: Optional[str] = None  # For progress updates
    ) -> RestaurantProfile:
        """
        Retrieves a restaurant profile from DB or triggers a cold start pipeline.
        
        Args:
            restaurant_name: Name of the restaurant
            place_id: Optional Google Place ID
            job_id: Optional job ID for progress updates during cold start
        """
        
        # Mock handling
        if place_id == 'mock-place-id':
            return MockService.get_mock_profile(restaurant_name)

        # Step 1: Fetch from DB (Warm Start check)
        profile_data = None
        if place_id:
            profile_data = firestore_service.get_restaurant_profile(place_id)
        
        if profile_data:
            # Warm Start - data already exists
            print(f"[RestaurantService] Warm Start: Profile found for {restaurant_name}")
            if job_id:
                # Quick update to 60% since we're skipping cold start
                from services.job_manager import job_manager, JobStatus
                job_manager.update_status(job_id, JobStatus.PROCESSING, progress=60, message="已找到餐廳資料...")
            return profile_data
        
        # Cold Start - need to run pipeline
        print(f"[RestaurantService] Cold Start: Profile not found. Triggering pipeline for: {restaurant_name}")
        
        try:
            if job_id:
                from services.job_manager import job_manager, JobStatus
                job_manager.update_status(job_id, JobStatus.PROCESSING, progress=20, message="正在搜尋餐廳菜單與評論...")
            
            pipeline = RestaurantPipeline()
            pipeline_input = PipelineInput(
                restaurant_name=restaurant_name,
                place_id=place_id
            )
            
            # Run pipeline with progress callback if job_id is provided
            if job_id:
                def progress_callback(step: int, message: str):
                    """Callback for pipeline progress updates"""
                    # Map pipeline steps to progress percentages (20-60%)
                    progress_map = {
                        1: (25, "正在搜尋餐廳菜單..."),
                        2: (35, "正在抓取餐廳評論..."),
                        3: (45, "正在解析菜單內容..."),
                        4: (55, "正在融合評論與菜單..."),
                    }
                    progress, msg = progress_map.get(step, (30, message))
                    job_manager.update_status(job_id, JobStatus.PROCESSING, progress=progress, message=msg)
                
                profile = await pipeline.process(pipeline_input, progress_callback=progress_callback)
            else:
                profile = await pipeline.process(pipeline_input)
            
            if not profile:
                raise ValueError(f"Failed to generate profile for '{restaurant_name}'")
            
            if job_id:
                job_manager.update_status(job_id, JobStatus.PROCESSING, progress=60, message="餐廳資料準備完成...")
            
            return profile
            
        except Exception as e:
            print(f"[RestaurantService] Cold Start failed: {e}")
            raise e

