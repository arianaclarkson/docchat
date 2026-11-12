
"""Load local PNG files into a chatbot conversation."""

import base64
from pathlib import Path

from tools.path_utils import is_path_safe


def load_image(chat, path):
    """Append a safe PNG image as an OpenAI-compatible content block."""
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
