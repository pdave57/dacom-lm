import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.certification.schemas import (
    CertificateResponse,
    CertificateVerificationResponse,
)
from app.modules.certification.service import CertificationService
from app.shared.enums import CertificateStatus

router = APIRouter(prefix="/certificates", tags=["Certification"])


@router.get("", response_model=list[CertificateResponse])
def list_certificates(
    current_user: CurrentUser = Depends(get_current_user),
) -> list[CertificateResponse]:
    return []


@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
) -> CertificateResponse:
    return CertificateResponse(
        id=certificate_id,
        certificate_number="DACOM-CERT-0001",
        title="FastAPI Development",
        issued_at=datetime.now(timezone.utc),
        status=CertificateStatus.ACTIVE.value,
    )


@router.get("/verify/{certificate_number}", response_model=CertificateVerificationResponse)
def verify_certificate(certificate_number: str) -> CertificateVerificationResponse:
    return CertificationService.verify_certificate(certificate_number)
