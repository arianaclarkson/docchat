
"""Provide utilities for checking whether file paths are safe to access."""

from pathlib import Path


def is_path_safe(path):
    """Reject absolute paths and parent-directory traversal.

    >>> is_path_safe("notes.txt")
    True
    >>> is_path_safe("../secret.txt")
    False
    >>> is_path_safe("/etc/passwd")
    False
    >>> from unittest.mock import patch
    >>> with patch("tools.path_utils.Path.resolve", side_effect=ValueError):
    ...     is_path_safe("notes.txt")
    False
    """

    path = Path(path)
    if path.is_absolute() or ".." in path.parts:
        return False

    try:
        path.resolve().relative_to(Path.cwd().resolve())
        return True
    except ValueError:
        return False
