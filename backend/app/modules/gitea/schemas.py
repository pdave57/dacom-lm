from pydantic import BaseModel


class GiteaRepoValidationRequest(BaseModel):
    repository_url: str
    branch_name: str = "main"
    commit_hash: str


class GiteaRepoValidationResponse(BaseModel):
    valid: bool
    commit_verified: bool
    message: str
