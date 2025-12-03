import uuid
from datetime import datetime, timezone
from firebase_admin import firestore
from enum import Enum
from typing import Dict, Any, Optional

class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobManager:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection('recommendation_jobs')

    def create_job(self, user_input: Dict[str, Any]) -> str:
        job_id = str(uuid.uuid4())
        job_data = {
            "job_id": job_id,
            "status": JobStatus.PENDING.value,
            "user_input": user_input,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "progress": 0,
            "message": "Job created"
        }
        self.collection.document(job_id).set(job_data)
        return job_id

    def update_status(self, job_id: str, status: JobStatus, progress: int = 0, message: str = "", result: Optional[Dict] = None, error: Optional[str] = None):
        update_data = {
            "status": status.value,
            "updated_at": datetime.now(timezone.utc),
            "progress": progress,
            "message": message
        }
        
        if result:
            update_data["result"] = result
        
        if error:
            update_data["error"] = error
            
        self.collection.document(job_id).update(update_data)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        doc = self.collection.document(job_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

# Global instance
job_manager = JobManager()
