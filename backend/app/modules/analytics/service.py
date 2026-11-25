from app.modules.analytics.schemas import ParticipantDashboardSummary


class AnalyticsService:
    @staticmethod
    def get_participant_summary(user_id: str) -> ParticipantDashboardSummary:
        return ParticipantDashboardSummary()
