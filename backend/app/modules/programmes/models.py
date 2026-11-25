from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import ContentStatus


class Programme(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "programmes"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=ContentStatus.DRAFT.value, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
