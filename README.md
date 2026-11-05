
# DocChat

DocChat is a simple chatbot created in Python.

It uses the Groq API to generate responses and remembers
previous messages during a conversation.

## Installation

Install the dependencies and the chatbot:

    python -m pip install .

## Usage

To start the chatbot, type:

    chat

Type messages to have a conversation.

Press Ctrl+C or Ctrl+D to exit on macOS/Linux.

## Testing

To run the offline doctests:

    python -m pytest chat.py --doctest-modules

The tests use fake API replies and do not need a live
model connection.
