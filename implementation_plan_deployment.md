# Implementation Plan: Staging Deployment on Cloud Run

This document outlines the phased plan to containerize and deploy the application to a staging environment on Google Cloud Run.

---

## Phase 1: Containerization

**Goal**: Prepare a `Dockerfile` that correctly builds a runnable container image for our FastAPI application.

**Key Tasks**:
1.  **Analyze Existing Dockerfile**: Review the `Dockerfile` in the root directory to understand its current state.
2.  **Ensure Dependencies**: Verify that the Dockerfile copies `requirements.txt` and runs `pip install -r requirements.txt` in a Python environment.
3.  **Expose Port**: Cloud Run expects applications to listen for requests on port `8080`. The `uvicorn` command in the Dockerfile must be configured to use this port.
4.  **Startup Command**: Ensure the `CMD` or `ENTRYPOINT` instruction correctly starts the FastAPI application using `uvicorn`. The command should be `uvicorn main:app --host 0.0.0.0 --port 8080`.
5.  **.dockerignore**: Create a `.dockerignore` file to exclude unnecessary files and directories (like `.git`, `__pycache__`, `venv/`) from the Docker build context, resulting in a smaller and more secure image.

---

## Phase 2: Secret Management Setup

**Goal**: Securely store API keys in Google Secret Manager and prepare them for injection into the Cloud Run service.

**Key Tasks**:
1.  **Provide Instructions**: I will provide the user with the necessary `gcloud` commands to create secrets for `GEMINI_API_KEY` and `APIFY_API_TOKEN` in Google Secret Manager.
2.  **Grant Permissions**: I will also provide the command for granting the Cloud Build service account the necessary permissions to access these secrets during deployment.

---

## Phase 3: Cloud Build Pipeline (CI/CD)

**Goal**: Create a `cloudbuild.yaml` file to define the automated build and deployment pipeline.

**Key Tasks**:
1.  **Create `cloudbuild.yaml`**: Create a new file named `cloudbuild.yaml` in the project root.
2.  **Define Build Step**: Add a step using the `gcr.io/cloud-builders/docker` builder to build the container image from our `Dockerfile`. The image will be tagged with the build ID and pushed to Google Artifact Registry.
3.  **Define Deploy Step**: Add a step using the `gcr.io/google.com/cloudsdktool/cloud-sdk` builder to deploy the image from Artifact Registry to Cloud Run.
4.  **Inject Secrets**: The deploy step will include arguments to link the secrets created in Phase 2 to the corresponding environment variables (`GEMINI_API_KEY`, `APIFY_API_TOKEN`) in the new Cloud Run service revision.

---

## Phase 4: Deployment Trigger & Verification

**Goal**: Provide a single command to trigger the deployment and instructions for verifying the result.

**Key Tasks**:
1.  **Provide Command**: I will provide the final `gcloud builds submit` command that kicks off the entire Cloud Build pipeline.
2.  **Verification**: After the deployment is complete, I will guide the user on how to find the public URL for the new staging service and how to test it (e.g., using `curl`).
