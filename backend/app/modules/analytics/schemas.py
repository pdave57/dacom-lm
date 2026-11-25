from pydantic import BaseModel


class ParticipantDashboardSummary(BaseModel):
    overall_progress_percentage: float = 0.0
    enrolled_programmes: int = 0
    active_courses: int = 0
    completed_courses: int = 0
    lessons_completed: int = 0
    certificates_earned: int = 0
