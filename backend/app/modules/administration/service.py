from app.modules.administration.schemas import AdminDashboardStats


class AdministrationService:
    @staticmethod
    def get_dashboard_stats() -> AdminDashboardStats:
        return AdminDashboardStats()
