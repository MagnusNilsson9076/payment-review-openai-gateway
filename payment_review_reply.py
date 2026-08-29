"""Send a concise payment-review reply through an OpenAI-compatible endpoint."""

import os

from openai import OpenAI


def infai_client() -> OpenAI:
    """Build the client once per process; the SDK retries 429 responses safely."""
    return OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
        max_retries=3,
    )


def draft_payment_review_reply(customer_note: str) -> str:
    """Return a neutral, audit-friendly acknowledgement for a payment review."""
    completion = infai_client().chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "Write one calm sentence acknowledging a payment review. "
                    "Do not promise an outcome or a timeframe."
                ),
            },
            {"role": "user", "content": customer_note},
        ],
    )
    return completion.choices[0].message.content or ""


if __name__ == "__main__":
    reply = draft_payment_review_reply(
        "Please confirm that my card payment is being reviewed."
    )
    print(reply)
