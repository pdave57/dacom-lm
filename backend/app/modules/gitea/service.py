from app.modules.gitea.schemas import GiteaRepoValidationRequest, GiteaRepoValidationResponse


class GiteaService:
    @staticmethod
    def validate_repository(payload: GiteaRepoValidationRequest) -> GiteaRepoValidationResponse:
        # TODO: Query Gitea REST API with settings.GITEA_BASE_URL and settings.GITEA_API_TOKEN.
        return GiteaRepoValidationResponse(
            valid=True,
            commit_verified=True,
            message="Gitea repository validation scaffold.",
        )
