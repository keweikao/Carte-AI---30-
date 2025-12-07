# Task Checklist: Architecture V2 (Refined Plan)

This document provides a detailed, actionable checklist for implementing the complete "Menu-First" architecture, based on the refined specifications in `specs/architecture_v2_pipeline.md`.

---

## Phase 1: Foundational Setup & API Layer

**Goal**: Establish the new data schemas, create a robust API layer capable of handling different warm-start paths, and define the asynchronous communication protocol for cold starts.

### 1.1. Schema Definition
-   [ ] Create/Update `schemas/restaurant_profile.py` with Pydantic models.
-   [ ] Define `Meta` model, including `status` Enum (`indexed`, `pending`, `error`).
-   [ ] Define `MenuItem` model, ensuring it includes `original_category: str` and `standard_category: str` as per the refined spec.
-   [ ] Define `PrecomputedSetItem` model.
-   [ ] Define the main `RestaurantProfile` model that encapsulates all sub-models.

### 1.2. API Endpoint & Routing
-   [ ] Create a new directory `api/v1/`.
-   [ ] Create `api/v1/recommend.py` and initialize a FastAPI `APIRouter`.
-   [ ] Modify `main.py` to include the new `v1` router.

### 1.3. Warm Start Logic (`/recommend` endpoint)
-   [ ] Implement `POST /recommend` endpoint to handle synchronous, warm-start requests.
-   [ ] Implement Firestore `get()` logic to check for an existing profile with `status == 'indexed'`.
-   [ ] **Path A (Pre-computed):**
    -   [ ] Implement logic to match user input against `precomputed_sets`.
    -   [ ] If a match is found, add a placeholder to format the response with Gemini Flash and return it.
-   [ ] **Path B (Dynamic Filter - Fallback):**
    -   [ ] If no pre-computed set matches, implement the dynamic filtering logic.
    -   [ ] Use Python to filter the `menu_items` list based on user query parameters (e.g., tags, price).
    -   [ ] Add a placeholder to send the filtered list to Gemini Flash to generate a final response.

### 1.4. Cold Start Logic (`/stream_recommend` endpoint)
-   [ ] Implement a new `POST /stream_recommend` endpoint designed for Server-Sent Events (SSE).
-   [ ] Use FastAPI's `StreamingResponse` with a media type of `text/event-stream`.
-   [ ] **Initial Response**: Immediately query Google Places for basic info (name, address) and stream the `initial_data` event.
-   [ ] **Background Task**: Trigger the (placeholder) `run_pipeline` background task.
-   [ ] **Progress Events**: As the pipeline runs (in Phase 2), it should be able to report progress. For now, simulate this by streaming `progress` events (e.g., `{"status": "crawling"}`).
-   [ ] **Completion Event**: Stream the `complete` event with the final data upon task completion.

---

## Phase 2: Profiler Pipeline (The Worker)

**Goal**: Implement the core data processing engine that runs asynchronously to build the `Golden Profile`.

### 2.1. Ingestion & Vision
-   [ ] Create a `pipeline/` directory.
-   [ ] In `pipeline/ingestion.py`, implement the Apify `google-maps-scraper` service call. Include error handling for scraper failures.
-   [ ] In `pipeline/vision.py`, implement the Gemini Flash `image_filter` function.
-   [ ] In `pipeline/vision.py`, implement the Gemini Pro `menu_extractor_ocr` function, ensuring it captures `evidence`.

### 2.2. Data Cleaning & Normalization
-   [ ] In a new module `pipeline/normalization.py`, create a `normalize_price` function to clean price strings into integers.
-   [ ] In `pipeline/normalization.py`, create a `normalize_category` function that uses a mapping dictionary or a Gemini Flash call to map `original_category` to `standard_category` (e.g., "前菜", "Starters" -> "appetizer").

### 2.3. Analysis & Tagging
-   [ ] In a new module `pipeline/analysis.py`, implement a function to perform keyword frequency analysis on reviews.
-   [ ] In `pipeline/analysis.py`, implement the Gemini Flash `dish_tagger` function to generate descriptive tags for each `MenuItem` based on review snippets.

### 2.4. Worker Assembly
-   [ ] Create `pipeline/worker.py` with a main `run_pipeline(place_id: str)` function.
-   [ ] Orchestrate all steps: Ingestion -> Vision -> Normalization -> Analysis.
-   [ ] Ensure the worker writes the complete, processed `RestaurantProfile` to Firestore and updates the `status` to `indexed`.
-   [ ] Integrate this real worker with the background task trigger in the `/stream_recommend` endpoint.

---

## Phase 3: Pre-computation & Finalization

**Goal**: Implement the final optimization step to enable sub-3-second responses for common scenarios.

### 3.1. Menu Architect
-   [ ] Create `pipeline/architect.py`.
-   [ ] Implement a rule-based `generate_precomputed_sets` function that takes the final `menu_items` list.
-   [ ] The function should generate various set menus for common scenarios (`dating_2_people`, `family_4`, etc.) and return a dictionary matching the `precomputed_sets` schema.

### 3.2. Final Integration
-   [ ] Add the `generate_precomputed_sets` function as the final step in the `pipeline/worker.py` before writing to Firestore.
-   [ ] Fully implement the logic in the `/recommend` endpoint (Path A) to retrieve and format these `precomputed_sets` for the user.
-   [ ] Write end-to-end integration tests to validate the entire flow.
