"""
Range-related utilities split from utils.py
"""

from .types import RangeMode


def ranges_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    """
    Check if two ranges overlap.

    Args:
        r1: First range as (start, end)
        r2: Second range as (start, end)

    Example (overlapping):
        ranges_overlap((1, 5), (3, 8))
        Returns: True  # They share 3, 4, 5

    Example (not overlapping):
        ranges_overlap((1, 5), (6, 10))
        Returns: False  # No shared values

    Example (touching):
        ranges_overlap((1, 5), (5, 10))
        Returns: True  # They share 5
    """
    return r1[0] <= r2[1] and r2[0] <= r1[1]


def range_intersection(
    r1: tuple[int, int], r2: tuple[int, int]
) -> tuple[int, int] | None:
    """
    Get the overlapping part of two ranges.

    Args:
        r1: First range as (start, end)
        r2: Second range as (start, end)

    Returns:
        Overlapping range or None if no overlap

    Example (overlapping):
        range_intersection((1, 10), (5, 15))
        Returns: (5, 10)

    Example (no overlap):
        range_intersection((1, 5), (7, 10))
        Returns: None

    Example (one contains other):
        range_intersection((1, 20), (5, 10))
        Returns: (5, 10)
    """
    start = max(r1[0], r2[0])
    end = min(r1[1], r2[1])
    if start <= end:
        return (start, end)
    return None


def merge_ranges(
    ranges: list[tuple[int, int]], inclusive: bool = True
) -> list[tuple[int, int]]:
    """
    Merge overlapping/adjacent ranges into non-overlapping ones.

    Example:
        ranges = [(1, 5), (3, 8), (10, 15)]
        merge_ranges(ranges)
        Returns: [(1, 8), (10, 15)]  # First two merged

    Example (adjacent ranges):
        ranges = [(1, 5), (6, 10), (20, 25)]
        merge_ranges(ranges)
        Returns: [(1, 10), (20, 25)]  # Adjacent 5-6 merged when inclusive=True

    Example (exclusive):
        ranges = [(1, 5), (6, 10), (20, 25)]
        merge_ranges(ranges, inclusive=False)
        Returns: [(1, 5), (6, 10), (20, 25)]  # No merge since exclusive
    Example (unsorted input):
        ranges = [(10, 15), (1, 5), (3, 8)]
        merge_ranges(ranges)
        Returns: [(1, 8), (10, 15)]  # Sorted and merged
    """
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        if start <= merged[-1][1] + (1 if inclusive else 0):
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def within_range(
    value: int, ranges: list[tuple[int, int]], inclusive: bool = True
) -> bool:
    """
    Check if one int is in any of the given ranges.

    Args:
        ranges: List of ranges as (start, end)

    Returns:
        Boolean indicating if the int is in any range

    Example:
        within_range (1, [(1, 5), (3, 7), (10, 15), (14, 20)])
        Returns: True

    Example (exclusive):
        within_range (5, [(1, 5), (6, 10)], inclusive=False)
        Returns: False

    Example (contiguous):
        within_range (7, [(1, 3), (4, 6), (8, 10)])
        Returns: False
    """
    for start, end in ranges:
        if inclusive:
            if start <= value <= end:
                return True
        else:
            if start < value < end:
                return True
    return False


def subtract_interval(
    base: tuple[int, int], remove: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Subtract one interval from another, returning remaining pieces.

    Args:
        base: The base interval as (start, end)
        remove: The interval to remove from base as (start, end)

    Returns:
        List of remaining intervals (0, 1 or 2 tuples). Endpoints are inclusive.

    Examples:
        subtract_interval((1, 10), (3, 5)) -> [(1, 2), (6, 10)]
        subtract_interval((1, 5), (5, 10)) -> [(1, 4)]
        subtract_interval((1, 5), (6, 10)) -> [(1, 5)]  # no overlap
    """
    a, b = base
    c, d = remove

    # No overlap
    if d < a or c > b:
        return [base]

    # Remove covers base entirely
    if c <= a and d >= b:
        return []

    remaining: list[tuple[int, int]] = []

    # Left piece
    if c > a:
        left_end = min(b, c - 1)
        if a <= left_end:
            remaining.append((a, left_end))

    # Right piece
    if d < b:
        right_start = max(a, d + 1)
        if right_start <= b:
            remaining.append((right_start, b))

    return remaining


def range_coverage(
    ranges: list[tuple[int, int]], mode: RangeMode = RangeMode.HALF_OPEN
) -> int:
    """
    Calculate total coverage of ranges.

    Args:
        ranges: List of ranges as (start, end)
        mode: Counting mode (default: RangeMode.HALF_OPEN)
            - RangeMode.INCLUSIVE: Both endpoints [start, end]
            - RangeMode.HALF_OPEN: Exclude end [start, end)
            - RangeMode.EXCLUSIVE: Exclude both (start, end)

    Returns:
        Total coverage as int

    Examples:
        For range (10, 15):
        - INCLUSIVE: 6 values (10,11,12,13,14,15)
        - HALF_OPEN: 5 values (10,11,12,13,14)
        - EXCLUSIVE: 4 values (11,12,13,14)

        from fraocme.common import RangeMode
        range_coverage([(3, 5), (10, 14), (16, 20), (12, 18)], mode=RangeMode.INCLUSIVE)
        Returns: 17

        range_coverage([(3, 5), (10, 14), (16, 20), (12, 18)], mode=RangeMode.HALF_OPEN)
        Returns: 14

        range_coverage([(3, 5), (10, 14), (16, 20), (12, 18)], mode=RangeMode.EXCLUSIVE)
        Returns: 11
    """
    # Convert mode to inclusive boolean for merge_ranges
    merge_inclusive = mode != RangeMode.EXCLUSIVE
    merged = merge_ranges(ranges, inclusive=merge_inclusive)
    total = 0
    for start, end in merged:
        if mode == RangeMode.INCLUSIVE:
            total += end - start + 1  # [start, end]
        elif mode == RangeMode.EXCLUSIVE:
            total += end - start - 1  # (start, end)
        else:  # HALF_OPEN
            total += end - start  # [start, end)
    return total
