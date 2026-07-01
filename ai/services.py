import json

from openai import OpenAI
from django.conf import settings

from .prompts import (
    SYSTEM_PROMPT,
    ANALYZE_USER_PROMPT,
    CHAT_USER_PROMPT,
)

client = OpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url="https://api.mistral.ai/v1",
)


def analyze_expenses(expense_data):

    response = client.chat.completions.create(
        model="mistral-small-latest",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ANALYZE_USER_PROMPT.format(
                    expense_data=json.dumps(
                        expense_data,
                        indent=2,
                    )
                ),
            },
        ],
        temperature=0.5,
        max_tokens=1200,
    )

    return json.loads(
        response.choices[0].message.content
    )


def chat_with_ai(expense_data, question):

    response = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": CHAT_USER_PROMPT.format(
                    expense_data=json.dumps(
                        expense_data,
                        indent=2,
                    ),
                    question=question,
                ),
            },
        ],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()