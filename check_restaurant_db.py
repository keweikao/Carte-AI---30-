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
        # Fallback for local dev if ADC is not set but gcloud is
        # Note: This is a bit hacky, usually ADC is preferred.
        pass

try:
    db = firestore.client()
    print(f"Successfully connected to Firestore project: {PROJECT_ID}")
except Exception as e:
    print(f"Error connecting to Firestore: {e}")
    exit(1)

def check_restaurant(name):
    print(f"Checking for restaurant: {name}")
    
    # Check by document ID (assuming name is used as ID or part of it)
    # Also check by 'restaurant_name' field query
    
    found_any = False
    
    # 1. Query by field 'restaurant_name'
    print("--- Querying by 'restaurant_name' field ---")
    docs = db.collection('restaurant_profiles').where('restaurant_name', '==', name).stream()
    for doc in docs:
        found_any = True
        data = doc.to_dict()
        print(f"✅ Found document ID: {doc.id}")
        print(f"   Status: {data.get('status')}")
        print(f"   Last Updated: {data.get('last_updated')}")
        print(f"   Golden Profile: {'Yes' if data.get('golden_profile') else 'No'}")
        
    # 2. Query by field 'name' (legacy check)
    if not found_any:
        print("--- Querying by 'name' field ---")
        docs = db.collection('restaurant_profiles').where('name', '==', name).stream()
        for doc in docs:
            found_any = True
            data = doc.to_dict()
            print(f"✅ Found document ID: {doc.id}")
            print(f"   Status: {data.get('status')}")
            print(f"   Last Updated: {data.get('last_updated')}")
            print(f"   Golden Profile: {'Yes' if data.get('golden_profile') else 'No'}")

    # 3. Check specific ID (sometimes we use name as ID)
    if not found_any:
        print(f"--- Checking document ID '{name}' ---")
        doc_ref = db.collection('restaurant_profiles').document(name)
        doc = doc_ref.get()
        if doc.exists:
            found_any = True
            data = doc.to_dict()
            print(f"✅ Found document ID: {doc.id}")
            print(f"   Status: {data.get('status')}")
            print(f"   Last Updated: {data.get('last_updated')}")
            print(f"   Golden Profile: {'Yes' if data.get('golden_profile') else 'No'}")
            
    if not found_any:
        print(f"❌ Restaurant '{name}' NOT found in database.")

if __name__ == "__main__":
    check_restaurant("葉公館滬菜")
