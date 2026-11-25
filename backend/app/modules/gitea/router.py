from fastapi import APIRouter, Depends

from app.core.dependencies import CurrentUser, get_current_user
from app.modules.gitea.schemas import GiteaRepoValidationRequest, GiteaRepoValidationResponse
from app.modules.gitea.service import GiteaService

router = APIRouter(prefix="/gitea", tags=["Gitea Integration"])


@router.post("/validate", response_model=GiteaRepoValidationResponse)
def validate_repository(
    payload: GiteaRepoValidationRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> GiteaRepoValidationResponse:
    return GiteaService.validate_repository(payload)
