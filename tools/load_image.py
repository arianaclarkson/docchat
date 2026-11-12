
"""Load local PNG files into a chatbot conversation."""

import base64
from pathlib import Path

from tools.path_utils import is_path_safe


def load_image(chat, path):
    """Append a safe PNG image as an OpenAI-compatible content block.

    >>> import tempfile
    >>> import os
    >>> from chat import Chat
    >>> bot = Chat()
    >>> load_image(bot, "../secret.png")
    'Invalid path'
    >>> len(bot.messages)
    1
    >>> load_image(bot, "notes.txt")
    'Only PNG files are supported'
    >>> load_image(bot, "missing_image_12345.png")
    'Cannot read image'
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     path = os.path.join(os.path.relpath(folder), "test.png")
    ...     _ = open(path, "wb").write(b"test image bytes")
    ...     load_image(bot, path)
    'Image loaded'
    >>> bot.messages[-1]["content"][0]["type"]
    'image_url'
    >>> bot.messages[-1]["content"][0]["image_url"]["url"].startswith("data:image/png;base64,")
    True
    """

    if not is_path_safe(path):
        return "Invalid path"

    if Path(path).suffix.lower() != ".png":
        return "Only PNG files are supported"

    try:
        with open(path, "rb") as file:
            contents = file.read()
    except OSError:
        return "Cannot read image"

    encoded = base64.b64encode(contents).decode("ascii")

    chat.messages.append({
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encoded}"
                },
            }
        ],
    })

    return "Image loaded"
