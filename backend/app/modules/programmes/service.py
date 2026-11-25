from sqlalchemy.orm import Session

from app.modules.programmes.models import Programme


class ProgrammeService:
    @staticmethod
    def list_programmes(db: Session, offset: int = 0, limit: int = 20) -> list[Programme]:
        return db.query(Programme).offset(offset).limit(limit).all()
