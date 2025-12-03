# Task Checklist: Architecture V2 - Phase 1

This document breaks down the tasks required to complete **Phase 1: Foundational Schema & API Layer** of the `implementation_plan_v2_hybrid.md`.

## 1. Setup & Schema Definition

-   [ ] Create a new directory `api/v1/`.
-   [ ] Create a new file `schemas/restaurant_profile.py`.
-   [ ] In `schemas/restaurant_profile.py`, define a Pydantic model `Meta` with fields: `name`, `place_id`, `address`, `status` (Enum: "indexed", "pending", "error"), `last_updated`.
-   [ ] In `schemas/restaurant_profile.py`, define a Pydantic model `Evidence` with fields: `image_url` (Optional), `ocr_confidence` (Optional).
-   [ ] In `schemas/restaurant_profile.py`, define a Pydantic model `MenuItem` with fields: `id`, `name`, `price`, `category`, `description` (Optional), `tags` (List[str]), `evidence` (Optional[Evidence]).
-   [ ] In `schemas/restaurant_profile.py`, define a Pydantic model `PrecomputedSetItem` with fields: `title`, `total_price`, `items` (List[str]), `reasoning`.
-   [ ] In `schemas/restaurant_profile.py`, define the main Pydantic model `RestaurantProfile` containing `meta` (Meta), `menu_items` (List[MenuItem]), and `precomputed_sets` (Dict[str, PrecomputedSetItem]).

## 2. API Endpoint Implementation

-   [ ] Create a new file `api/v1/recommend.py`.
-   [ ] In `api/v1/recommend.py`, initialize a new `APIRouter` from FastAPI.
-   [ ] Define the `POST /recommend` endpoint function. It should accept a request body model containing at least `place_id: str`.
-   [ ] Add placeholder logic inside the endpoint to represent the main functionality.
-   [ ] Modify `main.py` (or create a new entry point) to include this new V1 API router.

## 3. Firestore & Background Task Logic

-   [ ] In `api/v1/recommend.py`, add the necessary code to initialize the Firestore client (can be imported from `services.firestore_service`).
-   [ ] Implement the database query within the endpoint: `db.collection('restaurants').document(place_id).get()`.
-   [ ] Implement the `if/else` logic based on the document's existence and its `status` field.
-   [ ] **Cold Start Block (`else`)**:
    -   [ ] Define a placeholder function `trigger_profiler_pipeline(place_id: str)`. For now, it can just contain a `print()` statement.
    -   [ ] Use FastAPI's `BackgroundTasks` to add `trigger_profiler_pipeline` as a background task.
    -   [ ] Return a `JSONResponse` with `status_code=202` and a body like `{"status": "processing", "message": "Restaurant profile is being generated."}`.
-   [ ] **Warm Start Block (`if`)**:
    -   [ ] Add a `print()` or `logging` statement indicating a warm start.
    -   [ ] For now, return a placeholder `JSONResponse` like `{"status": "indexed", "message": "Placeholder for recommendation logic."}`.
-   [ ] Add a separate test script `test_api_v1.py` to verify the cold/warm start responses.
