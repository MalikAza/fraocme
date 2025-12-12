"""
Sequence-related utilities split from utils.py
"""

from collections import Counter
from typing import Sequence, TypeVar

T = TypeVar("T")


def frequencies(data: Sequence[T]) -> dict[T, int]:
    """
    Count occurrences of each element.

    Example:
        data = ["a", "b", "a", "c", "a", "b"]
        frequencies(data)
        Returns: {"a": 3, "b": 2, "c": 1}
    """
    return dict(Counter(data))


def all_equal(data: Sequence[T]) -> bool:
    """
    Check if all elements in the sequence are the same.

    Example:
        all_equal([1, 1, 1, 1])
        Returns: True

    Example (different elements):
        all_equal([1, 2, 1, 1])
        Returns: False

    Example (empty or single):
        all_equal([])      Returns: True
        all_equal([42])    Returns: True
    """
    return len(set(data)) <= 1


def chunks(data: Sequence[T], size: int) -> list[Sequence[T]]:
    """
    Split sequence into fixed-size groups.

    Args:
        data: Sequence to split
        size: Size of each chunk

    Example:
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks(data, 3)
        Returns: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    Example (input grouped by 3 lines):
        lines = ["name: Alice", "age: 30", "city: Paris",
                 "name: Bob", "age: 25", "city: London"]
        chunks(lines, 3)
        Returns: [["name: Alice", "age: 30", "city: Paris"],
                  ["name: Bob", "age: 25", "city: London"]]
    """
    return [data[i : i + size] for i in range(0, len(data), size)]


def windows(data: Sequence[T], size: int) -> list[Sequence[T]]:
    """
    Sliding window over sequence.

    Args:
        data: Sequence to slide over
        size: Window size

    Example:
        data = [1, 2, 3, 4, 5]
        windows(data, 3)
        Returns: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

    Example (sum of 3 consecutive):
        data = [199, 200, 208, 210, 200]
        sums = [sum(w) for w in windows(data, 3)]
        Returns: [607, 618, 618]
    """
    return [data[i : i + size] for i in range(len(data) - size + 1)]


def pairwise(data: Sequence[T]) -> list[tuple[T, T]]:
    """
    Return consecutive pairs.

    Example:
        data = [1, 2, 3, 4]
        pairwise(data)
        Returns: [(1, 2), (2, 3), (3, 4)]

    Example (count increases):
        data = [199, 200, 208, 200, 207]
        increases = sum(1 for a, b in pairwise(data) if b > a)
        Returns: 3
    """
    return list(zip(data, data[1:]))


def rotate(data: Sequence[T], n: int) -> list[T]:
    """
    Rotate sequence by n positions.

    Args:
        data: Sequence to rotate
        n: Positions to rotate (positive = right, negative = left)

    Example (rotate left):
        rotate([1, 2, 3, 4, 5], -2)
        Returns: [3, 4, 5, 1, 2]
    """
    if not data:
        return []
    n = n % len(data)
    return list(data[-n:]) + list(data[:-n])


def unique(data: Sequence[T]) -> list[T]:
    """
    Remove duplicates while preserving order.

    Example:
        unique([1, 2, 2, 3, 1, 4, 2])
        Returns: [1, 2, 3, 4]

    Note: Unlike set(), this preserves the first occurrence order.
    """
    seen = set()
    result = []
    for item in data:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def flatten(nested: Sequence[Sequence[T]]) -> list[T]:
    """
    Flatten one level of nesting.

    Example:
        flatten([[1, 2], [3, 4], [5]])
        Returns: [1, 2, 3, 4, 5]

    Example (flatten parsed sections):
        data = [["a", "b"], ["c"], ["d", "e", "f"]]
        flatten(data)
        Returns: ["a", "b", "c", "d", "e", "f"]

    Note: Only flattens one level. For deeper nesting, apply multiple times.
    """
    return [item for sublist in nested for item in sublist]
