import os
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK FIRST
if not firebase_admin._apps:
    try:
        firebase_admin.initialize_app()
    except Exception as e:
        print(f"Warning: Failed to initialize Firebase Admin SDK: {e}")

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
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            return await _fetch_place_autocomplete(input)
        
        return [{
            "description": f"{input} Mock", 
            "place_id": "mock-place-1",
            "main_text": f"{input} Mock",
            "secondary_text": "Mock Address"
        }]
    fetch_place_autocomplete = mock_fetch_place_autocomplete

@app.get("/places/autocomplete")
async def get_place_autocomplete_endpoint(
    input: str = Query(..., min_length=1)
):
    """
    Proxies Google Places Autocomplete API to get restaurant suggestions.
    """
    suggestions = await fetch_place_autocomplete(input)
    return {"suggestions": suggestions}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Legacy Routes for Backward Compatibility ---
from services.job_manager import job_manager

@app.get("/v2/recommendations/status/{job_id}")
async def get_job_status_legacy(job_id: str):
    """Legacy endpoint for backward compatibility with existing frontend"""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)