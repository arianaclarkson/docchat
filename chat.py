
"""Run a command-line chatbot that can inspect local files.

The chatbot supports manual commands and automatic model tool calls.
"""

import argparse
import json
import os
import shlex

from dotenv import load_dotenv
from groq import Groq

from tools.calculate import calculate
from tools.cat import cat
from tools.grep import grep
from tools.ls import ls


FUNCTIONS = {
    "calculate": calculate,
    "ls": ls,
    "cat": cat,
    "grep": grep,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read a local text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search files using a regular expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "regex": {"type": "string"},
                    "path": {"type": "string"},
                },
                "required": ["regex", "path"],
            },
        },
    },
]


def get_client():
    """Create a Groq client only when an API request is needed.

    >>> from unittest.mock import patch
    >>> with patch("chat.load_dotenv"), patch("chat.Groq") as fake_groq:
    ...     with patch.dict("os.environ", {"GROQ_API_KEY": "test-key"}):
    ...         _ = get_client()
    ...     fake_groq.assert_called_once_with(api_key="test-key")
    """
    load_dotenv(override=True)
    return Groq(api_key=os.environ.get("GROQ_API_KEY"))


def execute_tool(name, arguments):
    """Call a registered tool using named arguments.

    >>> execute_tool("calculate", {"expression": "2 + 3"})
    '5'
    >>> execute_tool("unknown", {})
    'Unknown tool'
    """
    if name not in FUNCTIONS:
        return "Unknown tool"

    try:
        return str(FUNCTIONS[name](**arguments))
    except (TypeError, ValueError, OSError) as error:
        return f"Tool error: {error}"



def llm(messages, temperature=1):
    """Send messages to Groq and return the model's text reply.

    >>> from unittest.mock import MagicMock, patch
    >>> fake_client = MagicMock()
    >>> fake_client.chat.completions.create.return_value.choices[0].message.content = "Hello!"
    >>> messages = [{"role": "user", "content": "Hi"}]
    >>> with patch("chat.get_client", return_value=fake_client):
    ...     llm(messages, temperature=0)
    'Hello!'
    >>> fake_client.chat.completions.create.call_args.kwargs["temperature"]
    0
    """
    client = get_client()

    completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-20b",
        temperature=temperature,
        timeout=30,
    )

    return completion.choices[0].message.content


class Chat:
    """Store a chatbot's conversation and execute file tools.

    The chatbot supports both direct slash commands and automatic
    tool requests from a language model.

    >>> bot = Chat(system="Be brief.")
    >>> bot.messages[0]["content"]
    'Be brief.'
    >>> bot.run_command("/calculate 2 + 3")
    '5'
    >>> bot.run_command("/unknown")
    'Unknown command'
    """

    def __init__(self, system="You are a helpful assistant."):
        """Initialize the conversation with a system message."""
        self.messages = [
            {"role": "system", "content": system}
        ]
        self.debug = False

    def send_message(self, message, temperature=0.8):
        """Send a message and run tools requested by the model.

        >>> from unittest.mock import MagicMock, patch
        >>> fake_client = MagicMock()
        >>> fake_reply = MagicMock()
        >>> fake_reply.content = "Ahoy!"
        >>> fake_reply.tool_calls = None
        >>> fake_client.chat.completions.create.return_value.choices[0].message = fake_reply
        >>> with patch("chat.get_client", return_value=fake_client):
        ...     bot = Chat()
        ...     bot.send_message("Hello", temperature=0)
        'Ahoy!'
        >>> [m["role"] for m in bot.messages]
        ['system', 'user', 'assistant']
        """
        self.messages.append({
            "role": "user",
            "content": message,
        })

        client = get_client()

        while True:
            completion = client.chat.completions.create(
                messages=self.messages,
                model="openai/gpt-oss-20b",
                temperature=temperature,
                tools=TOOLS,
                tool_choice="auto",
                timeout=30,
            )

            reply = completion.choices[0].message
            tool_calls = reply.tool_calls

            if not isinstance(tool_calls, (list, tuple)):
                tool_calls = []

            if tool_calls:
                self.messages.append(
                    reply.model_dump(exclude_none=True)
                )

                for call in tool_calls:
                    name = call.function.name

                    try:
                        arguments = json.loads(
                            call.function.arguments
                        )

                        if not isinstance(arguments, dict):
                            raise ValueError("Expected an object")

                        result = execute_tool(name, arguments)

                    except (ValueError, TypeError) as error:
                        arguments = {}
                        result = f"Tool error: {error}"

                    if self.debug:
                        print(f"[DEBUG] {name}: {arguments}")

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result),
                    })

                continue

            content = reply.content or ""

            self.messages.append({
                "role": "assistant",
                "content": content,
            })

            return content

    def run_command(self, user_input):
        """Execute a slash command without an API request.

        >>> chat = Chat()
        >>> chat.run_command("/calculate 2 + 3")
        '5'
        >>> chat.run_command("/unknown")
        'Unknown command'
        >>> chat.run_command("/calculate 10 * 2")
        '20'
        """
        try:
            parts = shlex.split(user_input[1:])
        except ValueError:
            return "Invalid command"

        if not parts:
            return "Unknown command"

        command = parts[0]
        args = parts[1:]

        if command not in FUNCTIONS:
            return "Unknown command"

        if command == "calculate":
            arguments = {
                "expression": " ".join(args)
            }

        elif command == "ls":
            if len(args) > 1:
                return "Tool error: too many arguments"

            arguments = {
                "path": args[0] if args else "."
            }

        elif command == "cat":
            if len(args) != 1:
                return "Tool error: cat requires one path"

            arguments = {"path": args[0]}

        elif command == "grep":
            if len(args) != 2:
                return "Tool error: grep requires a regex and path"

            arguments = {
                "regex": args[0],
                "path": args[1],
            }

        result = execute_tool(command, arguments)

        if self.debug:
            print(f"[DEBUG] {command}: {arguments}")

        self.messages.append({
            "role": "user",
            "content": user_input,
        })

        self.messages.append({
            "role": "assistant",
            "content": f"Result of {user_input}:\n{result}",
        })

        return str(result)


def repl(chat=None, temperature=0.8):
    """Run the interactive chatbot until the user exits."""
    if chat is None:
        chat = Chat(
            system=(
                "You are a helpful assistant. "
                "You always speak like a pirate."
            )
        )

    try:
        while True:
            user_input = input("chat> ")

            if user_input.startswith("/"):
                print(chat.run_command(user_input))
            else:
                print(
                    chat.send_message(
                        user_input,
                        temperature=temperature,
                    )
                )

    except (KeyboardInterrupt, EOFError):
        print()


def main():
    """Run the chatbot with command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="?")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    chat = Chat()
    chat.debug = args.debug

    if args.message is not None:
        print(chat.send_message(args.message))
    else:
        repl(chat)


if __name__ == "__main__":
    main()
