import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Raid(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raids"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), default="intermediate", nullable=False)


class RaidRequirement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_requirements"

    raid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raids.id", ondelete="CASCADE"), index=True
    )
    requirement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class RaidDeliverable(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_deliverables"

    raid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raids.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)


class RaidRubric(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_rubrics"

    raid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raids.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)


class RaidRubricCriterion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_rubric_criteria"

    rubric_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_rubrics.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    weight_percentage: Mapped[float] = mapped_column(Float, nullable=False)


class RaidAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_assignments"

    raid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raids.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )


class RaidSubmission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_submissions"

    raid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raids.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    repository_url: Mapped[str] = mapped_column(String(500), nullable=False)
    branch_name: Mapped[str] = mapped_column(String(120), nullable=False)
    commit_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    deployment_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="submitted", nullable=False)


class RaidRepository(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "raid_repositories"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raid_submissions.id", ondelete="CASCADE"), index=True
    )
    repo_full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    default_branch: Mapped[str] = mapped_column(String(120), default="main", nullable=False)
