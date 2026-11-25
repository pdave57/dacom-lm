import uuid

from app.modules.trials.schemas import TrialResultResponse, TrialStartResponse


class TrialService:
    @staticmethod
    def start_trial(trial_id: uuid.UUID) -> TrialStartResponse:
        return TrialStartResponse(attempt_id=uuid.uuid4(), trial_id=trial_id)

    @staticmethod
    def get_result(attempt_id: uuid.UUID) -> TrialResultResponse:
        return TrialResultResponse(attempt_id=attempt_id, score=0.0, passed=False)
