# Project Specification: Staging Deployment on Cloud Run

## 1. System Overview

The goal is to deploy the "OderWhat - AI Dining Agent" application to a staging environment on Google Cloud Run. This will provide a stable, production-like environment for end-to-end testing, bypassing local environment inconsistencies.

## 2. Key Components & Tech Stack

| Component | Technology/Service | Purpose |
| :--- | :--- | :--- |
| **Containerization** | **Docker** | Package the FastAPI application and its dependencies into a portable container image. |
| **CI/CD** | **Google Cloud Build** | Automate the process of building the Docker image and deploying it to Cloud Run. |
| **Hosting** | **Google Cloud Run** | A serverless platform to run our containerized application. |
| **Secret Management** | **Google Secret Manager** | Securely store and manage API keys (`GEMINI_API_KEY`, `APIFY_API_TOKEN`). |
| **Image Storage** | **Google Artifact Registry** | Store the built Docker container images. |

## 3. Deployment Flow

The deployment process will be automated via Cloud Build and triggered by a single `gcloud` command.

1.  A developer (or AI agent) with appropriate permissions runs `gcloud builds submit`.
2.  Cloud Build reads the `cloudbuild.yaml` file.
3.  **Build Step**: Cloud Build uses the `Dockerfile` to build the application container image.
4.  **Push Step**: The newly built image is pushed to the Google Artifact Registry.
5.  **Deploy Step**: Cloud Build deploys the image to a Cloud Run service, injecting the necessary secrets from Secret Manager as environment variables.
6.  The staging endpoint becomes available for testing.

## 4. Core Requirements

-   The final deployment must expose the FastAPI application via a public HTTPS URL provided by Cloud Run.
-   All sensitive keys must be managed by Secret Manager and not be present in the source code or container image.
-   The process should be repeatable and triggered by a single command.
-   The Cloud Run service should be configured with appropriate, but minimal, resources to start with.

