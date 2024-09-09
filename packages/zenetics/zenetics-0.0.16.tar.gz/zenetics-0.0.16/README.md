# Zenetics SDK

Zenetics SDK is a Python library that provides a simple interface to interact with Zenetics API.

### Installation

```commandline
pip install zenetics
```

### Usage

Define the following environment variables: `OPENAI_API_KEY`, `ZENETICS_API_KEY`, `ZENETICS_APP_ID`.

```python
from zenetics import openai

openai.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    model="gpt-3.5-turbo",
)
```
