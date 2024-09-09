from zenetics import openai

## Define the environment variables
#
#   OPENAI_API_KEY: Your OpenAI API key.
#   ZENETICS_API_KEY: Your Zenetics API key.
#   ZENETICS_APP_ID: Your Zenetics app ID.
#

openai.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    model="gpt-3.5-turbo",
)
