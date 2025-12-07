#!/bin/bash

PROJECT_ID="sales-ai-automation-v2"
PROJECT_NUMBER="497329205771"
CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

SECRETS=("SERPER_API_KEY" "JINA_API_KEY" "GOOGLE_API_KEY" "APIFY_API_TOKEN" "GEMINI_API_KEY")

for SECRET in "${SECRETS[@]}"; do
    echo "Granting access to $SECRET..."
    
    # Grant to Cloud Build SA
    gcloud secrets add-iam-policy-binding $SECRET \
        --member="serviceAccount:$CLOUDBUILD_SA" \
        --role="roles/secretmanager.secretAccessor" \
        --project=$PROJECT_ID > /dev/null
        
    # Grant to Compute SA (for Cloud Run)
    gcloud secrets add-iam-policy-binding $SECRET \
        --member="serviceAccount:$COMPUTE_SA" \
        --role="roles/secretmanager.secretAccessor" \
        --project=$PROJECT_ID > /dev/null
done

echo "Access granted!"
