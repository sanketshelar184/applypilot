from fastapi import APIRouter
from sqlalchemy import func, select

from app.api.dependencies import CurrentUser, DatabaseSession
from app.models.resume import Resume
from app.schemas.dashboard import DashboardResponse, RecentResume

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
async def dashboard(user: CurrentUser, db: DatabaseSession) -> DashboardResponse:
    count = await db.scalar(select(func.count(Resume.id)).where(Resume.user_id == user.id))
    rows = await db.scalars(
        select(Resume)
        .where(Resume.user_id == user.id)
        .order_by(Resume.updated_at.desc())
        .limit(5)
    )
    return DashboardResponse(
        first_name=user.telegram_account.first_name,
        resume_count=count or 0,
        current_plan=user.subscription_status.value,
        recent_resumes=[
            RecentResume(
                id=str(item.id),
                title=item.title,
                target_role=item.target_role,
                status=item.status.value,
                updated_at=item.updated_at,
            )
            for item in rows
        ],
    )

