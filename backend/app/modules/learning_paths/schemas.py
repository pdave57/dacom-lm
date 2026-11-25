import uuid
from typing import Optional

from pydantic import BaseModel


class LearningPathResponse(BaseModel):
    id: uuid.UUID
    programme_id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    status: str
    display_order: int

    model_config = {"from_attributes": True}
