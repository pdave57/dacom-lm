import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Trial(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trials"

    course_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)


class TrialQuestion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trial_questions"

    trial_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), index=True
    )
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    points: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)


class TestCase(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "test_cases"

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trial_questions.id", ondelete="CASCADE"), index=True
    )
    input_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class TrialAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trial_assignments"

    trial_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )


class TrialAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trial_attempts"

    trial_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="in_progress", nullable=False)


class CodeSubmission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "code_submissions"

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trial_attempts.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trial_questions.id", ondelete="CASCADE"), index=True
    )
    source_code: Mapped[str] = mapped_column(Text, nullable=False)


class TrialDataset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trial_datasets"

    trial_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    schema_sql: Mapped[str] = mapped_column(Text, nullable=False)


class TrialScore(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trial_scores"

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trial_attempts.id", ondelete="CASCADE"), index=True
    )
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
