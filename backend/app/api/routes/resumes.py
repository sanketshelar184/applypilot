from fastapi import APIRouter, status
from sqlalchemy import func, select

from app.api.dependencies import CurrentUser, DatabaseSession
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeResponse

router = APIRouter(prefix="/resumes", tags=["Resumes"])


def serialize(resume: Resume) -> ResumeResponse:
    return ResumeResponse(
        id=str(resume.id), title=resume.title, target_role=resume.target_role,
        status=resume.status.value, is_master=resume.is_master,
        created_at=resume.created_at, updated_at=resume.updated_at,
    )


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    payload: ResumeCreate, user: CurrentUser, db: DatabaseSession
) -> ResumeResponse:
    existing = await db.scalar(select(func.count(Resume.id)).where(Resume.user_id == user.id))
    resume = Resume(
        user_id=user.id,
        title=payload.title.strip(),
        target_role=payload.target_role.strip() if payload.target_role else None,
        is_master=(existing or 0) == 0,
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return serialize(resume)


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(user: CurrentUser, db: DatabaseSession) -> list[ResumeResponse]:
    result = await db.scalars(
        select(Resume).where(Resume.user_id == user.id).order_by(Resume.updated_at.desc()).limit(50)
    )
    return [serialize(resume) for resume in result]
