# Staging Environment Deployment Guide

This document provides the standard operating procedure (SOP) for deploying the "OderWhat" backend application to the **Staging Environment** on Google Cloud Run.

## 1. Objective

The Staging environment serves as a pre-production testing area. All new features and bug fixes should be deployed to and verified on Staging before being considered for a production release. Its purpose is to mirror the production environment as closely as possible to ensure reliability.

## 2. Architecture Overview

We use a CI/CD (Continuous Integration/Continuous Deployment) approach automated by **Google Cloud Build**. The workflow is as follows:

1.  A developer triggers a new build.
2.  **Cloud Build** reads `cloudbuild.yaml`.
3.  **Build**: A Docker container image is built using the `Dockerfile`.
4.  **Push**: The new image is pushed to our dedicated Staging repository in **Artifact Registry** (`oderwhat-staging-repo`).
5.  **Deploy**: The new image is deployed to the `oderwhat-staging` service on **Cloud Run**, with all necessary secrets automatically injected.

## 3. One-Time Setup (Prerequisites)

The following components must exist in the GCP project (`gen-lang-client-0415289079`). If you are setting up a new project, ensure these are created once:

1.  **Enable APIs**:
    -   Cloud Build API (`cloudbuild.googleapis.com`)
    -   Cloud Run API (`run.googleapis.com`)
    -   Secret Manager API (`secretmanager.googleapis.com`)
    -   Artifact Registry API (`artifactregistry.googleapis.com`)

2.  **Artifact Registry Repository**:
    -   A Docker repository named `oderwhat-staging-repo` must exist in the `asia-east1` region.

3.  **Secret Manager Secrets**:
    -   A secret named `GEMINI_API_KEY` must exist.
    -   A secret named `APIFY_API_TOKEN` must exist.

4.  **IAM Permissions**:
    -   The service account used by the deployment process (e.g., `1045148759148-compute@developer.gserviceaccount.com` as per our setup) must have the `Secret Manager Secret Accessor` role.

---

## 4. How to Deploy to Staging

After you have committed your latest code changes to your Git branch, run the following single command from your local terminal in the project root:

```bash
gcloud builds submit --config=cloudbuild.yaml --project=gen-lang-client-0415289079 --no-user-output-enabled
```

This command will trigger the entire build and deployment pipeline. The process typically takes 5-10 minutes. You can monitor the progress in the **Cloud Build History** page in the Google Cloud Console.

## 5. How to Verify the Deployment

1.  Once the Cloud Build job succeeds, go to the **Cloud Run** service in the Google Cloud Console.
2.  Find the `oderwhat-staging` service.
3.  The main page for the service will display its public **URL**.
4.  You can use a tool like `curl` to test an endpoint. For example, to test the cold start pipeline:

    ```bash
    # Replace YOUR_CLOUD_RUN_URL with the actual URL
    curl -X POST https://YOUR_CLOUD_RUN_URL/api/v1/stream_recommend \
    -H "Content-Type: application/json" \
    -d '{"place_id": "ChIJ-x-t9W_eQjQRhFjU2g08sHk"}'
    ```

---

## 6. Future: Promoting to Production

This same workflow can be adapted for production. A common practice is to create a separate `cloudbuild-prod.yaml` file. Instead of building a new image, this production pipeline would typically re-tag an already-tested Staging image (e.g., `oderwhat-staging:build-id-123`) as a production image and deploy that to a separate `oderwhat-production` Cloud Run service. This ensures the exact code that was tested is what gets deployed.
