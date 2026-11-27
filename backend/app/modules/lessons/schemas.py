import uuid
from typing import Optional

from pydantic import BaseModel


class LessonResponse(BaseModel):
    id: uuid.UUID
    module_id: uuid.UUID
    title: str
    slug: str
    status: str
    display_order: int

    model_config = {"from_attributes": True}


class LessonAudioGenerateRequest(BaseModel):
    voice: str = "alloy"
    language: str = "en"


class LessonAudioResponse(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    audio_url: Optional[str] = None
    voice: str
    language: str
    duration_seconds: int = 0
    status: str

    model_config = {"from_attributes": True}
