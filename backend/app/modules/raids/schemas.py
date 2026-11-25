import uuid
from typing import Optional

from pydantic import BaseModel


class RaidResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    difficulty: str

    model_config = {"from_attributes": True}


class RaidSubmitRequest(BaseModel):
    project_description: str
    gitea_repo_url: str
    branch_name: str = "main"
    commit_hash: str
    documentation: Optional[str] = None
    deployment_url: Optional[str] = None


class RaidSubmissionResponse(BaseModel):
    id: uuid.UUID
    raid_id: uuid.UUID
    repository_url: str
    branch_name: str
    commit_hash: str
    status: str


class RaidReviewRequest(BaseModel):
    score: float
    feedback: str
    approved: bool = True
