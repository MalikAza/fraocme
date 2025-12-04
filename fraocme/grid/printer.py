from typing import Any, Callable

from ..ui.colors import c
from .types import Grid, Position


def print_grid(grid: Grid | list[list[Any]], separator: str = '', highlight: set[Position] | None = None) -> None:
    """
    Print a 2D grid with optional position highlighting.
    
    Args:
        grid: 2D grid to print
        separator: String to place between cells (default: no separator)
        highlight: Optional set of positions to highlight
    
    Example:
        grid = [['a', 'b'], ['c', 'd']]
        print_grid(grid, separator=' ', highlight={(0, 0)})
    """
    for y, row in enumerate(grid):
        line_parts = []
        for x, cell in enumerate(row):
            cell_str = str(cell)
            if highlight and (x, y) in highlight:
                cell_str = c.cyan(cell_str)
            line_parts.append(cell_str)
        print(separator.join(line_parts))
