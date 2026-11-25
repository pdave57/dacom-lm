from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.analytics.schemas import ParticipantDashboardSummary
from app.modules.analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/participant-dashboard", response_model=ParticipantDashboardSummary)
def get_participant_dashboard(
    current_user: CurrentUser = Depends(get_current_user),
) -> ParticipantDashboardSummary:
    return AnalyticsService.get_participant_summary(current_user.user_id)
