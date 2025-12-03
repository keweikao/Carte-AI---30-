"""
V2 Recommendation API Endpoint
Implements two-stage recommendation: Hard Filter + Soft Ranking
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from schemas.recommendation import UserInputV2, RecommendationResponseV2
from schemas.restaurant_profile import RestaurantProfile
from agent.recommendation import RecommendationService
from services import firestore_service
from services.pipeline.orchestrator import RestaurantPipeline
from schemas.pipeline import PipelineInput

router = APIRouter()


@router.post("/recommend/v2", response_model=RecommendationResponseV2)
async def recommend_dishes_v2(user_input: UserInputV2):
    """
    V2 Recommendation API - Two-stage recommendation system

    Workflow:
    1. Fetch restaurant profile from Firestore
    2. Hard Filter: Remove dishes that violate constraints
    3. Soft Ranking: AI-powered ranking based on context

    Args:
        user_input: UserInputV2 with dining preferences

    Returns:
        RecommendationResponseV2 with ranked dish recommendations
    """
    try:
        print(f"[RecommendAPI] V2 recommendation request for: {user_input.restaurant_name}")

        # Step 1: Fetch restaurant profile
        # Try to get by place_id first
        if user_input.place_id:
            profile_data = firestore_service.get_restaurant_profile(user_input.place_id)
        else:
            # No place_id provided, will trigger Cold Start/Pipeline lookup
            print(f"[RecommendAPI] No place_id provided for: {user_input.restaurant_name}. Proceeding to Cold Start.")
            profile_data = None

        if not profile_data:
            print(f"[RecommendAPI] Restaurant not found in DB. Triggering Cold Start for: {user_input.restaurant_name}")
            try:
                pipeline = RestaurantPipeline()
                pipeline_input = PipelineInput(
                    restaurant_name=user_input.restaurant_name,
                    place_id=user_input.place_id
                )
                # Run pipeline (this takes time, e.g. 60-90s)
                profile = await pipeline.process(pipeline_input)
                
                if not profile:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Failed to generate profile for '{user_input.restaurant_name}'"
                    )
                
                # Profile is already saved to Firestore by the pipeline
                print(f"[RecommendAPI] Cold Start complete. Profile generated.")
                
            except Exception as e:
                print(f"[RecommendAPI] Cold Start failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Cold Start failed: {str(e)}"
                )
        else:
            profile = profile_data

        # Check if profile has menu items
        if not profile.menu_items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restaurant '{profile.name}' has no menu items available."
            )

        # Check if menu items have analysis data (DishAttributes)
        items_with_analysis = [item for item in profile.menu_items if item.analysis]
        if not items_with_analysis:
            print(f"[RecommendAPI] Warning: No items have analysis data. Recommendations may be limited.")
            # Continue anyway - the RecommendationService will filter out items without analysis

        # Step 2 & 3: Run two-stage recommendation
        recommendation_service = RecommendationService()
        recommendations = await recommendation_service.generate_recommendation(
            user_input=user_input,
            profile=profile
        )

        print(f"[RecommendAPI] Generated {len(recommendations.items)} recommendations")
        return recommendations

    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        print(f"[RecommendAPI] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


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
                "llm_model": "gemini-1.5-flash"
            }
        }
    )
