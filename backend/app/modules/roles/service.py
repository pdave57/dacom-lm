from sqlalchemy.orm import Session

from app.modules.roles.models import Role


class RoleService:
    @staticmethod
    def list_roles(db: Session) -> list[Role]:
        return db.query(Role).all()
