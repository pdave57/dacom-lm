import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import ExecutionStatus


class PlaygroundProject(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "playground_projects"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    environment_type: Mapped[str] = mapped_column(String(50), nullable=False)


class PlaygroundExercise(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "playground_exercises"

    lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    starter_code: Mapped[str | None] = mapped_column(Text, nullable=True)


class PlaygroundSubmission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "playground_submissions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("playground_exercises.id", ondelete="CASCADE"), index=True
    )
    submitted_code: Mapped[str] = mapped_column(Text, nullable=False)


class ExecutionJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "execution_jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    runtime: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ExecutionStatus.QUEUED.value)


class ExecutionResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "execution_results"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("execution_jobs.id", ondelete="CASCADE"), index=True
    )
    stdout: Mapped[str | None] = mapped_column(Text, nullable=True)
    stderr: Mapped[str | None] = mapped_column(Text, nullable=True)


class FrontendExerciseEnvironment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "frontend_exercise_environments"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("playground_exercises.id", ondelete="CASCADE"), index=True
    )
    html_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    css_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    js_template: Mapped[str | None] = mapped_column(Text, nullable=True)
