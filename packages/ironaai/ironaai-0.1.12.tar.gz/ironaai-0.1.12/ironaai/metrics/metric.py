from typing import Optional

from ironaai import settings
from ironaai.exceptions import ApiError
from ironaai.llms.config import LLMConfig
from ironaai.metrics.request import feedback_request
from ironaai.types import IAIApiKeyValidator


class Metric:
    def __init__(self, metric: Optional[str] = "accuracy"):
        self.metric = metric

    def __call__(self):
        return self.metric

    def feedback(
        self,
        session_id: str,
        llm_config: LLMConfig,
        value: int,
        ironaai_api_key: Optional[str] = None,
        _user_agent: str = None,
    ):
        if ironaai_api_key is None:
            ironaai_api_key = settings.IRONAAI_API_KEY
        IAIApiKeyValidator(api_key=ironaai_api_key)
        if value not in [0, 1]:
            raise ApiError("Invalid feedback value. It must be 0 or 1.")

        return feedback_request(
            session_id=session_id,
            llm_config=llm_config,
            feedback_payload=self.request_payload(value),
            ironaai_api_key=ironaai_api_key,
            _user_agent=_user_agent,
        )

    def request_payload(self, value: int):
        return {self.metric: value}
