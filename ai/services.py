from openai import OpenAI

from django.conf import settings

from .prompts import (
    SYSTEM_PROMPT,
    ANALYZE_USER_PROMPT,
)


client = OpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url="https://api.mistral.ai/v1"
)


def analyze_expenses(expense_data):

    response = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ANALYZE_USER_PROMPT.format(
                    expense_data=expense_data
                ),
            },
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    return response.choices[0].message.content


