import uuid

from pydantic import BaseModel


class InspectionStatusResponse(BaseModel):
    inspection_id: uuid.UUID
    submission_id: uuid.UUID
    status: str
