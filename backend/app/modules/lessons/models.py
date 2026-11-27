import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import ContentStatus


class Lesson(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lessons"

    module_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("course_modules.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ContentStatus.DRAFT.value, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class LessonContent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_contents"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)


class LessonVideo(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_videos"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    video_url: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class LessonAudio(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_audios"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    voice: Mapped[str] = mapped_column(String(64), default="alloy", nullable=False)
    language: Mapped[str] = mapped_column(String(32), default="en", nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="queued", nullable=False)
    source_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)


class LessonResource(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_resources"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)


class CodeSnippet(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "code_snippets"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str | None] = mapped_column(Text, nullable=True)


class SQLSnippet(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sql_snippets"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), index=True
    )
    query: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str | None] = mapped_column(Text, nullable=True)
