import uuid
from datetime import datetime

from pydantic import BaseModel


class CertificateResponse(BaseModel):
    id: uuid.UUID
    certificate_number: str
    title: str
    issued_at: datetime
    status: str


class CertificateVerificationResponse(BaseModel):
    certificate_number: str
    valid: bool
    status: str
