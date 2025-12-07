import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Explicitly set the project ID
PROJECT_ID = "gen-lang-client-0415289079"

# Initialize Firestore
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': PROJECT_ID,
        })
    except Exception as e:
        print(f"Error initializing firebase app: {e}")
        pass

try:
    db = firestore.client()
    print(f"Successfully connected to Firestore project: {PROJECT_ID}")
except Exception as e:
    print(f"Error connecting to Firestore: {e}")
    exit(1)

def list_all_restaurants():
    print("Listing top 20 documents in 'restaurant_profiles'...")
    docs = db.collection('restaurant_profiles').limit(20).stream()
    count = 0
    for doc in docs:
        count += 1
        data = doc.to_dict()
        name = data.get('restaurant_name') or data.get('name') or "Unknown"
        print(f"- ID: {doc.id}, Name: {name}, Status: {data.get('status')}")
    
    if count == 0:
        print("No documents found in 'restaurant_profiles'.")

if __name__ == "__main__":
    list_all_restaurants()
