import uuid
from typing import Optional

from pydantic import BaseModel


class CourseResponse(BaseModel):
    id: uuid.UUID
    learning_path_id: uuid.UUID
    title: str
    slug: str
    description: Optional[str] = None
    status: str
    display_order: int

    model_config = {"from_attributes": True}


class CourseModuleResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    description: Optional[str] = None
    display_order: int

    model_config = {"from_attributes": True}
