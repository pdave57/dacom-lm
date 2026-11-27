import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, get_current_user
from app.database.session import get_db
from app.modules.lessons.schemas import (
    LessonAudioGenerateRequest,
    LessonAudioResponse,
    LessonResponse,
)
from app.modules.lessons.service import LessonService
from app.shared.pagination import PaginationParams

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("", response_model=list[LessonResponse])
def list_lessons(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> list[LessonResponse]:
    return []


@router.post(
    "/{lesson_id}/audio/generate",
    response_model=LessonAudioResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_lesson_audio(
    lesson_id: uuid.UUID,
    payload: LessonAudioGenerateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonAudioResponse:
    """Queue AI text-to-audio generation from the lesson's written content."""
    return LessonService.generate_lesson_audio(db, lesson_id, payload)


@router.get("/{lesson_id}/audio", response_model=LessonAudioResponse)
def get_lesson_audio(
    lesson_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonAudioResponse:
    """Retrieve generated AI audio metadata and URL for a lesson."""
    return LessonService.get_lesson_audio(db, lesson_id)
