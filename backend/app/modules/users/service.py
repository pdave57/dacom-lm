from sqlalchemy.orm import Session

from app.modules.users.models import User


class UserService:
    @staticmethod
    def list_users(db: Session, offset: int = 0, limit: int = 20) -> list[User]:
        return db.query(User).offset(offset).limit(limit).all()
