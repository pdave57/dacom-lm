import uuid

from sqlalchemy.orm import Session

from app.modules.lessons.models import Lesson
from app.modules.lessons.schemas import LessonAudioGenerateRequest, LessonAudioResponse


class LessonService:
    @staticmethod
    def list_lessons(db: Session, offset: int = 0, limit: int = 20) -> list[Lesson]:
        return db.query(Lesson).offset(offset).limit(limit).all()

    @staticmethod
    def generate_lesson_audio(
        db: Session, lesson_id: uuid.UUID, payload: LessonAudioGenerateRequest
    ) -> LessonAudioResponse:
        # TODO: Fetch LessonContent markdown, strip formatting, and enqueue
        # generate_lesson_audio_task via Celery to synthesize AI audio and upload to S3.
        return LessonAudioResponse(
            id=uuid.uuid4(),
            lesson_id=lesson_id,
            audio_url=None,
            voice=payload.voice,
            language=payload.language,
            duration_seconds=0,
            status="queued",
        )

    @staticmethod
    def get_lesson_audio(db: Session, lesson_id: uuid.UUID) -> LessonAudioResponse:
        return LessonAudioResponse(
            id=uuid.uuid4(),
            lesson_id=lesson_id,
            audio_url=None,
            voice="alloy",
            language="en",
            duration_seconds=0,
            status="pending",
        )
