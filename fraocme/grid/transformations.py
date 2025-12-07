"""Grid transformation operations."""

from typing import TypeVar

from .core import Grid

T = TypeVar("T")


def transpose(grid: Grid[T]) -> Grid[T]:
    """
    Transpose grid (swap rows and columns).

    Args:
        grid: Grid to transpose

    Returns:
        New transposed Grid
    """
    transposed_data = tuple(zip(*grid.data))
    return Grid(transposed_data)


def rotate_90(grid: Grid[T]) -> Grid[T]:
    """
    Rotate grid 90 degrees clockwise.

    Args:
        grid: Grid to rotate

    Returns:
        New rotated Grid
    """
    # Transpose then flip horizontally
    transposed = transpose(grid)
    return flip_horizontal(transposed)


def rotate_180(grid: Grid[T]) -> Grid[T]:
    """
    Rotate grid 180 degrees.

    Args:
        grid: Grid to rotate

    Returns:
        New rotated Grid
    """
    # Flip both axes
    flipped_v = flip_vertical(grid)
    return flip_horizontal(flipped_v)


def rotate_270(grid: Grid[T]) -> Grid[T]:
    """
    Rotate grid 270 degrees clockwise (or 90 counter-clockwise).

    Args:
        grid: Grid to rotate

    Returns:
        New rotated Grid
    """
    # Transpose then flip vertically
    transposed = transpose(grid)
    return flip_vertical(transposed)


def flip_horizontal(grid: Grid[T]) -> Grid[T]:
    """
    Flip grid horizontally (mirror left-right).

    Args:
        grid: Grid to flip

    Returns:
        New flipped Grid
    """
    flipped_data = tuple(row[::-1] for row in grid.data)
    return Grid(flipped_data)


def flip_vertical(grid: Grid[T]) -> Grid[T]:
    """
    Flip grid vertically (mirror top-bottom).

    Args:
        grid: Grid to flip

    Returns:
        New flipped Grid
    """
    flipped_data = grid.data[::-1]
    return Grid(flipped_data)


Grid.transpose = lambda self: transpose(self)
Grid.rotate_90 = lambda self: rotate_90(self)
Grid.rotate_180 = lambda self: rotate_180(self)
Grid.rotate_270 = lambda self: rotate_270(self)
Grid.flip_horizontal = lambda self: flip_horizontal(self)
Grid.flip_vertical = lambda self: flip_vertical(self)
