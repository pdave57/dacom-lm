from pydantic import BaseModel


class AdminDashboardStats(BaseModel):
    total_participants: int = 0
    active_participants: int = 0
    suspended_participants: int = 0
    registered_mentors: int = 0
    available_programmes: int = 0
    published_courses: int = 0
    published_lessons: int = 0
    active_trials: int = 0
    active_raids: int = 0
    pending_project_reviews: int = 0
    mentorship_requests: int = 0
    certificates_issued: int = 0
