from google.cloud import firestore
import hashlib
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firestore Client
# Assumes GOOGLE_APPLICATION_CREDENTIALS is set in env or default credentials are available
try:
    # Initialize with specific database ID
    db = firestore.Client(database="carted-data")
except Exception as e:
    print(f"Warning: Firestore client could not be initialized. Caching will be disabled. Error: {e}")
    db = None

COLLECTION_NAME = "restaurants"
CACHE_DURATION_DAYS = 180  # Changed from 30 to 180 days (6 months)

def _get_doc_id(place_id: str = None, restaurant_name: str = None) -> str:
    """
    Generates a consistent document ID.
    Prioritizes place_id if available, falls back to restaurant_name for backward compatibility.
    """
    if place_id:
        # Use place_id directly as the document ID (cleaner and guaranteed unique by Google)
        return place_id.replace("/", "_")  # Replace any slashes to make it Firestore-safe
    elif restaurant_name:
        # Fallback to old MD5 hash method for backward compatibility
        return hashlib.md5(restaurant_name.lower().strip().encode()).hexdigest()
    else:
        raise ValueError("Either place_id or restaurant_name must be provided")

def get_cached_data(place_id: str = None, restaurant_name: str = None) -> dict:
    """
    Retrieves cached data for a restaurant if it exists and is fresh.
    Prioritizes place_id for lookup, falls back to restaurant_name.
    Returns None if cache miss or expired.
    """
    if not db:
        return None

    doc_id = _get_doc_id(place_id=place_id, restaurant_name=restaurant_name)
    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)

    identifier = place_id or restaurant_name

    try:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            updated_at = data.get("updated_at")

            # Check expiration
            if updated_at:
                # Handle both datetime object and string (if serialized)
                if isinstance(updated_at, str):
                    updated_at = datetime.datetime.fromisoformat(updated_at)

                # Ensure timezone awareness compatibility (naive vs aware)
                if updated_at.tzinfo is None:
                    updated_at = updated_at.replace(tzinfo=datetime.timezone.utc)

                now = datetime.datetime.now(datetime.timezone.utc)

                if (now - updated_at).days < CACHE_DURATION_DAYS:
                    print(f"Cache HIT for {identifier} (age: {(now - updated_at).days} days)")
                    return data
                else:
                    print(f"Cache EXPIRED for {identifier} (age: {(now - updated_at).days} days, TTL: {CACHE_DURATION_DAYS} days)")
            else:
                 print(f"Cache INVALID (no timestamp) for {identifier}")
        else:
            print(f"Cache MISS for {identifier}")

    except Exception as e:
        print(f"Error reading from Firestore: {e}")

    return None

def save_restaurant_data(place_id: str = None, restaurant_name: str = None, reviews_data: dict = None, menu_text: str = None):
    """
    Saves restaurant data to Firestore.
    Prioritizes place_id as the key, falls back to restaurant_name for backward compatibility.
    """
    if not db:
        return

    doc_id = _get_doc_id(place_id=place_id, restaurant_name=restaurant_name)
    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)

    identifier = place_id or restaurant_name

    data = {
        "name": restaurant_name,
        "place_id": place_id,  # Store place_id for reference
        "reviews_data": reviews_data,  # Store raw reviews data structure
        "menu_text": menu_text,
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
    }

    try:
        doc_ref.set(data)
        print(f"Saved data for {identifier} to Firestore (using {'place_id' if place_id else 'restaurant_name'} as key).")
    except Exception as e:
        print(f"Error writing to Firestore: {e}")

def get_user_profile(user_id: str) -> dict:
    """
    Retrieves user profile (preferences, history).
    """
    if not db:
        return {}

    try:
        doc = db.collection("users").document(user_id).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Error getting user profile: {e}")
    
    return {}

def update_user_profile(user_id: str, feedback_data: dict):
    """
    Updates user profile based on feedback.
    Simple logic: Accumulate dietary restrictions or preferences based on comments/ratings.
    For MVP, we just store the raw feedback history.
    """
    if not db:
        return

    doc_ref = db.collection("users").document(user_id)

    try:
        # Use array_union to append feedback to history
        doc_ref.set({
            "feedback_history": firestore.ArrayUnion([feedback_data]),
            "last_updated": datetime.datetime.now(datetime.timezone.utc)
        }, merge=True)
        print(f"Updated profile for {user_id}")
    except Exception as e:
        print(f"Error updating user profile: {e}")

# ----- Session Tracking Functions -----

def create_recommendation_session(session_data: dict) -> bool:
    """
    建立新的推薦 session 記錄

    Args:
        session_data: RecommendationSession serialized dict

    Returns:
        bool: 是否成功建立
    """
    if not db:
        print("Warning: Firestore not available, session not saved.")
        return False

    user_id = session_data.get("user_id")
    recommendation_id = session_data.get("recommendation_id")

    if not user_id or not recommendation_id:
        print("Error: Missing user_id or recommendation_id")
        return False

    doc_ref = db.collection("users").document(user_id).collection("sessions").document(recommendation_id)

    try:
        doc_ref.set(session_data)
        print(f"Created session {recommendation_id} for user {user_id}")
        return True
    except Exception as e:
        print(f"Error creating session: {e}")
        return False

def get_recommendation_session(user_id: str, recommendation_id: str) -> dict:
    """
    取得指定的推薦 session

    Args:
        user_id: 使用者 ID
        recommendation_id: 推薦 ID

    Returns:
        dict: Session data or None
    """
    if not db:
        return None

    doc_ref = db.collection("users").document(user_id).collection("sessions").document(recommendation_id)

    try:
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Error getting session: {e}")

    return None

def add_swap_to_session(user_id: str, recommendation_id: str, swap_data: dict) -> bool:
    """
    將換菜記錄加入 session

    Args:
        user_id: 使用者 ID
        recommendation_id: 推薦 ID
        swap_data: SwapRequest serialized dict

    Returns:
        bool: 是否成功
    """
    if not db:
        print("Warning: Firestore not available, swap not recorded.")
        return False

    doc_ref = db.collection("users").document(user_id).collection("sessions").document(recommendation_id)

    try:
        # 使用 Firestore transaction 確保資料一致性
        doc_ref.update({
            "swap_history": firestore.ArrayUnion([swap_data]),
            "total_swap_count": firestore.Increment(1)
        })
        print(f"Added swap to session {recommendation_id}")
        return True
    except Exception as e:
        print(f"Error adding swap to session: {e}")
        return False

def finalize_recommendation_session(user_id: str, recommendation_id: str, finalize_data: dict) -> bool:
    """
    完成推薦 session，記錄最終選擇

    Args:
        user_id: 使用者 ID
        recommendation_id: 推薦 ID
        finalize_data: Dict containing final_selections, final_total_price, session_duration_seconds

    Returns:
        bool: 是否成功
    """
    if not db:
        print("Warning: Firestore not available, finalization not recorded.")
        return False

    doc_ref = db.collection("users").document(user_id).collection("sessions").document(recommendation_id)

    try:
        # 更新最終資料
        doc_ref.update({
            "final_selections": finalize_data.get("final_selections"),
            "final_total_price": finalize_data.get("final_total_price"),
            "session_duration_seconds": finalize_data.get("session_duration_seconds"),
            "finalized_at": datetime.datetime.now(datetime.timezone.utc)
        })
        print(f"Finalized session {recommendation_id}")
        return True
    except Exception as e:
        print(f"Error finalizing session: {e}")
        return False

def get_user_sessions(user_id: str, limit: int = 10) -> list:
    """
    取得使用者最近的 sessions

    Args:
        user_id: 使用者 ID
        limit: 回傳數量限制

    Returns:
        list: List of session dicts
    """
    if not db:
        return []

    try:
        sessions_ref = db.collection("users").document(user_id).collection("sessions")
        docs = sessions_ref.order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()

        sessions = []
        for doc in docs:
            sessions.append(doc.to_dict())

        return sessions
    except Exception as e:
        print(f"Error getting user sessions: {e}")
        return []

# ----- Recommendation Candidate Pool Functions -----

CANDIDATES_COLLECTION_NAME = "recommendation_candidates"

def save_recommendation_candidates(recommendation_id: str, candidates_data: list, cuisine_type: str) -> bool:
    """
    Saves the full candidate pool for a recommendation session.

    Args:
        recommendation_id: The unique ID of the recommendation session.
        candidates_data: A list of candidate dish dictionaries.
        cuisine_type: The detected cuisine type for the session.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not db:
        print("Warning: Firestore not available, candidate pool not saved.")
        return False

    doc_ref = db.collection(CANDIDATES_COLLECTION_NAME).document(recommendation_id)
    
    data = {
        "recommendation_id": recommendation_id,
        "cuisine_type": cuisine_type,
        "candidates": candidates_data,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }

    try:
        doc_ref.set(data)
        print(f"Saved candidate pool for recommendation {recommendation_id}")
        return True
    except Exception as e:
        print(f"Error saving recommendation candidates: {e}")
        return False

def get_recommendation_candidates(recommendation_id: str) -> dict:
    """
    Retrieves the full candidate pool for a recommendation session.

    Args:
        recommendation_id: The unique ID of the recommendation session.

    Returns:
        dict: The stored candidate data (including 'candidates' list), or None.
    """
    if not db:
        return None

    doc_ref = db.collection(CANDIDATES_COLLECTION_NAME).document(recommendation_id)

    try:
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Error getting recommendation candidates: {e}")
    
    return None
def save_user_activity(user_id: str, activity_type: str, data: dict) -> bool:
    """
    Saves a user activity (e.g., search, generate_menu) to Firestore.

    Args:
        user_id: The user's ID.
        activity_type: The type of activity (e.g., 'search', 'generate_menu').
        data: The activity data.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not db:
        print("Warning: Firestore not available, activity not saved.")
        return False

    try:
        activity_ref = db.collection("users").document(user_id).collection("activities").document()
        activity_data = {
            "type": activity_type,
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            **data
        }
        activity_ref.set(activity_data)
        
        # Update user's aggregate stats
        user_ref = db.collection("users").document(user_id)
        user_ref.set({
            "activity_counts": {
                activity_type: firestore.Increment(1)
            },
            "last_active": datetime.datetime.now(datetime.timezone.utc)
        }, merge=True)

        print(f"Saved user activity '{activity_type}' for user {user_id}")
        return True
    except Exception as e:
        print(f"Error saving user activity: {e}")
        return False

def save_job_status(job_id: str, status: str, result: dict = None, error: str = None):
    """
    Saves the status of an async job.
    """
    if not db:
        return

    doc_ref = db.collection("jobs").document(job_id)
    data = {
        "status": status,
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
    }
    if result:
        data["result"] = result
    if error:
        data["error"] = error
        
    try:
        doc_ref.set(data, merge=True)
    except Exception as e:
        print(f"Error saving job status: {e}")

def get_job_status(job_id: str) -> dict:
    """
    Retrieves the status of an async job.
    """
    if not db:
        return None

    try:
        doc = db.collection("jobs").document(job_id).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Error getting job status: {e}")
    
    return None
