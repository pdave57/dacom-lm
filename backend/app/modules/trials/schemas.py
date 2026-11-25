import uuid
from typing import Optional

from pydantic import BaseModel


class TrialResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    language: str
    duration_minutes: int
    passing_score: float

    model_config = {"from_attributes": True}


class TrialStartResponse(BaseModel):
    attempt_id: uuid.UUID
    trial_id: uuid.UUID
    status: str = "in_progress"


class TrialExecuteRequest(BaseModel):
    question_id: uuid.UUID
    source_code: str


class TrialSubmitRequest(BaseModel):
    attempt_id: uuid.UUID


class TrialResultResponse(BaseModel):
    attempt_id: uuid.UUID
    score: float
    passed: bool
    feedback: Optional[str] = None
