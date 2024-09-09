from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Result:
    content: str
    content_type: str

    def to_dict(self):
        return {
            "content": self.content,
            "contentType": self.content_type,
        }


@dataclass
class Message:
    role: str
    content: str
    version: str

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "version": self.version,
        }


@dataclass
class Prompt:
    version: str
    messages: List[Message]

    def to_dict(self):
        return {
            "version": self.version,
            "messages": [message.to_dict() for message in self.messages],
        }


@dataclass
class InputContext:
    label: str
    data_json: str

    def to_dict(self):
        return {"label": self.label, "dataJson": self.data_json}


@dataclass
class Completion:
    id: str
    type: str
    model_params: Dict
    usage: Dict
    prompt: Prompt
    result: Result
    input_context: List[InputContext]

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "modelParams": self.model_params,
            "usage": self.usage,
            "prompt": self.prompt.to_dict(),
            "result": self.result.to_dict(),
            "inputContext": [context.to_dict() for context in self.input_context],
        }


@dataclass
class Session:
    id: str
    completions: List[Completion]

    def to_dict(self):
        return {
            "id": self.id,
            "completions": [completion.to_dict() for completion in self.completions],
        }
