import datetime
from services.firestore_service import db

if not db:
    print("Error: Firestore client could not be initialized from services.firestore_service. Please check your authentication.")
    exit()

# Try to fetch one user document to inspect its structure
print("Fetching one user document to inspect its fields...")
try:
    first_user_doc = db.collection('users').limit(1).get()
    if first_user_doc:
        doc_snapshot = first_user_doc[0]
        user_data = doc_snapshot.to_dict()
        print(f"Found user document with ID: {doc_snapshot.id}")
        print("User document fields:")
        for key in user_data.keys():
            print(f"  - {key}")
        if 'created_at' not in user_data:
            print("\nWarning: 'created_at' field not found in this user document. User sign-up date might be stored under a different field name or not at all.")
            # If created_at is not found, try to use 'last_updated' or 'last_active' for the query as a fallback
            # But inform the user that this is not ideal for sign-up count
            if 'last_updated' in user_data:
                print("Falling back to 'last_updated' for counting, but this might not reflect true sign-up count.")
                timestamp_field = 'last_updated'
            elif 'last_active' in user_data:
                print("Falling back to 'last_active' for counting, but this might not reflect true sign-up count.")
                timestamp_field = 'last_active'
            else:
                timestamp_field = None
                print("No suitable timestamp field found for user sign-up count.")
        else:
            timestamp_field = 'created_at'
    else:
        print("No user documents found in the 'users' collection.")
        timestamp_field = None
except Exception as e:
    print(f"Error fetching user document: {e}")
    timestamp_field = None


if timestamp_field:
    # Define the time range
    two_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)
    now = datetime.datetime.now(datetime.timezone.utc)

    # Query the users collection
    users_ref = db.collection('users')
    query = users_ref.where(timestamp_field, '>=', two_days_ago).where(timestamp_field, '<=', now)

    try:
        docs = query.stream()
        user_count = len(list(docs))

        print(f"\n從 {two_days_ago.strftime('%Y-%m-%d %H:%M:%S UTC')} 到現在，總共增加了 {user_count} 位使用者 (使用欄位: '{timestamp_field}')。")

    except Exception as e:
        if 'requires an index' in str(e):
            print("\nError: The query requires a Firestore index that is not present.")
            print(f"Please create a composite index for the 'users' collection on the '{timestamp_field}' field (ascending or descending).")
            print(f"Full error: {e}")
        else:
            print(f"\nAn error occurred during query: {e}")
else:
    print("\nSkipping time-based query because no suitable timestamp field or user documents were found.")