import uuid
from typing import Optional

from pydantic import BaseModel


class PythonSandboxRequest(BaseModel):
    code: str
    timeout_seconds: int = 5


class PythonSandboxResult(BaseModel):
    job_id: uuid.UUID
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    task_id: Optional[str] = None
