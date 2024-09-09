import os
import time
import uuid
from typing import Dict, Any

from wrapt import wrap_function_wrapper

from zenetics.client import APIClient
from zenetics.types import Result, Message, Prompt, InputContext, Completion, Session

try:
    import openai
except ImportError:
    raise ImportError(
        "Please install the OpenAI Python package using `pip install openai`"
    )


class Zenetics:
    def __init__(self, api_key: str, app_id: str, api_client: APIClient):
        self.api_key = api_key
        self.app_id = app_id
        self.api_client = api_client

    def capture(self, request, result, latency_milliseconds: int):

        session_result = None
        input_context = []

        if len(result.choices) > 0:
            session_result = Result(
                content=result.choices[0].message.content,
                content_type="text",
            )

        opts_input_context = request.get("opts", {}).get("inputContext")

        if opts_input_context:
            input_context = [
                InputContext(
                    label=context.get("label"),
                    data_json=context.get("dataJson"),
                )
                for context in opts_input_context
            ]

        completion = Completion(
            id=str(uuid.uuid4()),
            type="text",
            model_params=request["model_params"],
            usage={
                "completionTokens": result.usage.completion_tokens,
                "promptTokens": result.usage.prompt_tokens,
                "totalTokens": result.usage.total_tokens,
                "latencyMilliseconds": latency_milliseconds,
            },
            prompt=Prompt(
                version="1.0",
                messages=[
                    Message(
                        role=message["role"],
                        content=message["content"],
                        version="1.0",
                    )
                    for message in request["messages"]
                ],
            ),
            result=session_result,
            input_context=input_context,
        )

        session = Session(
            id=str(uuid.uuid4()),
            completions=[completion],
        )

        self.api_client.post(session.to_dict(), self.api_key, self.app_id)


api_key = os.environ.get("ZENETICS_API_KEY")
app_id = os.environ.get("ZENETICS_APP_ID")
host = os.environ.get("ZENETICS_HOST")

if not api_key:
    raise ValueError("ZENETICS_API_KEY environment variable is required")

if not app_id:
    raise ValueError("ZENETICS_APP_ID environment variable is required")

if not host:
    host = "https://api.zenetics.io"

api_client = APIClient(host)

zenetics = Zenetics(api_key, app_id, api_client)


def format_model_params(opts: Dict[str, Any]) -> Dict[str, str]:
    """
    Format model parameters to be sent to Zenetics API.
    This is a helper function to convert the model parameters to string
    :param opts:
    :return: model_params: Dict[str, str]
    """
    model_params = dict()
    for key, value in opts.items():
        model_params[key] = str(value)

    return model_params


def extract_args(kwargs):
    opts = kwargs.copy()

    zenetics_opts = opts.pop("zenetics_opts", {})

    forward_opts = opts.copy()

    messages = opts.pop("messages", [])
    params = format_model_params(opts)

    request = {
        "opts": zenetics_opts,
        "messages": messages,
        "model_params": params,
    }

    return request, forward_opts


def trace_function(wrapped, instance, args, kwargs):
    request, forward_kwargs = extract_args(kwargs)

    start = time.time()
    result = wrapped(*args, **forward_kwargs)
    latency_milliseconds = (time.time() - start) * 1000

    zenetics.capture(request, result, int(latency_milliseconds))
    return result


wrap_function_wrapper(
    "openai.resources.chat.completions",
    "Completions.create",
    trace_function,
)
