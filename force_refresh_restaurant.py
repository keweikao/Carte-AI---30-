import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firestore
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': os.getenv('GOOGLE_CLOUD_PROJECT'),
    })

try:
    db = firestore.client(database="carted-data")
except Exception as e:
    print(f"Error initializing client with database='carted-data': {e}")
    db = firestore.client()

def delete_restaurant_profile(name):
    print(f"Attempting to delete profile for: {name}")
    
    # 1. Search by restaurant_name
    docs = db.collection('restaurants').where('name', '==', name).stream()
    deleted_count = 0
    for doc in docs:
        print(f"Deleting doc {doc.id} (found by restaurant_name)...")
        doc.reference.delete()
        deleted_count += 1
        
    # 2. Search by name (fallback, though 'name' is the field used in save_restaurant_data)
    if deleted_count == 0:
        # In firestore_service, the field is 'name'
        pass 
            
    # 3. Try direct ID
    if deleted_count == 0:
        doc_ref = db.collection('restaurants').document(name)
        if doc_ref.get().exists:
             print(f"Deleting doc {name} (found by ID)...")
             doc_ref.delete()
             deleted_count += 1

    # 4. Try by mock place_id (for testing)
    if deleted_count == 0:
        mock_place_id = "mock_place_id_ye_gong_guan"
        doc_ref = db.collection('restaurants').document(mock_place_id)
        if doc_ref.get().exists:
             print(f"Deleting doc {mock_place_id} (found by Mock ID)...")
             doc_ref.delete()
             deleted_count += 1

    if deleted_count > 0:
        print(f"✅ Successfully deleted {deleted_count} documents for '{name}'. Next run will be a Cold Start.")
    else:
        print(f"⚠️ No documents found for '{name}'.")

if __name__ == "__main__":
    restaurant_name = "葉公館滬菜"
    delete_restaurant_profile(restaurant_name)
