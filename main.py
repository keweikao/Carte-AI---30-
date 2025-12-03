from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import (
    FastAPI, HTTPException, Depends, Query
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.restaurant_profile import RestaurantProfile
from auth.google_auth import verify_google_token
from agent.data_fetcher import fetch_place_autocomplete
from api.v1.restaurant import router as v1_restaurant_router
from api.v1.recommend_v2 import router as v2_recommend_router
import os
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        firebase_admin.initialize_app()
    except Exception as e:
        print(f"Warning: Failed to initialize Firebase Admin SDK: {e}")

USE_MOCK_EXTERNAL = os.getenv("USE_MOCK_EXTERNAL", "").lower() in ("true", "1", "yes")

app = FastAPI(title="AI Dining Agent API", version="4.1")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://dining-frontend-1045148759148.asia-east1.run.app",
        "https://dining-frontend-u33peegeaa-de.a.run.app",
        "https://dining-frontend-staging-1045148759148.asia-east1.run.app",
        "https://www.carte.tw"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_restaurant_router, prefix="/api/v1") # New v4.1 router
app.include_router(v2_recommend_router, prefix="/api/v1") # V2 recommendation router

security = HTTPBearer(auto_error=not USE_MOCK_EXTERNAL)
def _mock_user():
    return {
        "sub": "mock-user",
        "email": "keweikao@gmail.com",
        "name": "Mock User"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if USE_MOCK_EXTERNAL:
        return _mock_user()
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = credentials.credentials
    return verify_google_token(token)

if USE_MOCK_EXTERNAL:
    _fetch_place_autocomplete = fetch_place_autocomplete
    async def mock_fetch_place_autocomplete(input: str):
        return await _fetch_place_autocomplete(input) if GOOGLE_API_KEY else [{"description": f"{input} Mock", "place_id": "mock-place-1"}]
    fetch_place_autocomplete = mock_fetch_place_autocomplete

@app.get("/places/autocomplete")
async def get_place_autocomplete_endpoint(
    input: str = Query(..., min_length=1),
    user_info: dict = Depends(get_current_user)
):
    """
    Proxies Google Places Autocomplete API to get restaurant suggestions.
    """
    suggestions = await fetch_place_autocomplete(input)
    return {"suggestions": suggestions}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Async Recommendation API (True Async with Polling) ---
from fastapi import BackgroundTasks
from schemas.recommendation import UserInputV2
from api.v1.recommend_v2 import recommend_dishes_v2
from services.job_manager import job_manager, JobStatus

async def process_recommendation_task(job_id: str, user_input: UserInputV2):
    """
    Background task to process recommendation pipeline
    """
    try:
        print(f"[Job {job_id}] Starting processing...")
        job_manager.update_status(job_id, JobStatus.PROCESSING, 10, "正在搜尋餐廳資料...")
        
        # Execute pipeline
        # TODO: Pass job_id to recommend_dishes_v2 for granular progress updates
        recommendations = await recommend_dishes_v2(user_input)
        
        print(f"[Job {job_id}] Completed successfully")
        job_manager.update_status(
            job_id, 
            JobStatus.COMPLETED, 
            100, 
            "分析完成！", 
            result=recommendations
        )
    except Exception as e:
        print(f"[Job {job_id}] Failed: {e}")
        import traceback
        traceback.print_exc()
        job_manager.update_status(
            job_id, 
            JobStatus.FAILED, 
            0, 
            "分析失敗，請稍後再試", 
            error=str(e)
        )

@app.post("/v2/recommendations/async")
async def recommend_async(user_input: UserInputV2, background_tasks: BackgroundTasks):
    """
    Starts an async recommendation job.
    Returns a job_id immediately.
    """
    try:
        # Create job in Firestore
        job_id = job_manager.create_job(user_input.model_dump())
        
        # Add background task
        background_tasks.add_task(process_recommendation_task, job_id, user_input)
        
        return {"job_id": job_id, "status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start job: {str(e)}")

@app.get("/v2/recommendations/status/{job_id}")
async def get_job_status(job_id: str):
    """
    Retrieves the status of the recommendation job from Firestore.
    """
    job = job_manager.get_job(job_id)
    if not job:
        # Fallback for old base64 job_ids (backward compatibility)
        if len(job_id) > 50: 
             return {"status": "failed", "error": "Invalid job ID format (legacy)"}
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "status": job["status"],
        "progress": job.get("progress", 0),
        "message": job.get("message", ""),
        "result": job.get("result"),
        "error": job.get("error")
    }

# --- Finalize Order API Simulation (for Frontend Compatibility) ---
from schemas.tracking import FinalizeRequest, FinalizeResponse
import uuid

@app.post("/v2/recommendations/{recommendation_id}/finalize", response_model=FinalizeResponse)
async def finalize_order(recommendation_id: str, request: FinalizeRequest):
    """
    Records the final order selection.
    Currently a stub that logs the data to allow the frontend flow to complete.
    """
    print(f"[Tracking] Finalizing order for recommendation: {recommendation_id}")
    print(f"  - Total Price: {request.total_price}")
    print(f"  - Selections: {len(request.final_selections)} items")
    
    # In a real implementation, we would save this to Firestore
    
    return FinalizeResponse(
        status="success",
        message="Order finalized successfully",
        order_id=str(uuid.uuid4()),
        summary={
            "total_price": request.total_price,
            "item_count": len(request.final_selections)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)