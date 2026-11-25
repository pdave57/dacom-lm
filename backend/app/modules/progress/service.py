from sqlalchemy.orm import Session

from app.modules.progress.schemas import LessonProgressResponse, LessonProgressUpdate


class ProgressService:
    @staticmethod
    def upsert_lesson_progress(
        db: Session, user_id: str, payload: LessonProgressUpdate
    ) -> LessonProgressResponse:
        return LessonProgressResponse(
            lesson_id=payload.lesson_id,
            is_completed=payload.is_completed,
            video_position_seconds=payload.video_position_seconds,
        )
