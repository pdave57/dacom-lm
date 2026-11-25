import uuid

from app.modules.raids.schemas import RaidSubmissionResponse, RaidSubmitRequest


class RaidService:
    @staticmethod
    def submit_raid(raid_id: uuid.UUID, payload: RaidSubmitRequest) -> RaidSubmissionResponse:
        return RaidSubmissionResponse(
            id=uuid.uuid4(),
            raid_id=raid_id,
            repository_url=payload.gitea_repo_url,
            branch_name=payload.branch_name,
            commit_hash=payload.commit_hash,
            status="submitted",
        )
