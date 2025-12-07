# Task Checklist: Deployment - Phase 1 (Containerization)

This document breaks down the tasks required to complete **Phase 1: Containerization** of the `implementation_plan_deployment.md`.

### 1.1 Analyze Existing Dockerfile
-   [ ] Read the contents of the `Dockerfile` in the project root to understand its current configuration.

### 1.2 Identify Necessary Changes
-   [ ] Check if a `WORKDIR` is set. If not, plan to add one (e.g., `/app`).
-   [ ] Verify that `requirements.txt` is copied into the image.
-   [ ] Verify that `pip install -r requirements.txt` is run.
-   [ ] Check the `EXPOSE` instruction. It should expose port `8080`.
-   [ ] Check the `CMD` or `ENTRYPOINT` instruction. It must start `uvicorn` and bind it to `0.0.0.0:8080`.

### 1.3 Create `.dockerignore`
-   [ ] Check if a `.dockerignore` file exists.
-   [ ] If not, create a `.dockerignore` file.
-   [ ] Add entries to exclude common unnecessary files and directories to keep the image small and secure:
    -   `.git`
    -   `.gitignore`
    -   `__pycache__`
    -   `venv/`
    -   `.env`
    -   `*.pyc`
    -   `*.md` (Readme, specs, etc., are not needed in the final image)

### 1.4 Modify Dockerfile
-   [ ] Based on the analysis in step 1.2, apply the necessary changes to the `Dockerfile`. This will likely involve using `replace` to update the `EXPOSE` and `CMD` lines.
