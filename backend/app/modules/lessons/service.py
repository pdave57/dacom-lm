from sqlalchemy.orm import Session

from app.modules.lessons.models import Lesson


class LessonService:
    @staticmethod
    def list_lessons(db: Session, offset: int = 0, limit: int = 20) -> list[Lesson]:
        return db.query(Lesson).offset(offset).limit(limit).all()
