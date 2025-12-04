from typing import Any

from .colors import c


def print_header(text: str, width: int = 40) -> None:
    """Print a formatted header."""
    print(f"\n{'═' * width}")
    print(f"  {text}")
    print(f"{'═' * width}")


def print_section(text: str, width: int = 40) -> None:
    """Print a section divider."""
    print(f"\n{'─' * width}")
    print(f"  {text}")
    print(f"{'─' * width}")

