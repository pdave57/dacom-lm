import uuid
from typing import Optional

from pydantic import BaseModel


class SQLSandboxRequest(BaseModel):
    query: str
    dataset_id: Optional[uuid.UUID] = None


class SQLSandboxResult(BaseModel):
    job_id: uuid.UUID
    status: str
    rows: list[dict] = []
    error_message: Optional[str] = None
    task_id: Optional[str] = None
