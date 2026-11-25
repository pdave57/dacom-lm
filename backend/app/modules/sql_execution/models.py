import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import ExecutionStatus


class SQLExerciseEnvironment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sql_exercise_environments"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    init_sql: Mapped[str] = mapped_column(Text, nullable=False)


class SQLDataset(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sql_datasets"

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    seed_sql: Mapped[str] = mapped_column(Text, nullable=False)


class SQLExecutionJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sql_execution_jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    query: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ExecutionStatus.QUEUED.value)


class SQLExecutionResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sql_execution_results"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sql_execution_jobs.id", ondelete="CASCADE"), index=True
    )
    rows_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
