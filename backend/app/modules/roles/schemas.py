import uuid
from typing import Optional

from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class AssignRoleRequest(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID
