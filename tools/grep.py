
"""Search local text files using regular expressions."""

import glob
import re

from tools.path_utils import is_path_safe


def grep(regex, path):

    r"""Find lines matching a regular expression.

    >>> import tempfile, os
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     filename = os.path.join(os.path.relpath(folder), "example.txt")
    ...     _ = open(filename, "w").write("TODO fix\nall done\n")
    ...     grep("TODO", filename)
    'TODO fix'
    >>> grep("TODO", "nonexistent_12345.txt")
    ''
    >>> grep("hello", "../*.txt")
    'Invalid path'
    >>> grep("[", "*.txt")
    'Invalid regex'
    >>> from unittest.mock import patch
    >>> with patch('tools.grep.glob.glob', return_value=['../secret.txt']):
    ...     grep('secret', '*.txt')
    ''
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     filename = os.path.join(os.path.relpath(folder), "binary.dat")
    ...     _ = open(filename, "wb").write(b'\xff')
    ...     grep("anything", filename)
    ''
    """

    if not is_path_safe(path):
        return "Invalid path"

    try:
        pattern = re.compile(regex)
    except re.error:
        return "Invalid regex"

    matches = []
    for filename in sorted(glob.glob(path, recursive=True)):
        if not is_path_safe(filename):
            continue

        try:
            with open(filename, encoding="utf-8") as file:
                for line in file:
                    if pattern.search(line):
                        matches.append(line.rstrip("\n"))
        except (OSError, UnicodeError):
            continue

    return "\n".join(matches)
