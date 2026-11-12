
"""Summarize and compact a chatbot's conversation history."""


def compact(chat):
    """Replace a conversation with a summary of five lines or less."""
    if not chat.messages:
        return ""

    from chat import get_client

    client = get_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=chat.messages,
        temperature=0,
        timeout=30,
    )

    summary = response.choices[0].message.content or ""
    summary = "\n".join(summary.splitlines()[:5])

    chat.messages = [
        {"role": "system", "content": summary}
    ]

    return summary
