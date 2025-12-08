"""
V2 Recommendation API Endpoint
Implements two-stage recommendation: Hard Filter + Soft Ranking
"""

from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from typing import List, Optional

from schemas.recommendation import UserInputV2, RecommendationResponseV2, MenuItemV2
from schemas.restaurant_profile import RestaurantProfile
from agent.recommendation import RecommendationService
from services import firestore_service
from services.pipeline.orchestrator import RestaurantPipeline
from schemas.pipeline import PipelineInput
from services.job_manager import job_manager, JobStatus

router = APIRouter()

from services.restaurant_service import RestaurantService
from services.mock_service import MockService

# Note: get_or_create_profile is now handled by RestaurantService

async def process_recommendation_logic(user_input: UserInputV2) -> RecommendationResponseV2:
    """Core recommendation logic"""
    print(f"[RecommendAPI] Processing recommendation for: {user_input.restaurant_name}")
    
    # Mock handling for tests to bypass external services
    if user_input.place_id == 'mock-place-id':
         return MockService.get_mock_recommendation(user_input.restaurant_name)

    # Get profile using Service Layer
    profile = await RestaurantService.get_or_create_profile(user_input.restaurant_name, user_input.place_id)
    
    # Check if profile has menu items
    if not profile.menu_items:
        raise ValueError(f"Restaurant '{profile.name}' has no menu items available.")

    # Run recommendation service
    recommendation_service = RecommendationService()
    recommendations = await recommendation_service.generate_recommendation(
        user_input=user_input,
        profile=profile
    )
    
    return recommendations

async def process_recommendation_job(job_id: str, user_input: UserInputV2):
    """Background task for async recommendation with progress updates"""
    try:
        # Stage 1: Start (10%)
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=10, message="正在搜尋餐廳資料...")
        
        # Mock handling for tests
        if user_input.place_id == 'mock-place-id':
            recommendations = MockService.get_mock_recommendation(user_input.restaurant_name)
            job_manager.update_status(job_id, JobStatus.COMPLETED, progress=100, message="推薦生成完成", result=recommendations.model_dump(mode='json'))
            return
        
        # Stage 2: Get profile (20-60% for cold start, or quick jump for warm start)
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=15, message="正在檢查餐廳資料...")
        
        # Pass job_id for progress updates during cold start
        profile = await RestaurantService.get_or_create_profile(
            user_input.restaurant_name, 
            user_input.place_id,
            job_id=job_id  # Pass job_id for progress updates
        )
        
        if not profile.menu_items:
            raise ValueError(f"Restaurant '{profile.name}' has no menu items available.")
        
        # Stage 3: Analyze menu (65%)
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=65, message="正在分析菜單內容...")
        
        # Stage 4: Generate recommendation (75%)
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=75, message="AI 正在計算最佳推薦...")
        
        recommendation_service = RecommendationService()
        recommendations = await recommendation_service.generate_recommendation(
            user_input=user_input,
            profile=profile
        )
        
        # Stage 5: Finalize (90%)
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=90, message="正在組合完美菜單...")
        
        # Override recommendation_id with job_id
        recommendations.recommendation_id = job_id
        result_dict = recommendations.model_dump(mode='json')
        
        # Complete (100%)
        job_manager.update_status(
            job_id, 
            JobStatus.COMPLETED, 
            progress=100, 
            message="推薦生成完成！", 
            result=result_dict
        )
        
    except Exception as e:
        print(f"[JobWorker] Job {job_id} failed: {e}")
        job_manager.update_status(
            job_id, 
            JobStatus.FAILED, 
            error=str(e)
        )


@router.post("/recommend/v2", response_model=RecommendationResponseV2)
async def recommend_dishes_v2(user_input: UserInputV2):
    """Synchronous V2 Recommendation API"""
    try:
        return await process_recommendation_logic(user_input)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"[RecommendAPI] Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")

@router.post("/recommend/v2/async")
async def recommend_dishes_v2_async(user_input: UserInputV2, background_tasks: BackgroundTasks):
    """Asynchronous V2 Recommendation API"""
    try:
        # Create job
        job_id = job_manager.create_job(user_input.model_dump(mode='json'))
        
        # Start background task
        background_tasks.add_task(process_recommendation_job, job_id, user_input)
        
        return {"job_id": job_id, "status": "pending", "message": "Recommendation job started"}
        
    except Exception as e:
        print(f"[RecommendAPI] Async start error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to start job: {str(e)}")

@router.get("/recommend/v2/status/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a recommendation job"""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    return job

@router.get("/recommend/v2/alternatives", response_model=List[MenuItemV2])
async def get_alternatives(
    recommendation_id: str = Query(..., description="Job ID / Recommendation ID"),
    category: str = Query(...),
    exclude: List[str] = Query(default=[])
):
    """Get alternative dishes for a category"""
    
    # 1. Look up job to get context (place_id)
    job = job_manager.get_job(recommendation_id)
    
    place_id = None
    restaurant_name = None
    
    if job and "user_input" in job:
        user_input_data = job["user_input"]
        place_id = user_input_data.get("place_id")
        restaurant_name = user_input_data.get("restaurant_name")
    
    if not place_id and not restaurant_name:
        # If we can't find context, return empty list
        print(f"[RecommendAPI] Alternatives: Context not found for rec_id {recommendation_id}")
        return []
        
    # 2. Get profile
    try:
        profile = await RestaurantService.get_or_create_profile(restaurant_name, place_id)
    except Exception as e:
        print(f"[RecommendAPI] Alternatives: Failed to get profile: {e}")
        return []
    
    # 3. Get alternatives
    service = RecommendationService()
    return service.get_alternatives(category, exclude, profile)

@router.get("/recommend/v2/health")
async def health_check():
    """Health check endpoint for V2 recommendation system"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "version": "v2",
            "features": {
                "hard_filter": True,
                "soft_ranking": True,
                "llm_model": "gemini-1.5-flash",
                "async_support": True
            }
        }
    )

    return job

@router.post("/recommend/v2/prefetch", status_code=202)
async def prefetch_restaurant(
    restaurant_name: str = Query(..., description="Restaurant name"),
    place_id: Optional[str] = Query(None, description="Google Place ID"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Prefetch restaurant data to speed up future recommendations.
    
    This endpoint triggers Cold Start in the background if the restaurant
    is not in cache, without blocking the frontend.
    """
    try:
        # Check if already in cache
        from services import firestore_service
        if place_id:
            cached_profile = firestore_service.get_restaurant_profile(place_id)
            if cached_profile:
                return {"status": "cached", "message": f"{restaurant_name} is already in cache"}
        
        # Trigger background pipeline
        async def prefetch_task():
            try:
                print(f"[Prefetch] Starting background Cold Start for: {restaurant_name}")
                from services.restaurant_service import RestaurantService
                await RestaurantService.get_or_create_profile(restaurant_name, place_id)
                print(f"[Prefetch] Completed for: {restaurant_name}")
            except Exception as e:
                print(f"[Prefetch] Failed for {restaurant_name}: {e}")
                # Don't raise - this is background, failure is OK
        
        background_tasks.add_task(prefetch_task)
        
        return {
            "status": "prefetching",
            "message": f"Started background prefetch for {restaurant_name}"
        }
        
    except Exception as e:
        print(f"[Prefetch] Error: {e}")
        return {"status": "error", "message": str(e)}

# --- Finalize Order API (Moved from main.py) ---
from schemas.tracking import FinalizeRequest, FinalizeResponse
import uuid

@router.post("/recommend/v2/{recommendation_id}/finalize", response_model=FinalizeResponse)
async def finalize_order(recommendation_id: str, request: FinalizeRequest):
    """
    Records the final order selection.
    """
    print(f"[Tracking] Finalizing order for recommendation: {recommendation_id}")
    print(f"  - Total Price: {request.total_price}")
    print(f"  - Selections: {len(request.final_selections)} items")
    
    return FinalizeResponse(
        status="success",
        message="Order finalized successfully",
        order_id=str(uuid.uuid4()),
        summary={
            "total_price": request.total_price,
            "item_count": len(request.final_selections)
        }
    )
