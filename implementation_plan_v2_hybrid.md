# Implementation Plan: Architecture V2 (Hybrid Approach)

This document outlines the phased implementation plan for transitioning to the new "Menu-First" pipeline architecture, as defined in `specs/architecture_v2_pipeline.md`.

We will adopt a **hybrid approach** to de-risk the project and deliver value incrementally. The core idea is to solve the **data quality problem first** by building the new data pipeline, while temporarily retaining the existing `OrchestratorAgent` for recommendation logic. Once the data foundation is solid, we will proceed to optimize the real-time recommendation speed.

---

## Phase 1: Foundational Schema & API Layer

**Goal**: Establish the new data contract and the API endpoint behavior for handling cold/warm starts.

**Key Tasks**:
1.  **Schema Definition**:
    -   [ ] Create Pydantic models in a new file `schemas/restaurant_profile.py` that strictly match the new Firestore `restaurants` collection schema.
    -   This includes `Meta`, `MenuItem`, and `PrecomputedSet` models.

2.  **API Endpoint Implementation**:
    -   [ ] In a new file `api/v1/recommend.py`, create a new FastAPI router.
    -   [ ] Implement the `POST /api/v1/recommend` endpoint.

3.  **Cold/Warm Start Logic**:
    -   [ ] The endpoint will first query Firestore for the restaurant document based on `place_id`.
    -   [ ] **If `doc.exists and doc.to_dict().get('meta', {}).get('status') == 'indexed'` (Warm Start):**
        -   For now, log a "Warm start detected" message.
        -   Temporarily, it will still call the **existing `OrchestratorAgent`** as a placeholder for the recommendation logic.
    -   [ ] **If `doc` does not exist or `status` is not `indexed` (Cold Start):**
        -   [ ] Implement the logic to return an `HTTP 202 Accepted` response.
        -   [ ] The response body should contain basic info (e.g., restaurant name) and a `status: 'processing'` message.
        -   [ ] Implement the trigger for a background task (e.g., using `FastAPI.BackgroundTasks`). The task itself will be a placeholder function for now.

---

## Phase 2: Data Pipeline Implementation (The Worker)

**Goal**: Build the offline worker that fetches and processes restaurant data into the new Firestore schema.

**Key Tasks**:
1.  **Create Pipeline Worker Module**:
    -   [ ] Create a new directory `pipeline/` with a main file `profiler_worker.py`.

2.  **Step 2.1: Data Ingestion Service**:
    -   [ ] Create a module `pipeline/ingestion/apify_scraper.py`.
    -   [ ] Implement a function to call the Apify `google-maps-scraper` actor and retrieve image URLs and reviews.

3.  **Step 2.2: Image Processing Service**:
    -   [ ] Create a module `pipeline/vision/menu_ocr.py`.
    -   [ ] Implement an `image_filter` function using Gemini Flash to identify which of the scraped images are menus.
    -   [ ] Implement a `menu_extractor_ocr` function using Gemini Pro (Vision) to process the filtered menu images and output structured `MenuItem` data, including the `evidence` field.

4.  **Step 2.3: Review Analysis Service**:
    -   [ ] Create a module `pipeline/analysis/review_tagger.py`.
    -   [ ] Implement a function that takes reviews, performs basic keyword counting in Python, and then calls Gemini Flash to generate relevant `tags` for each dish identified in the OCR step.

5.  **Assemble the Worker**:
    -   [ ] In `profiler_worker.py`, create a main `run_pipeline` function.
    -   [ ] This function will chain the above steps in the correct order: Ingestion -> Image Filter -> OCR -> Review Tagging.
    -   [ ] The final step of the pipeline will be to write the complete `RestaurantProfile` object (with `meta`, `menu_items`, etc.) to Firestore and set the `meta.status` to `"indexed"`.

---

## Phase 3: Connecting the Dots & Adapting the Orchestrator

**Goal**: Connect the API layer to the data pipeline and make the existing `OrchestratorAgent` work with the new, high-quality data.

**Key Tasks**:
1.  **Connect API to Worker**:
    -   [ ] In the `POST /api/v1/recommend` endpoint, replace the placeholder background task from Phase 1 with a call to the `run_pipeline` function from Phase 2.

2.  **Adapt `OrchestratorAgent`**:
    -   [ ] Modify `agent/recommendation_agents.py`.
    -   [ ] The `OrchestratorAgent.run` method's signature will be updated to accept the new `RestaurantProfile` Pydantic model instead of the old `candidates` list.
    -   [ ] **Crucially, refactor `DishSelectorAgent`'s prompt and input logic.** It should now primarily use the `profile.menu_items` list as its source of truth for selecting dishes, leveraging the rich `tags` and verified `price`. This eliminates the need for it to reason over messy, conflicting data.

3.  **Deploy & Evaluate**:
    -   [ ] Deploy the new end-to-end flow.
    -   [ ] At this stage, cold starts will trigger the new, robust pipeline.
    -   [ ] Warm starts will yield much higher **quality** recommendations, although the **latency will still be high (~52 seconds)**.

---

## Phase 4: Performance Optimization (The Final Step)

**Goal**: Address the ~52-second warm-start latency and achieve the target of < 3 seconds for most requests.

**Key Tasks**:
1.  **Implement Pre-computation Engine**:
    -   [ ] Create a `pipeline/architect/menu_architect.py` module.
    -   [ ] Implement the logic to generate various `precomputed_sets` (e.g., for 2 people, 4 people, solo diners) based on the structured `menu_items`. This will likely be a rule-based engine, not an LLM.
    -   [ ] Add this as the final step in the `profiler_worker.py` pipeline, so `precomputed_sets` are saved along with the main profile.

2.  **Update Warm Start Logic**:
    -   [ ] Modify the `POST /api/v1/recommend` endpoint's warm start path.
    -   [ ] It should now attempt to find a matching scenario in the `precomputed_sets` field in Firestore based on the user's input.
    -   [ ] **If a match is found**: Use Gemini Flash to format the pre-computed set into a natural language response and return it. This is the **fast path (< 3s)**.
    -   [ ] **If no match is found (Fallback)**: As a fallback, invoke the (now adapted) `OrchestratorAgent` to generate a menu on the fly. This will be the slower `~52s` path, but ensures all requests can be handled.

This phased plan ensures we build a robust data foundation first, immediately improving recommendation quality, before moving on to solve the final real-time performance challenge.
