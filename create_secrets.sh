#!/bin/bash
# Create secrets from .env file

# Read .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found!"
    exit 1
fi

# Function to create or update secret
create_secret() {
    local name=$1
    local value=$2
    
    if [ -z "$value" ]; then
        echo "Warning: $name is empty, skipping"
        return
    fi

    echo "Creating/Updating secret: $name"
    
    # Check if secret exists
    if gcloud secrets describe $name --project=sales-ai-automation-v2 > /dev/null 2>&1; then
        echo "Secret exists, adding new version"
        echo -n "$value" | gcloud secrets versions add $name --data-file=- --project=sales-ai-automation-v2
    else
        echo "Creating new secret"
        echo -n "$value" | gcloud secrets create $name --data-file=- --project=sales-ai-automation-v2
    fi
}

create_secret "SERPER_API_KEY" "$SERPER_API_KEY"
create_secret "JINA_API_KEY" "$JINA_API_KEY"
create_secret "GOOGLE_API_KEY" "$GOOGLE_API_KEY"
create_secret "APIFY_API_TOKEN" "$APIFY_API_TOKEN"
create_secret "GEMINI_API_KEY" "$GEMINI_API_KEY"
