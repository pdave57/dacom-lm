import uuid
from typing import Optional

from pydantic import BaseModel


class ProgrammeCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    display_order: int = 0


class ProgrammeResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    status: str
    display_order: int

    model_config = {"from_attributes": True}
