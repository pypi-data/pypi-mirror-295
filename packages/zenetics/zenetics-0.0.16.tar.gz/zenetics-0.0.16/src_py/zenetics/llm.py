import contextlib
import logging
import uuid
from typing import Dict, TypeVar, Optional

from openai import OpenAI

from zenetics.client import APIClient

ChatCompletion = TypeVar("ChatCompletion")

logger = logging.getLogger("zenetics_sdk")


def lens_payload(
    kwargs: Dict, response: ChatCompletion, session_id: Optional[str] = None
) -> Dict:

    result = {}

    if len(response.choices) > 0:
        result = {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
        }

    session = {
        "id": session_id or str(uuid.uuid4()),
        "applicationId": "default",
        "completions": [
            {
                "messages": kwargs["messages"],
                "model": kwargs["model"],
                "result": result,
            }
        ],
    }

    return session


class LLMClient:
    def __init__(self, api_key: str):
        """
        TODO: check compatible OpenAI version
        """
        self.api_key = api_key
        self.api_client = APIClient("http://localhost:8080")

    @contextlib.contextmanager
    def capture_session(self, client: OpenAI):
        def wrapper(*args, **kwargs) -> ChatCompletion:
            # TODO check for lens_capture flag
            # TODO record time
            # TODO record session
            completion = create(*args, **kwargs)

            payload = lens_payload(kwargs, completion)

            self.api_client.post(payload)

            return completion

        create = client.chat.completions.create
        try:
            client.chat.completions.create = wrapper
            yield
        finally:
            client.chat.completions.create = create
