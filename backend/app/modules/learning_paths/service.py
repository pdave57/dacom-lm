from sqlalchemy.orm import Session

from app.modules.learning_paths.models import LearningPath


class LearningPathService:
    @staticmethod
    def list_learning_paths(db: Session, offset: int = 0, limit: int = 20) -> list[LearningPath]:
        return db.query(LearningPath).offset(offset).limit(limit).all()
