import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class NotificationTemplate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notification_templates"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)


class Announcement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)


class AuditLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(150), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)


class SystemSetting(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)


class IntegrationSetting(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "integration_settings"

    provider: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    config_json: Mapped[str] = mapped_column(Text, nullable=False)
