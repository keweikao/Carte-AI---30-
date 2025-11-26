from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.recommendation import UserInputV2, RecommendationResponseV2, RecommendationRequest, FullRecommendationResponse, MenuItemV2
from schemas.feedback import FeedbackRequest
from schemas.tracking import SwapRequest, SwapResponse, FinalizeRequest, FinalizeResponse
from agent.dining_agent import DiningAgent
from auth.google_auth import verify_google_token
from services.firestore_service import (
    update_user_profile,
    create_recommendation_session,
    get_recommendation_session,
    add_swap_to_session,
    finalize_recommendation_session,
    get_recommendation_candidates # New import
)
import uvicorn
import os
import uuid
from datetime import datetime

app = FastAPI(title="AI Dining Agent API", version="2.0")

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://dining-frontend-1045148759148.asia-east1.run.app",
        "https://dining-frontend-u33peegeaa-de.a.run.app",  # 新增自動生成的 URL
        "https://www.carte.tw"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return verify_google_token(token)

agent = DiningAgent()

@app.post("/v2/recommendations", response_model=RecommendationResponseV2)
async def get_recommendations_v2(
    request: UserInputV2,
    user_info: dict = Depends(get_current_user)
):
    """
    Generates dining recommendations using the V2 structured prompt.
    Requires a valid Google ID Token.
    """
    try:
        print(f"V2 Request from user: {user_info.get('email')}")
        user_id = user_info.get("sub")
        request.user_id = user_id

        response = await agent.get_recommendations_v2(request)

        # User info is already added in the agent method, but we can ensure it here if needed.
        response.user_info = {"email": user_info.get("email"), "name": user_info.get("name")}

        # Create recommendation session for tracking
        try:
            session_data = {
                "recommendation_id": response.recommendation_id,
                "user_id": user_id,
                "restaurant_name": response.restaurant_name,
                "restaurant_cuisine_type": response.cuisine_type,
                "user_input": request.dict(),
                "initial_recommendations": [slot.display.dict() for slot in response.items],
                "initial_total_price": response.total_price,
                "swap_history": [],
                "final_selections": None,
                "final_total_price": None,
                "created_at": datetime.now(),
                "finalized_at": None,
                "session_duration_seconds": None,
                "total_swap_count": 0
            }
            create_recommendation_session(session_data)
        except Exception as session_error:
            print(f"Warning: Failed to create session: {session_error}")
            # Don't fail the main request if session creation fails

        return response

    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unexpected error in /v2/recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.post("/recommendations", response_model=FullRecommendationResponse, deprecated=True)
async def get_recommendations_v1(
    request: RecommendationRequest,
    user_info: dict = Depends(get_current_user)
):
    """
    DEPRECATED: This endpoint is deprecated and will be removed in a future version.
    Please migrate to /v2/recommendations.
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="This endpoint is deprecated. Please use /v2/recommendations."
    )

@app.post("/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    user_info: dict = Depends(get_current_user)
):
    """Submits user feedback."""
    user_id = user_info.get("sub")
    if user_id:
        update_user_profile(user_id, feedback.dict())
    return {"status": "success", "message": "Feedback received"}


@app.get("/v2/recommendations/alternatives", response_model=List[MenuItemV2])
async def get_alternatives(
    recommendation_id: str,
    category: str,
    exclude: List[str] = Query(...),
    user_info: dict = Depends(get_current_user) # Ensures endpoint is protected
):
    """
    Retrieves alternative dishes for a specific category within a recommendation session.
    """
    candidate_data = get_recommendation_candidates(recommendation_id)
    if not candidate_data:
        raise HTTPException(
            status_code=404,
            detail=f"Recommendation session {recommendation_id} not found or has no candidates."
        )

    all_candidates = candidate_data.get("candidates", [])
    
    # Filter by category and exclude already seen/used dishes
    alternatives = [
        item for item in all_candidates
        if item.get("category") == category and item.get("dish_name") not in exclude
    ]
    
    # Convert dicts to MenuItemV2 objects
    try:
        validated_alternatives = [MenuItemV2.model_validate(alt) for alt in alternatives]
    except Exception as e:
        print(f"Error validating alternatives for {recommendation_id}: {e}")
        raise HTTPException(status_code=500, detail="Error processing alternative dishes.")

    return validated_alternatives


@app.post("/v2/recommendations/{recommendation_id}/swap", response_model=SwapResponse)
async def record_swap(
    recommendation_id: str,
    swap: SwapRequest,
    user_info: dict = Depends(get_current_user)
):
    """
    記錄換菜行為

    Args:
        recommendation_id: 推薦 ID
        swap: 換菜資料（原始菜品、新菜品）
    """
    user_id = user_info.get("sub")

    # 驗證 recommendation_id 是否一致
    if swap.recommendation_id != recommendation_id:
        raise HTTPException(
            status_code=400,
            detail="recommendation_id in path and body must match"
        )

    # 取得 session 驗證是否存在
    session = get_recommendation_session(user_id, recommendation_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session {recommendation_id} not found for user"
        )

    # 加入時間戳記
    if not swap.timestamp:
        swap.timestamp = datetime.now()

    # 記錄換菜
    swap_data = swap.dict()
    success = add_swap_to_session(user_id, recommendation_id, swap_data)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to record swap"
        )

    # 取得更新後的 swap count
    updated_session = get_recommendation_session(user_id, recommendation_id)
    swap_count = updated_session.get("total_swap_count", 0) if updated_session else 0

    return SwapResponse(
        status="success",
        message=f"Swap recorded: {swap.original_dish.dish_name} → {swap.new_dish.dish_name}",
        swap_count=swap_count
    )

@app.post("/v2/recommendations/{recommendation_id}/finalize", response_model=FinalizeResponse)
async def finalize_order(
    recommendation_id: str,
    finalize: FinalizeRequest,
    user_info: dict = Depends(get_current_user)
):
    """
    記錄最終點餐決策

    Args:
        recommendation_id: 推薦 ID
        finalize: 最終選擇資料
    """
    user_id = user_info.get("sub")

    # 驗證 recommendation_id 是否一致
    if finalize.recommendation_id != recommendation_id:
        raise HTTPException(
            status_code=400,
            detail="recommendation_id in path and body must match"
        )

    # 取得 session 驗證是否存在
    session = get_recommendation_session(user_id, recommendation_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session {recommendation_id} not found for user"
        )

    # 記錄最終選擇
    finalize_data = {
        "final_selections": [item.dict() for item in finalize.final_selections],
        "final_total_price": finalize.total_price,
        "session_duration_seconds": finalize.session_duration_seconds
    }

    success = finalize_recommendation_session(user_id, recommendation_id, finalize_data)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to finalize order"
        )

    # 產生訂單 ID
    order_id = f"order_{uuid.uuid4().hex[:12]}"

    # 計算摘要
    initial_price = session.get("initial_total_price", 0)
    final_price = finalize.total_price
    price_diff = final_price - initial_price
    swap_count = session.get("total_swap_count", 0)

    summary = {
        "order_id": order_id,
        "restaurant_name": session.get("restaurant_name"),
        "cuisine_type": session.get("restaurant_cuisine_type"),
        "dish_count": len(finalize.final_selections),
        "initial_total_price": initial_price,
        "final_total_price": final_price,
        "price_difference": price_diff,
        "total_swaps": swap_count,
        "session_duration_seconds": finalize.session_duration_seconds
    }

    return FinalizeResponse(
        status="success",
        message=f"Order finalized with {len(finalize.final_selections)} dishes",
        order_id=order_id,
        summary=summary
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



