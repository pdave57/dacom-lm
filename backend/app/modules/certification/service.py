from app.modules.certification.schemas import CertificateVerificationResponse
from app.shared.enums import CertificateStatus


class CertificationService:
    @staticmethod
    def verify_certificate(certificate_number: str) -> CertificateVerificationResponse:
        return CertificateVerificationResponse(
            certificate_number=certificate_number,
            valid=True,
            status=CertificateStatus.ACTIVE.value,
        )
