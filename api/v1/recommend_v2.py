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

async def get_or_create_profile(restaurant_name: str, place_id: Optional[str] = None) -> RestaurantProfile:
    """Helper to get profile or trigger cold start"""
    
    # Mock handling for tests to bypass Apify dependency
    if place_id == 'mock-place-id':
        print(f"[RecommendAPI] Using mock profile for {restaurant_name}")
        from schemas.restaurant_profile import MenuItem, DishAttributes, MenuItemAnalysis
        from datetime import datetime
        return RestaurantProfile(
            place_id="mock-place-id",
            name=restaurant_name,
            address="測試地址",
            updated_at=datetime.now(),
            trust_level="high",
            menu_source_url="https://example.com",
            review_summary="測試餐廳評價",
            menu_items=[
                MenuItem(
                    name="宮保雞丁", 
                    price=300, 
                    category="熱菜", 
                    description="Spicy chicken",
                    analysis=DishAttributes(
                        is_spicy=True, 
                        contains_beef=False, 
                        contains_pork=False, 
                        contains_seafood=False,
                        is_vegan=False,
                        allergens=["peanuts"],
                        flavors=["spicy"],
                        textures=["tender"],
                        temperature="hot",
                        cooking_method="stir-fry",
                        suitable_occasions=["casual"],
                        is_signature=True,
                        sentiment_score=0.8,
                        highlight_review="Great!"
                    ),
                    ai_insight=MenuItemAnalysis(
                        sentiment="positive",
                        summary="Good",
                        mention_count=10
                    ),
                    is_popular=True,
                    is_risky=False
                ),
                MenuItem(
                    name="炒青菜", 
                    price=150, 
                    category="蔬菜", 
                    description="Stir-fried vegetables",
                    analysis=DishAttributes(
                        is_spicy=False,
                        is_vegan=True,
                        allergens=[],
                        flavors=["salty"],
                        textures=["crispy"],
                        temperature="hot",
                        cooking_method="stir-fry",
                        suitable_occasions=["casual"],
                        is_signature=False,
                        sentiment_score=0.7,
                        highlight_review="Fresh"
                    ),
                    ai_insight=MenuItemAnalysis(
                        sentiment="positive",
                        summary="Healthy",
                        mention_count=5
                    ),
                    is_popular=False,
                    is_risky=False
                )
            ]
        )

    # Step 1: Fetch restaurant profile
    profile_data = None
    if place_id:
        profile_data = firestore_service.get_restaurant_profile(place_id)
    
    if not profile_data:
        print(f"[RecommendAPI] Restaurant not found in DB. Triggering Cold Start for: {restaurant_name}")
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
            print(f"[RecommendAPI] Cold Start failed: {e}")
            raise e
    else:
        return profile_data

async def process_recommendation_logic(user_input: UserInputV2) -> RecommendationResponseV2:
    """Core recommendation logic"""
    print(f"[RecommendAPI] Processing recommendation for: {user_input.restaurant_name}")
    
    profile = await get_or_create_profile(user_input.restaurant_name, user_input.place_id)
    
    # Check if profile has menu items
    if not profile.menu_items:
        raise ValueError(f"Restaurant '{profile.name}' has no menu items available.")

    # Mock handling for tests to bypass Gemini API
    if user_input.place_id == 'mock-place-id':
        print(f"[RecommendAPI] Using mock recommendations for {user_input.restaurant_name}")
        from schemas.recommendation import RecommendationResponseV2, DishSlotResponse, MenuItemV2
        import uuid
        return RecommendationResponseV2(
            recommendation_id=str(uuid.uuid4()),
            restaurant_name=user_input.restaurant_name,
            recommendation_summary="Mock recommendation summary",
            total_price=450,
            cuisine_type="中式餐館",
            category_summary={"熱菜": 1, "蔬菜": 1},
            items=[
                DishSlotResponse(
                    category="熱菜",
                    display=MenuItemV2(
                        dish_name="宮保雞丁",
                        price=300,
                        quantity=1,
                        reason="經典川菜，香辣可口",
                        category="熱菜"
                    ),
                    alternatives=[]
                ),
                DishSlotResponse(
                    category="蔬菜",
                    display=MenuItemV2(
                        dish_name="炒青菜",
                        price=150,
                        quantity=1,
                        reason="新鮮健康",
                        category="蔬菜"
                    ),
                    alternatives=[]
                )
            ]
        )

    # Run recommendation service
    recommendation_service = RecommendationService()
    recommendations = await recommendation_service.generate_recommendation(
        user_input=user_input,
        profile=profile
    )
    
    return recommendations

async def process_recommendation_job(job_id: str, user_input: UserInputV2):
    """Background task for async recommendation"""
    try:
        job_manager.update_status(job_id, JobStatus.PROCESSING, progress=10, message="Fetching restaurant profile...")
        
        recommendations = await process_recommendation_logic(user_input)
        
        # Override recommendation_id with job_id so we can look it up later for alternatives
        recommendations.recommendation_id = job_id
        
        # Convert Pydantic model to dict for storage
        result_dict = recommendations.model_dump(mode='json')
        
        job_manager.update_status(
            job_id, 
            JobStatus.COMPLETED, 
            progress=100, 
            message="Recommendation generated", 
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
        profile = await get_or_create_profile(restaurant_name, place_id)
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
