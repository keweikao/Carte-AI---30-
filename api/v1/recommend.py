from fastapi import APIRouter, status, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from services.firestore_service import db
from schemas.restaurant_profile import RestaurantProfile, ProfileStatus, Meta
import datetime
import asyncio
import json

from pipeline.worker import run_pipeline # Import the real pipeline worker

router = APIRouter()

class RecommendRequest(BaseModel):
    place_id: str = Field(..., description="Google Place ID of the restaurant")
    # Placeholder for other user input parameters

async def event_generator(place_id: str):
    """Generates SSE events for the client, running the profiler pipeline."""
    # Step 1: Send initial processing status
    initial_data = {
        "status": "processing",
        "message": f"Starting profile generation for {place_id}..."
    }
    yield f"event: initial_data\ndata: {json.dumps(initial_data)}\n\n"
    
    try:
        # Step 2: Run the actual pipeline and get the final profile
        # The run_pipeline function already handles its own Firestore updates and prints progress.
        # For more granular SSE progress, run_pipeline itself would need to yield events.
        # For now, we'll wait for its completion and report final status.
        print(f"Calling real run_pipeline for {place_id}...")
        
        # Simulate progress events (re-introduce for test)
        progress_steps = [
            "Crawling images...",
            "Analyzing menus...",
            "Extracting dishes...",
            "Analyzing reviews...",
            "Generating profile..."
        ]
        for step_message in progress_steps:
            progress_data = {"status": "progress", "message": step_message}
            yield f"event: progress\ndata: {json.dumps(progress_data)}\n\n"
            await asyncio.sleep(0.5) # Simulate time for each step

        final_profile = await run_pipeline(place_id)
        print(f"Real run_pipeline for {place_id} completed.")

        # Step 3: Send completion event with the final profile
        completion_data = {
            "status": "complete",
            "message": "Restaurant profile generation complete!",
            "profile": final_profile.model_dump_json(by_alias=True) # Use model_dump_json for datetime serialization
        }
        yield f"event: complete\ndata: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        error_data = {
            "status": "error",
            "message": f"Pipeline failed: {str(e)}"
        }
        yield f"event: error\ndata: {json.dumps(error_data)}\n\n"
    
    finally:
        # This ensures the connection is properly closed by StreamingResponse
        pass


@router.post("/recommend")
async def recommend_menu(request: RecommendRequest, background_tasks: BackgroundTasks):
    # 1. Check Firestore for restaurant profile
    doc_ref = db.collection('restaurants').document(request.place_id)
    doc = doc_ref.get()

    if doc.exists:
        profile_data = doc.to_dict()
        # Ensure 'last_updated' is a datetime object before validation
        if 'meta' in profile_data and 'last_updated' in profile_data['meta'] and isinstance(profile_data['meta']['last_updated'], str):
            profile_data['meta']['last_updated'] = datetime.datetime.fromisoformat(profile_data['meta']['last_updated'].replace('Z', '+00:00'))
        
        try:
            profile = RestaurantProfile.model_validate(profile_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to validate profile data: {e}")

        if profile.meta.status == ProfileStatus.INDEXED:
            # Warm Start Logic (Placeholder for now)
            print(f"Warm start detected for {request.place_id}. Profile status: {profile.meta.status}")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "indexed", "message": "Placeholder for recommendation logic."}
            )
        else:
            # Profile exists but not indexed (pending, processing, error)
            # This path is typically handled by the SSE endpoint for Cold Start
            # Here, we just return a status indicating it's processing
            print(f"Profile for {request.place_id} is in status: {profile.meta.status}. Client should use SSE for updates.")
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content={"status": profile.meta.status.value, "message": f"Profile is {profile.meta.status.value}. Client should use SSE to monitor progress."}
            )
    else:
        # Cold Start Logic (Profile does not exist)
        # This endpoint is NOT for initiating cold starts with immediate 202
        # Clients should use the /stream_recommend endpoint for cold starts to get progress updates
        print(f"Cold start detected for {request.place_id}. Profile does not exist. Client should use SSE endpoint.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant profile not found. Please use /api/v1/stream_recommend to initiate cold start."
        )

@router.post("/stream_recommend")
async def stream_recommend_menu(request: RecommendRequest, background_tasks: BackgroundTasks):
    """
    Initiates a cold start for restaurant profile generation and streams progress via SSE.
    """
    print(f"Initiating cold start stream for {request.place_id}...")
    # Check if a profile is already processing for this place_id to avoid duplicate tasks
    doc_ref = db.collection('restaurants').document(request.place_id)
    doc = doc_ref.get()
    
    if doc.exists:
        profile_data = doc.to_dict()
        if 'meta' in profile_data and 'status' in profile_data['meta']:
            current_status = ProfileStatus(profile_data['meta']['status'])
            if current_status == ProfileStatus.PROCESSING or current_status == ProfileStatus.PENDING:
                # If already processing, just tell the client to monitor
                print(f"Profile for {request.place_id} is already {current_status.value}. Monitoring existing task.")
                # We can return an event stream that just monitors status, or simply return 202
                # For now, let's just re-attach to the stream (simplified by running event_generator again)
                return StreamingResponse(event_generator(request.place_id), media_type="text/event-stream")
            elif current_status == ProfileStatus.INDEXED:
                # If already indexed, this shouldn't be a cold start. Redirect or return data directly.
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already indexed. Use /api/v1/recommend for warm start.")

    # Create a new placeholder profile to indicate processing
    new_profile_meta = Meta(
        name=f"TEMP NAME FOR {request.place_id}", # Will be updated by pipeline
        place_id=request.place_id,
        status=ProfileStatus.PENDING,
        last_updated=datetime.datetime.now(datetime.timezone.utc)
    )
    new_profile = RestaurantProfile(
        meta=new_profile_meta,
        menu_items=[],
        precomputed_sets={}
    )
    doc_ref.set(new_profile.model_dump(by_alias=True, exclude_unset=True))
    
    return StreamingResponse(event_generator(request.place_id), media_type="text/event-stream")
