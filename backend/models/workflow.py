from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

class WorkflowExecution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    workflow_config: Dict[str, Any]
    status: str  # 'pending', 'running', 'completed', 'failed'
    jobs_found: int = 0
    jobs_matched: int = 0
    email_sent: bool = False
    error_message: Optional[str] = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class WorkflowRequest(BaseModel):
    resume_id: str
    job_sources: list[str] = Field(default=["linkedin", "indeed", "jobrights", "startups_gallery", "briansjobs", "glassdoor", "ycombinator", "wellfound"])
    send_email: bool = True