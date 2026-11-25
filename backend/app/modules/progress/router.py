from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, get_current_user
from app.database.session import get_db
from app.modules.progress.schemas import LessonProgressResponse, LessonProgressUpdate
from app.modules.progress.service import ProgressService

router = APIRouter(tags=["Learning Progress"])


@router.post("/lesson-progress", response_model=LessonProgressResponse)
def update_lesson_progress(
    payload: LessonProgressUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonProgressResponse:
    return ProgressService.upsert_lesson_progress(db, current_user.user_id, payload)
