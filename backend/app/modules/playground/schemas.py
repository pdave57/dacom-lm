import uuid
from typing import Optional

from pydantic import BaseModel


class FrontendExecuteRequest(BaseModel):
    html: str = ""
    css: str = ""
    javascript: str = ""


class PythonExecuteRequest(BaseModel):
    code: str
    stdin: Optional[str] = None


class SQLExecuteRequest(BaseModel):
    query: str
    dataset_id: Optional[uuid.UUID] = None


class ExecutionResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
