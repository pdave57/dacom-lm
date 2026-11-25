import uuid
from typing import Optional

from pydantic import BaseModel


class MentorshipRequestCreate(BaseModel):
    title: str
    description: str
    repository_url: Optional[str] = None


class MentorshipRequestResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: str


class MentorshipMessageCreate(BaseModel):
    body: str


class MentorResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    is_available: bool
    specializations: list[str] = []
