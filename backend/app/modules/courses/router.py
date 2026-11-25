from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.courses.schemas import CourseModuleResponse, CourseResponse
from app.shared.pagination import PaginationParams

router = APIRouter(tags=["Courses & Modules"])


@router.get("/courses", response_model=list[CourseResponse])
def list_courses(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[CourseResponse]:
    return []


@router.get("/modules", response_model=list[CourseModuleResponse])
def list_modules(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[CourseModuleResponse]:
    return []
