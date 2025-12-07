# Async Job Implementation for Recommendation Service

## Overview
To support background processing (allowing users to switch apps without interrupting analysis) and improve reliability, we transitioned the recommendation API from synchronous to asynchronous.

## Changes

### Backend (`main.py`, `services/firestore_service.py`)
1.  **New Endpoints**:
    *   `POST /v2/recommendations/async`: Starts a background task and returns a `job_id`.
    *   `GET /v2/recommendations/status/{job_id}`: Returns the status (`pending`, `processing`, `completed`, `failed`) and result.
2.  **Firestore Job Tracking**:
    *   Jobs are tracked in the `jobs` collection in Firestore.
    *   Status and results are persisted.

### Frontend (`lib/api.ts`, `app/recommendation/page.tsx`)
1.  **Polling Mechanism**:
    *   The frontend now initiates the job and polls the status endpoint every 2 seconds.
    *   This ensures that even if the browser tab is backgrounded (on mobile), the server continues processing.
    *   When the user returns, the polling resumes (or completes if finished).
2.  **Error Handling**:
    *   If the job fails or an error occurs, the user is automatically redirected back to the `/input` page to retry.

## Benefits
*   **Reliability**: Long-running analysis (30s+) is no longer bound by HTTP timeouts or browser connection state.
*   **UX**: Users can multitask on their phone while waiting for the recommendation.
*   **Error Recovery**: Failures are handled gracefully with a redirect.

## Future Improvements
*   **Resume Session**: Store `job_id` in URL or `localStorage` to allow full page reloads without losing progress.
*   **Push Notifications**: Notify user when analysis is done (requires Service Worker).
