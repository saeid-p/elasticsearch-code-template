import os
from typing import Optional


def read(key: str) -> Optional[str]:
    """Reads an environment variable."""
    return os.environ.get(key)


def readOrDefault(key: str, default: str) -> Optional[str]:
    """Reads an environment variable or use the default value when it's none."""
    return os.environ.get(key, default)
