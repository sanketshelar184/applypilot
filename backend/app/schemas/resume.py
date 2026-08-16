from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    title: str = Field(default="My Resume", min_length=1, max_length=160)
    target_role: str | None = Field(default=None, max_length=160)


class ResumeResponse(BaseModel):
    id: str
    title: str
    target_role: str | None
    status: str
    is_master: bool
    created_at: datetime
    updated_at: datetime

