import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import MentorshipStatus


class Mentor(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentors"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MentorSpecialization(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentor_specializations"

    mentor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"), index=True
    )
    area: Mapped[str] = mapped_column(String(100), nullable=False)


class MentorshipRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentorship_requests"

    participant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    repository_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=MentorshipStatus.SUBMITTED.value, nullable=False
    )


class MentorAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentor_assignments"

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), index=True
    )
    mentor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"), index=True
    )


class MentorshipMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentorship_messages"

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), index=True
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)


class MentorshipAttachment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentorship_attachments"

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), index=True
    )
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)


class CodeReview(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "code_reviews"

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), index=True
    )
    mentor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"), index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)


class MentorFeedback(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentor_feedback"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("code_reviews.id", ondelete="CASCADE"), index=True
    )
    guidance: Mapped[str] = mapped_column(Text, nullable=False)


class MentorshipRating(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mentorship_ratings"

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mentorship_requests.id", ondelete="CASCADE"), index=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
