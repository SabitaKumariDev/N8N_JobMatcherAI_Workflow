from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str
    source: str  # linkedin, indeed, jobrights, etc.
    title: str
    company: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None
    posted_date: Optional[datetime] = None
    url: str
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class JobMatch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    job_id: str
    match_score: float  # 0-100
    match_reason: str
    matched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))