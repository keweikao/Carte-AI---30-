from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.recommendation import UserInputV2, RecommendationResponseV2, RecommendationRequest, FullRecommendationResponse, MenuItemV2, AddOnRequest, AddOnResponse
from schemas.feedback import FeedbackRequest
from schemas.tracking import SwapRequest, SwapResponse, FinalizeRequest, FinalizeResponse
from agent.dining_agent import DiningAgent
from auth.google_auth import verify_google_token
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search, fetch_place_autocomplete
from agent.prompt_builder import create_prompt_for_gemini_v2
from services.firestore_service import (
    update_user_profile,
    create_recommendation_session,
    get_recommendation_session,
    add_swap_to_session,
    finalize_recommendation_session,
    get_recommendation_candidates,
    save_user_activity
)
import uvicorn
import os
import uuid
from datetime import datetime

USE_MOCK_EXTERNAL = os.getenv("USE_MOCK_EXTERNAL", "").lower() in ("1", "true", "yes")

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

security = HTTPBearer(auto_error=not USE_MOCK_EXTERNAL)


def _mock_user():
    return {"sub": "mock-user", "email": "mock@example.com", "name": "Mock User"}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if USE_MOCK_EXTERNAL:
        return _mock_user()

    if not credentials:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = credentials.credentials
    return verify_google_token(token)


# --- Mock plumbing (in-memory) ---
_mock_sessions = {}
_mock_candidates = {}


async def mock_fetch_place_autocomplete(input: str):
    return [
        {"description": f"{input} Mock 餐廳", "place_id": "mock-place-1", "main_text": f"{input} Mock", "secondary_text": "台北市"},
        {"description": f"{input} Mock Bistro", "place_id": "mock-place-2", "main_text": f"{input} Bistro", "secondary_text": "新北市"},
    ]


class MockDiningAgent:
    async def get_recommendations_v2(self, request: UserInputV2) -> RecommendationResponseV2:
        rid = f"mock-{uuid.uuid4().hex[:8]}"
        items = [
            DishSlotResponse(
                category="熱菜",
                display=MenuItemV2(dish_name="宮保雞丁", price=250, quantity=1, reason="人氣招牌", category="熱菜", review_count=120),
                alternatives=[
                    MenuItemV2(dish_name="左宗棠雞", price=260, quantity=1, reason="口味相似", category="熱菜", review_count=80)
                ],
            ),
            DishSlotResponse(
                category="主食",
                display=MenuItemV2(dish_name="蛋炒飯", price=120, quantity=request.party_size, reason="填飽肚子", category="主食", review_count=60),
                alternatives=[],
            ),
        ]
        category_summary = {"熱菜": 1, "主食": 1}
        total_price = sum(slot.display.price for slot in items)
        resp = RecommendationResponseV2(
            recommendation_summary="為您準備了招牌熱菜與主食的組合。",
            items=items,
            total_price=total_price,
            nutritional_balance_note="葷素搭配，適合分享。",
            recommendation_id=rid,
            restaurant_name=request.restaurant_name,
            user_info=_mock_user(),
            cuisine_type="中式餐館",
            category_summary=category_summary,
            currency="TWD",
        )
        # 保存候選池（簡化）
        _mock_candidates[rid] = {
            "candidates": [slot.display.model_dump() for slot in items] + [alt.model_dump() for slot in items for alt in slot.alternatives],
            "cuisine_type": "中式餐館",
        }
        _mock_sessions[rid] = {
            "restaurant_name": request.restaurant_name,
            "restaurant_cuisine_type": "中式餐館",
            "initial_recommendations": [slot.display.model_dump() for slot in items],
            "initial_total_price": total_price,
            "swap_history": [],
            "total_swap_count": 0,
        }
        return resp


def mock_save_user_activity(*args, **kwargs):
    return True


def mock_create_recommendation_session(session_data):
    rid = session_data.get("recommendation_id") or f"mock-{uuid.uuid4().hex[:8]}"
    _mock_sessions[rid] = session_data
    return True


def mock_get_recommendation_session(user_id, recommendation_id):
    return _mock_sessions.get(recommendation_id)


def mock_add_swap_to_session(user_id, recommendation_id, swap_data):
    session = _mock_sessions.get(recommendation_id)
    if not session:
        return False
    session.setdefault("swap_history", []).append(swap_data)
    session["total_swap_count"] = len(session["swap_history"])
    return True


def mock_finalize_recommendation_session(user_id, recommendation_id, finalize_data):
    session = _mock_sessions.get(recommendation_id)
    if not session:
        return False
    session.update(finalize_data)
    return True


def mock_get_recommendation_candidates(recommendation_id):
    return _mock_candidates.get(recommendation_id)


def mock_save_recommendation_candidates(recommendation_id, candidates_data, cuisine_type):
    _mock_candidates[recommendation_id] = {
        "candidates": candidates_data,
        "cuisine_type": cuisine_type,
    }
    return True


def mock_update_user_profile(user_id, data):
    return True


if USE_MOCK_EXTERNAL:
    fetch_place_autocomplete = mock_fetch_place_autocomplete  # type: ignore
    save_user_activity = mock_save_user_activity  # type: ignore
    create_recommendation_session = mock_create_recommendation_session  # type: ignore
    get_recommendation_session = mock_get_recommendation_session  # type: ignore
    add_swap_to_session = mock_add_swap_to_session  # type: ignore
    finalize_recommendation_session = mock_finalize_recommendation_session  # type: ignore
    get_recommendation_candidates = mock_get_recommendation_candidates  # type: ignore
    save_recommendation_candidates = mock_save_recommendation_candidates  # type: ignore
    update_user_profile = mock_update_user_profile  # type: ignore
    agent = MockDiningAgent()
else:
    agent = DiningAgent()

@app.get("/places/autocomplete")
async def get_place_autocomplete(
    input: str = Query(..., min_length=1),
    user_info: dict = Depends(get_current_user)
):
    """
    Proxies Google Places Autocomplete API to get restaurant suggestions.
    Requires authentication to prevent abuse.
    """
    # Record search activity
    try:
        user_id = user_info.get("sub")
        save_user_activity(user_id, "search", {"query": input})
    except Exception as e:
        print(f"Failed to record search activity: {e}")

    suggestions = await fetch_place_autocomplete(input)
    return {"suggestions": suggestions}

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
        # Enhanced error reporting for debugging
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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

@app.post("/v2/recommendations/{recommendation_id}/add-on", response_model=AddOnResponse)
async def request_add_on(
    recommendation_id: str,
    request: AddOnRequest,
    user_info: dict = Depends(get_current_user)
):
    """
    請求加點推薦
    從候選菜品池中尋找符合類別的額外菜品。
    """
    user_id = user_info.get("sub")
    
    # 1. 驗證 Session
    session = get_recommendation_session(user_id, recommendation_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # 2. 取得候選菜品池
    candidates_data = get_recommendation_candidates(recommendation_id)
    if not candidates_data or "candidates" not in candidates_data:
        # 如果沒有候選池，回傳空列表（前端會顯示提示）
        return AddOnResponse(new_dishes=[])
        
    all_candidates = candidates_data["candidates"]
    
    # 3. 找出已推薦的菜品（避免重複）
    recommended_names = set()
    
    # 包含初始推薦
    if "initial_recommendations" in session:
        for item in session["initial_recommendations"]:
            recommended_names.add(item.get("dish_name"))
            
    # 包含換過的菜
    if "swap_history" in session:
        for swap in session["swap_history"]:
            if "new_dish" in swap:
                recommended_names.add(swap["new_dish"].get("dish_name"))
                
    # 4. 篩選符合類別且未重複的菜品
    available_dishes = []
    target_category = request.category
    
    for dish in all_candidates:
        # 檢查是否已推薦
        if dish.get("dish_name") in recommended_names:
            continue
            
        # 檢查類別 (模糊匹配)
        dish_category = dish.get("category", "")
        if target_category in dish_category or dish_category in target_category:
            available_dishes.append(dish)
            
    # 5. 選擇前 N 個
    selected_dishes = available_dishes[:request.count]
    
    # 6. 轉換格式並回傳
    result_dishes = []
    for dish in selected_dishes:
        # 確保 quantity 存在，預設為 1
        if "quantity" not in dish:
            dish["quantity"] = 1
            
        try:
            menu_item = MenuItemV2(**dish)
            result_dishes.append(menu_item)
        except Exception as e:
            print(f"Error converting dish to MenuItemV2: {e}")
            continue
        
    return AddOnResponse(new_dishes=result_dishes)

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
