import os
from google.cloud import firestore
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import json

# Initialize Firestore
# Note: We use google.cloud.firestore directly to specify database
db = firestore.Client(project='gen-lang-client-0415289079', database='carted-data')
bq_client = bigquery.Client(project='gen-lang-client-0415289079')

DATASET_ID = "carte_analytics"

def sync_users():
    print("Syncing Users...")
    users_ref = db.collection("users")
    docs = users_ref.stream()
    
    rows = []
    for doc in docs:
        data = doc.to_dict()
        data['user_id'] = doc.id
        # Convert timestamps
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        
        # Handle feedback_history (array of dicts)
        if 'feedback_history' in data:
            data['feedback_history'] = json.dumps(data['feedback_history'], default=str)
            
        rows.append(data)
        
    if not rows:
        print("No users found.")
        return

    df = pd.DataFrame(rows)
    
    # Upload to BigQuery
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", # Overwrite for now (simple sync)
        autodetect=True
    )
    job = bq_client.load_table_from_dataframe(
        df, f"{DATASET_ID}.users_raw", job_config=job_config
    )
    job.result()
    print(f"Synced {len(rows)} users to BigQuery.")

def sync_sessions():
    print("Syncing Sessions...")
    # This is tricky because sessions are subcollections.
    # We need to query all users first, or use a Collection Group query if index exists.
    # Let's try Collection Group 'sessions'
    sessions_ref = db.collection_group("sessions")
    docs = sessions_ref.stream()
    
    rows = []
    for doc in docs:
        data = doc.to_dict()
        data['recommendation_id'] = doc.id
        data['user_id'] = doc.reference.parent.parent.id # Get parent user ID
        
        # Convert timestamps
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        
        # Serialize complex objects
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                data[key] = json.dumps(value, default=str)
                
        rows.append(data)
        
    if not rows:
        print("No sessions found.")
        return

    df = pd.DataFrame(rows)
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
    job = bq_client.load_table_from_dataframe(
        df, f"{DATASET_ID}.sessions_raw", job_config=job_config
    )
    job.result()
    print(f"Synced {len(rows)} sessions to BigQuery.")

def sync_activities():
    print("Syncing Activities...")
    activities_ref = db.collection_group("activities")
    docs = activities_ref.stream()
    
    rows = []
    for doc in docs:
        data = doc.to_dict()
        data['activity_id'] = doc.id
        data['user_id'] = doc.reference.parent.parent.id
        
        # Ensure common fields exist to guarantee BigQuery schema
        for field in ['query', 'type', 'timestamp']:
            if field not in data:
                data[field] = None
            elif field == 'timestamp' and data[field] is not None:
                # Force string to avoid INT64/TIMESTAMP confusion
                if isinstance(data[field], datetime):
                    data[field] = data[field].isoformat()
                else:
                    data[field] = str(data[field])
        
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
                
        rows.append(data)
        
    if not rows:
        print("No activities found.")
        return

    df = pd.DataFrame(rows)
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
    job = bq_client.load_table_from_dataframe(
        df, f"{DATASET_ID}.activities_raw", job_config=job_config
    )
    job.result()
    print(f"Synced {len(rows)} activities to BigQuery.")

def create_views():
    print("Creating Views...")
    
    # View: Searches
    view_searches_query = f"""
    CREATE OR REPLACE VIEW `{DATASET_ID}.view_searches` AS
    SELECT
        activity_id,
        user_id,
        query as search_query,
        CASE
          WHEN SAFE_CAST(timestamp AS INT64) IS NOT NULL THEN TIMESTAMP_SECONDS(CAST(timestamp AS INT64))
          ELSE TIMESTAMP(CAST(timestamp AS STRING))
        END as created_at
    FROM
        `{DATASET_ID}.activities_raw`
    WHERE
        type = 'search'
    """
    bq_client.query(view_searches_query).result()
    
    # View: Sessions
    view_sessions_query = f"""
    CREATE OR REPLACE VIEW `{DATASET_ID}.view_sessions` AS
    SELECT
        recommendation_id,
        user_id,
        restaurant_name,
        restaurant_cuisine_type as cuisine_type,
        initial_total_price,
        final_total_price,
        CASE
          WHEN SAFE_CAST(created_at AS INT64) IS NOT NULL THEN TIMESTAMP_SECONDS(CAST(created_at AS INT64))
          ELSE TIMESTAMP(CAST(created_at AS STRING))
        END as created_at,
        CASE
          WHEN SAFE_CAST(finalized_at AS INT64) IS NOT NULL THEN TIMESTAMP_SECONDS(CAST(finalized_at AS INT64))
          ELSE TIMESTAMP(CAST(finalized_at AS STRING))
        END as finalized_at,
        (finalized_at IS NOT NULL) as is_converted
    FROM
        `{DATASET_ID}.sessions_raw`
    """
    bq_client.query(view_sessions_query).result()

    # View: Dashboard Funnel (Daily Stats)
    view_funnel_query = f"""
    CREATE OR REPLACE VIEW `{DATASET_ID}.view_dashboard_funnel` AS
    WITH daily_searches AS (
        SELECT DATE(created_at) as date, COUNT(*) as search_count 
        FROM `{DATASET_ID}.view_searches` 
        GROUP BY 1
    ),
    daily_orders AS (
        SELECT DATE(created_at) as date, COUNT(*) as recommendation_count, COUNTIF(is_converted) as order_count 
        FROM `{DATASET_ID}.view_sessions` 
        GROUP BY 1
    ),
    daily_new_users AS (
        SELECT DATE(first_seen) as date, COUNT(*) as new_user_count
        FROM (
            SELECT user_id, MIN(created_at) as first_seen
            FROM `{DATASET_ID}.view_sessions`
            GROUP BY user_id
        )
        GROUP BY 1
    )
    SELECT
      COALESCE(s.date, r.date, u.date) as date,
      IFNULL(u.new_user_count, 0) as new_user_count,
      IFNULL(s.search_count, 0) as search_count,
      IFNULL(r.recommendation_count, 0) as recommendation_count,
      IFNULL(r.order_count, 0) as order_count,
      IFNULL(r.recommendation_count, 0) / NULLIF(s.search_count, 0) as conversion_search_to_rec,
      IFNULL(r.order_count, 0) / NULLIF(r.recommendation_count, 0) as conversion_rec_to_order
    FROM daily_searches s
    FULL OUTER JOIN daily_orders r ON s.date = r.date
    FULL OUTER JOIN daily_new_users u ON COALESCE(s.date, r.date) = u.date
    ORDER BY 1 DESC
    """
    bq_client.query(view_funnel_query).result()

    # View: Dashboard Feedback (Enriched)
    view_feedback_enriched_query = f"""
    CREATE OR REPLACE VIEW `{DATASET_ID}.view_dashboard_feedback` AS
    SELECT
      f.*,
      s.restaurant_name,
      s.cuisine_type,
      s.final_total_price,
      s.created_at as session_time
    FROM `{DATASET_ID}.view_feedback` f
    LEFT JOIN `{DATASET_ID}.view_sessions` s
    ON f.recommendation_id = s.recommendation_id
    """
    bq_client.query(view_feedback_enriched_query).result()
    print("Dashboard Views created successfully.")
    
    # View: Feedback
    # Note: feedback_history is a JSON string in our raw table because of pandas export
    view_feedback_query = f"""
    CREATE OR REPLACE VIEW `{DATASET_ID}.view_feedback` AS
    SELECT
        user_id,
        CAST(JSON_EXTRACT_SCALAR(feedback, '$.rating') AS INT64) as rating,
        JSON_EXTRACT_SCALAR(feedback, '$.comment') as comment,
        JSON_EXTRACT_SCALAR(feedback, '$.product_feedback') as product_feedback,
        JSON_EXTRACT_SCALAR(feedback, '$.recommendation_id') as recommendation_id
    FROM
        `{DATASET_ID}.users_raw`,
        UNNEST(JSON_EXTRACT_ARRAY(feedback_history)) as feedback
    """
    bq_client.query(view_feedback_query).result()
    print("Views created successfully.")

if __name__ == "__main__":
    try:
        # Create dataset if not exists
        dataset = bigquery.Dataset(f"{bq_client.project}.{DATASET_ID}")
        dataset.location = "asia-east1"
        try:
            bq_client.create_dataset(dataset, exists_ok=True)
            print(f"Dataset {DATASET_ID} created.")
        except Exception as e:
            print(f"Dataset creation warning: {e}")

        # Delete tables to reset schema
        bq_client.delete_table(f"{DATASET_ID}.users_raw", not_found_ok=True)
        bq_client.delete_table(f"{DATASET_ID}.sessions_raw", not_found_ok=True)
        bq_client.delete_table(f"{DATASET_ID}.activities_raw", not_found_ok=True)

        sync_users()
        sync_sessions()
        sync_activities()
        create_views()
        print("Sync complete!")
    except Exception as e:
        print(f"Sync failed: {e}")
