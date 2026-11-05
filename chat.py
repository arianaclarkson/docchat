
import os
from unittest.mock import MagicMock, patch
from contextlib import redirect_stdout
from io import StringIO

from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def llm(messages, temperature=1):
    """Send messages to the model and return its response."""
    completion = client.chat.completions.create(
        messages=messages,
        model='openai/gpt-oss-20b',
        temperature=temperature,
    )
    return completion.choices[0].message.content


class Chat:
    def __init__(self, system='You are a helpful assistant.'):
        self.messages = [{'role': 'system', 'content': system}]
    
    def send_message(self, message, temperature=0.8):
        """Send a message while remembering the conversation.

        >>> requests = []
        >>> def fake_create(**kwargs):
        ...     requests.append([m.copy() for m in kwargs['messages']])
        ...     response = MagicMock()
        ...     response.choices[0].message.content = (
        ...         'Ahoy!' if len(requests) == 1 else 'Welcome back!'
        ...     )
        ...     return response
        >>> with patch.object(client.chat.completions, 'create', side_effect=fake_create):
        ...     bot = Chat(system='Be brief.')
        ...     print(bot.send_message('Hello', temperature=0))
        ...     print(bot.send_message('Remember me?', temperature=0))
        Ahoy!
        Welcome back!
        >>> requests[1]
        [{'role': 'system', 'content': 'Be brief.'}, {'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Ahoy!'}, {'role': 'user', 'content': 'Remember me?'}]
        >>> [m['role'] for m in bot.messages]
        ['system', 'user', 'assistant', 'user', 'assistant']
        >>> bot.messages[-1]['content']
        'Welcome back!'
        """
        self.messages.append({'role': 'user', 'content': message})
        reply = llm(self.messages, temperature=temperature)
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply


def repl(temperature=0.8):
    """Run the chatbot until the user exits.

    Test two inputs, two replies, and EOFError.

    >>> requests = []
    >>> def fake_create(**kwargs):
    ...     requests.append({
    ...         'messages': [m.copy() for m in kwargs['messages']],
    ...         'temperature': kwargs['temperature'],
    ...     })
    ...     response = MagicMock()
    ...     response.choices[0].message.content = (
    ...         'Hello!' if len(requests) == 1 else 'I remember!'
    ...     )
    ...     return response
    >>> output = StringIO()
    >>> with patch('builtins.input', side_effect=['Hi', 'Remember?', EOFError]), patch.object(client.chat.completions, 'create', side_effect=fake_create), redirect_stdout(output):
    ...     repl(temperature=0)
    >>> output.getvalue().strip().splitlines()
    ['Hello!', 'I remember!']
    >>> len(requests)
    2
    >>> [m['content'] for m in requests[1]['messages'][1:]]
    ['Hi', 'Hello!', 'Remember?']
    >>> [request['temperature'] for request in requests]
    [0, 0]

    Test KeyboardInterrupt separately.

    >>> output = StringIO()
    >>> with patch('builtins.input', side_effect=KeyboardInterrupt), redirect_stdout(output):
    ...     repl(temperature=0)
    >>> output.getvalue()
    '\\n'
    """
    chat = Chat(
        system='You are a helpful assistant. You always speak like a pirate.'
    )
    try:
        while True:
            user_input = input('chat> ')
            print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
