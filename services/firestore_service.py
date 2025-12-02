from google.cloud import firestore
import datetime
import os
from typing import Optional

from dotenv import load_dotenv

from schemas.restaurant_profile import RestaurantProfile

load_dotenv()

# Initialize Firestore Client
try:
    db = firestore.Client(project="gen-lang-client-0415289079", database="carted-data")
except Exception as e:
    print(f"Warning: Firestore client could not be initialized. Caching will be disabled. Error: {e}")
    db = None

RESTAURANTS_COLLECTION = "restaurants"
CACHE_TTL_DAYS = 7  # Time-to-live for cache is 7 days as per v4.1 spec

def get_restaurant_profile(place_id: str) -> Optional[RestaurantProfile]:
    """
    Retrieves a restaurant profile from Firestore if it exists and is not stale.

    Args:
        place_id: The Google Place ID of the restaurant.

    Returns:
        A RestaurantProfile Pydantic object if a valid cache entry is found, otherwise None.
    """
    if not db:
        print("Firestore is not available. Cannot get profile.")
        return None

    doc_ref = db.collection(RESTAURANTS_COLLECTION).document(place_id)

    try:
        doc = doc_ref.get()
        if not doc.exists:
            print(f"Cache MISS for place_id: {place_id}")
            return None

        data = doc.to_dict()
        updated_at = data.get("updated_at")

        # --- Cache Validity Check ---
        if not updated_at:
            print(f"Cache INVALID (no timestamp) for place_id: {place_id}")
            return None

        # Ensure timezone awareness for comparison
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=datetime.timezone.utc)

        now = datetime.datetime.now(datetime.timezone.utc)
        age = now - updated_at

        if age.days >= CACHE_TTL_DAYS:
            print(f"Cache EXPIRED for place_id: {place_id} (age: {age.days} days, TTL: {CACHE_TTL_DAYS} days)")
            return None
        
        print(f"Cache HIT for place_id: {place_id} (age: {age.days} days)")
        
        # Parse data into the Pydantic model to ensure type safety
        return RestaurantProfile(**data)

    except Exception as e:
        print(f"Error reading restaurant profile from Firestore for place_id {place_id}: {e}")
        return None


def save_restaurant_profile(profile: RestaurantProfile) -> bool:
    """
    Saves a restaurant profile to Firestore.

    Args:
        profile: The RestaurantProfile Pydantic object to save.

    Returns:
        True if successful, False otherwise.
    """
    if not db:
        print("Firestore is not available. Cannot save profile.")
        return False
        
    if not profile.place_id:
        print("Error: place_id is required to save a restaurant profile.")
        return False

    doc_ref = db.collection(RESTAURANTS_COLLECTION).document(profile.place_id)

    try:
        # Use .model_dump() to convert the Pydantic model to a dict suitable for Firestore
        data_to_save = profile.model_dump()
        
        doc_ref.set(data_to_save)
        print(f"Successfully saved profile for place_id: {profile.place_id} to Firestore.")
        return True
    except Exception as e:
        print(f"Error writing restaurant profile to Firestore for place_id {profile.place_id}: {e}")
        return False

# You can add a simple test block if needed
if __name__ == "__main__":
    
    # This is a dummy test block. It won't work without a valid RestaurantProfile object.
    # It serves as an example for future testing.
    def test_firestore_service():
        print("Testing Firestore Service (dummy test)...")
        
        # Example of creating a profile
        mock_profile = RestaurantProfile(
            place_id="test-place-id-12345",
            name="The Mock Restaurant",
            address="123 Mockingbird Lane",
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            trust_level="high",
            menu_items=[],
            review_summary="A great place for testing."
        )
        
        # Test save
        # Note: This will write to your actual Firestore database if credentials are set up.
        # Use with caution.
        # success = save_restaurant_profile(mock_profile)
        # print(f"Save successful: {success}")

        # Test get
        # profile_from_db = get_restaurant_profile("test-place-id-12345")
        # if profile_from_db:
        #     print(f"Successfully fetched profile: {profile_from_db.name}")
        #     print(f"Profile trust level: {profile_from_db.trust_level}")
        # else:
        #     print("Could not fetch profile (or it's stale/non-existent, which is expected if not saved).")

    test_firestore_service()