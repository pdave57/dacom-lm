from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, require_roles
from app.modules.roles.schemas import RoleResponse
from app.shared.enums import RoleEnum

router = APIRouter(prefix="/roles", tags=["Roles & Permissions"])


@router.get("", response_model=list[RoleResponse])
def list_roles(
    current_user: CurrentUser = Depends(require_roles(RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN)),
) -> list[RoleResponse]:
    return []
