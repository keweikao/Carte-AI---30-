
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'gen-lang-client-0415289079',
    })

db = firestore.client()

def list_cached_restaurants():
    print("Fetching cached restaurants from Firestore...")
    try:
        docs = db.collection('restaurant_profiles').stream()
        count = 0
        print(f"{'Restaurant Name':<30} | {'Place ID'}")
        print("-" * 50)
        for doc in docs:
            data = doc.to_dict()
            name = data.get('name', 'Unknown')
            place_id = doc.id
            print(f"{name:<30} | {place_id}")
            count += 1
        print("-" * 50)
        print(f"Total cached restaurants: {count}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_cached_restaurants()
