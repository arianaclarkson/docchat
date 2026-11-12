
"""List files and folders in a selected directory."""

import glob

from tools.path_utils import is_path_safe


def ls(path="."):

    """List directory entries in sorted order.

    >>> import tempfile, os
    >>> with tempfile.TemporaryDirectory(dir=".") as folder:
    ...     open(os.path.join(os.path.relpath(folder), "z.txt"), "w").close()
    ...     open(os.path.join(os.path.relpath(folder), "a.txt"), "w").close()
    ...     ls(os.path.relpath(folder)) == "a.txt  z.txt"
    True
    >>> ls("../")
    'Invalid path'
    >>> ls("nonexistent_directory_12345")
    'Directory not found'
    >>> from unittest.mock import patch
    >>> with patch('tools.ls.glob.glob', side_effect=OSError):
    ...     ls('.')
    'Directory not found'
    """

    if not is_path_safe(path):
        return "Invalid path"

    try:
        import os
        if not os.path.isdir(path):
            return "Directory not found"

        entries = glob.glob(os.path.join(path, "*"))
        entries = sorted(os.path.basename(p) for p in entries)
        return "  ".join(entries)
    except OSError:
        return "Directory not found"
