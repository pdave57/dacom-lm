import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.shared.enums import CertificateStatus


class CertificationProgramme(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certification_programmes"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class CertificationRequirement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certification_requirements"

    certification_programme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("certification_programmes.id", ondelete="CASCADE"),
        index=True,
    )
    requirement_type: Mapped[str] = mapped_column(String(80), nullable=False)
    threshold: Mapped[str] = mapped_column(String(80), nullable=False)


class Certificate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certificates"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    certification_programme_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("certification_programmes.id", ondelete="CASCADE"),
        index=True,
    )
    certificate_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default=CertificateStatus.ACTIVE.value, nullable=False
    )


class CertificateVerification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certificate_verifications"

    certificate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("certificates.id", ondelete="CASCADE"), index=True
    )
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
