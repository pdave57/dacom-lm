import uuid

from pydantic import BaseModel


class LessonResponse(BaseModel):
    id: uuid.UUID
    module_id: uuid.UUID
    title: str
    slug: str
    status: str
    display_order: int

    model_config = {"from_attributes": True}
