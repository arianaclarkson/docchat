
"""Summarize and compact a chatbot's conversation history."""


def compact(chat):
    """Replace conversation history with a summary of five lines or less.

    >>> from unittest.mock import MagicMock, patch
    >>> from chat import Chat
    >>> bot = Chat()
    >>> bot.messages.append({"role": "user", "content": "Hello"})
    >>> fake_client = MagicMock()
    >>> fake_client.chat.completions.create.return_value.choices[0].message.content = "We greeted each other."
    >>> with patch("chat.get_client", return_value=fake_client):
    ...     result = compact(bot)
    >>> result
    'We greeted each other.'
    >>> empty_bot = Chat()
    >>> empty_bot.messages = []
    >>> compact(empty_bot) == ""
    True
    >>> len(bot.messages)
    1
    >>> bot.messages[0]["content"]
    'We greeted each other.'
    """

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
