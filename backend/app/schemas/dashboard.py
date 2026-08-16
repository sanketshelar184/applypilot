from datetime import datetime

from pydantic import BaseModel


class RecentResume(BaseModel):
    id: str
    title: str
    target_role: str | None
    status: str
    updated_at: datetime


class DashboardResponse(BaseModel):
    first_name: str
    resume_count: int
    job_match_count: int = 0
    application_count: int = 0
    remaining_credits: int = 0
    current_plan: str
    recent_resumes: list[RecentResume]

