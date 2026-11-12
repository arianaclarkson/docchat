
"""Read the contents of a local text file."""

from tools.path_utils import is_path_safe


def cat(path):

    """Return file contents or a readable error.

    >>> import tempfile, os
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     filename = os.path.join(os.path.relpath(folder), "note.txt")
    ...     _ = open(filename, "w").write("hello world")
    ...     cat(filename)
    'hello world'
    >>> cat("../secret.txt")
    'Invalid path'
    >>> cat("nonexistent_file_12345.txt")
    'File not found'
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     filename = os.path.join(os.path.relpath(folder), "binary.dat")
    ...     _ = open(filename, "wb").write(b'\\xff')
    ...     cat(filename)
    'Cannot read file'
    """

    if not is_path_safe(path):
        return "Invalid path"

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found"
    except (UnicodeError, OSError):
        return "Cannot read file"
