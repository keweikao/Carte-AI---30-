
import datetime
from services.firestore_service import db

if not db:
    print("Error: Firestore client could not be initialized from services.firestore_service. Please check your authentication.")
    exit()

def get_all_user_ids():
    """Fetches all user IDs from the 'users' collection."""
    try:
        users_ref = db.collection('users')
        user_docs = users_ref.stream()
        user_ids = [user.id for user in user_docs]
        return user_ids
    except Exception as e:
        print(f"Error fetching user IDs: {e}")
        return []

def count_searched_restaurants(days=3):
    """Counts the number of unique restaurants searched in the last X days."""
    user_ids = get_all_user_ids()
    if not user_ids:
        print("No users found in the database.")
        return 0

    print(f"Found {len(user_ids)} users. Now checking their search activities...")

    searched_restaurants = set()
    end_date = datetime.datetime.now(datetime.timezone.utc)
    start_date = end_date - datetime.timedelta(days=days)

    for user_id in user_ids:
        try:
            activities_ref = db.collection('users').document(user_id).collection('activities')
            query = activities_ref.where('type', '==', 'search').where('timestamp', '>=', start_date).where('timestamp', '<=', end_date)
            search_activities = query.stream()

            for activity in search_activities:
                activity_data = activity.to_dict().get('data', {})
                if not activity_data:
                    continue
                
                restaurant_name = activity_data.get('restaurant_name') or activity_data.get('query')

                if restaurant_name:
                    searched_restaurants.add(restaurant_name.strip())

        except Exception as e:
            if 'requires an index' in str(e):
                print(f"\nError for user {user_id}: The query requires a Firestore index that is not present.")
                print("Please create a composite index for the 'activities' collection on 'type' and 'timestamp' fields.")
                # We can continue to the next user, but we should let the user know that the result is incomplete.
                print("The final count will be incomplete as some users' activities could not be queried.")
            else:
                print(f"An error occurred while fetching activities for user {user_id}: {e}")
                # We can also decide to stop here if the error is critical
    
    return len(searched_restaurants)

if __name__ == "__main__":
    num_restaurants = count_searched_restaurants(days=3)
    print(f"\n在過去的 3 天內，總共有 {num_restaurants} 間不重複的餐廳被搜尋過。")
