import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RaidReview(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_reviews"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_submissions.id", ondelete="CASCADE"), index=True
    )
    evaluator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)


class RaidFeedback(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_feedback"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_reviews.id", ondelete="CASCADE"), index=True
    )
    comments: Mapped[str] = mapped_column(Text, nullable=False)


class RaidScore(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_scores"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_reviews.id", ondelete="CASCADE"), index=True
    )
    total_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
