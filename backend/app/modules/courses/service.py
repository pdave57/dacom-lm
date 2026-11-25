from sqlalchemy.orm import Session

from app.modules.courses.models import Course, CourseModule


class CourseService:
    @staticmethod
    def list_courses(db: Session, offset: int = 0, limit: int = 20) -> list[Course]:
        return db.query(Course).offset(offset).limit(limit).all()

    @staticmethod
    def list_modules(db: Session, offset: int = 0, limit: int = 20) -> list[CourseModule]:
        return db.query(CourseModule).offset(offset).limit(limit).all()
