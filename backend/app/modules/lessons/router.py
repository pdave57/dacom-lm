from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.lessons.schemas import LessonResponse
from app.shared.pagination import PaginationParams

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("", response_model=list[LessonResponse])
def list_lessons(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[LessonResponse]:
    return []
