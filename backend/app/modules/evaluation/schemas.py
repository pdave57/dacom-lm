import uuid

from pydantic import BaseModel


class EvaluationSummaryResponse(BaseModel):
    submission_id: uuid.UUID
    total_score: float
    status: str
