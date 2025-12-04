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


    
def print_grid(grid: list[list[Any]], sep: str = '') -> None:
    """Print a 2D grid."""
    for row in grid:
        print(sep.join(str(cell) for cell in row))


# TODO: example function, need to make better later
def print_max_in_rows(grid: list[list[int]]) -> None:
    """Print the highest number in each row of a 2D grid."""
    for row in grid:
        if row:
            print(max(row))
        else:
            print("Empty row")