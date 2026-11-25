import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RaidInspection(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_inspections"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_submissions.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="queued", nullable=False)


class RaidInspectionResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_inspection_results"

    inspection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_inspections.id", ondelete="CASCADE"), index=True
    )
    check_name: Mapped[str] = mapped_column(String(120), nullable=False)
    passed: Mapped[bool] = mapped_column(default=False, nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
