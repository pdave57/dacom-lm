from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, require_roles
from app.modules.administration.schemas import AdminDashboardStats
from app.modules.administration.service import AdministrationService
from app.shared.enums import RoleEnum

router = APIRouter(
    prefix="/admin",
    tags=["Back Office Administration"],
    dependencies=[Depends(require_roles(RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN))],
)


@router.get("/dashboard", response_model=AdminDashboardStats)
def admin_dashboard() -> AdminDashboardStats:
    return AdministrationService.get_dashboard_stats()


@router.get("/participants")
def admin_list_participants() -> list[dict]:
    return []


@router.get("/mentors")
def admin_list_mentors() -> list[dict]:
    return []


@router.get("/programmes")
def admin_list_programmes() -> list[dict]:
    return []


@router.get("/courses")
def admin_list_courses() -> list[dict]:
    return []


@router.get("/trials")
def admin_list_trials() -> list[dict]:
    return []


@router.get("/raids")
def admin_list_raids() -> list[dict]:
    return []


@router.get("/reports")
def admin_reports() -> dict:
    return {"reports": []}


@router.get("/audit-logs")
def admin_audit_logs() -> list[dict]:
    return []


@router.get("/settings")
def admin_settings() -> dict:
    return {"settings": {}}
