from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import uuid

class Resume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    resume_text: str
    parsed_skills: List[str] = []
    parsed_experience: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None  # 'text' or 'pdf'
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ResumeCreate(BaseModel):
    resume_text: Optional[str] = None
    file_content: Optional[str] = None  # base64 encoded
    file_name: Optional[str] = None