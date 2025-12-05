import math
from collections import Counter
from typing import Sequence, TypeVar

T = TypeVar("T")


# ─────────────────────────────────────────────────────────
# Transpose
# ─────────────────────────────────────────────────────────
def transpose(data: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """
    Transpose rows into columns.

    Args:
        data: List of rows (e.g., from ints_per_line)

    Example:
        data = [[63721, 98916], [83871, 23584], [55026, 62690]]
        transpose(data)
        # Returns: ((63721, 83871, 55026), (98916, 23584, 62690))

    Usage with parser:
        pairs = ints_per_line(raw)
        left, right = transpose(pairs)
    """
    return tuple(zip(*data))


# ─────────────────────────────────────────────────────────
# Frequency/Counting utilities
# ─────────────────────────────────────────────────────────
def frequencies(data: Sequence[T]) -> dict[T, int]:
    """
    Count occurrences of each element.

    Example:
        data = ["a", "b", "a", "c", "a", "b"]
        frequencies(data)
        # Returns: {"a": 3, "b": 2, "c": 1}
    """
    return dict(Counter(data))


def all_equal(data: Sequence[T]) -> bool:
    """
    Check if all elements in the sequence are the same.

    Example:
        all_equal([1, 1, 1, 1])
        # Returns: True

    Example (different elements):
        all_equal([1, 2, 1, 1])
        # Returns: False

    Example (empty or single):
        all_equal([])      # Returns: True
        all_equal([42])    # Returns: True
    """
    return len(set(data)) <= 1


# ─────────────────────────────────────────────────────────
# Sequence utilities
# ─────────────────────────────────────────────────────────
def chunks(data: Sequence[T], size: int) -> list[Sequence[T]]:
    """
    Split sequence into fixed-size groups.

    Args:
        data: Sequence to split
        size: Size of each chunk

    Example:
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks(data, 3)
        # Returns: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    Example (input grouped by 3 lines):
        lines = ["name: Alice", "age: 30", "city: Paris",
                 "name: Bob", "age: 25", "city: London"]
        chunks(lines, 3)
        # Returns: [["name: Alice", "age: 30", "city: Paris"],
        #           ["name: Bob", "age: 25", "city: London"]]
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
        # Returns: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

    Example (sum of 3 consecutive):
        data = [199, 200, 208, 210, 200]
        sums = [sum(w) for w in windows(data, 3)]
        # Returns: [607, 618, 618]
    """
    return [data[i : i + size] for i in range(len(data) - size + 1)]


def pairwise(data: Sequence[T]) -> list[tuple[T, T]]:
    """
    Return consecutive pairs.

    Example:
        data = [1, 2, 3, 4]
        pairwise(data)
        # Returns: [(1, 2), (2, 3), (3, 4)]

    Example (count increases):
        data = [199, 200, 208, 200, 207]
        increases = sum(1 for a, b in pairwise(data) if b > a)
        # Returns: 3
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
        # Returns: [3, 4, 5, 1, 2]
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
        # Returns: [1, 2, 3, 4]

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
        # Returns: [1, 2, 3, 4, 5]

    Example (flatten parsed sections):
        data = [["a", "b"], ["c"], ["d", "e", "f"]]
        flatten(data)
        # Returns: ["a", "b", "c", "d", "e", "f"]

    Note: Only flattens one level. For deeper nesting, apply multiple times.
    """
    return [item for sublist in nested for item in sublist]


# ─────────────────────────────────────────────────────────
# Numeric utilities
# ─────────────────────────────────────────────────────────
def sign(n: int) -> int:
    """
    Return -1, 0, or 1 based on sign of n.

    Example:
        sign(5)   # Returns: 1
        sign(-3)  # Returns: -1
        sign(0)   # Returns: 0

    Example (moving toward target):
        current = 10
        target = 3
        step = sign(target - current)
        # Returns: -1 (need to decrease)
    """
    return (n > 0) - (n < 0)


def digits(n: int) -> list[int]:
    """
    Extract digits from an integer.

    Example:
        digits(1234)
        # Returns: [1, 2, 3, 4]

    Example (single digit):
        digits(7)
        # Returns: [7]

    Example (use with from_digits for round-trip):
        digits(987)        # Returns: [9, 8, 7]
        from_digits([9, 8, 7])  # Returns: 987
    """
    return [int(d) for d in str(abs(n))]


def wrap(value: int, size: int) -> int:
    """
    Wrap value into range [0, size).

    Args:
        value: The value to wrap
        size: The size of the range (exclusive upper bound)

    Example:
        wrap(105, 100)
        # Returns: 5

    Example (negative wrap):
        wrap(-10, 100)
        # Returns: 90

    Example (circular position):
        position = 50
        position = wrap(position + 60, 100)
        # Returns: 10  # Wrapped around
    """
    return value % size


def divisors(n: int) -> list[int]:
    """
    Get all divisors of n (including 1 and n).

    Example:
        divisors(12)
        # Returns: [1, 2, 3, 4, 6, 12]

    Example:
        divisors(28)
        # Returns: [1, 2, 4, 7, 14, 28]

    Example (prime number):
        divisors(17)
        # Returns: [1, 17]
    """
    result = []
    sqrt_n = int(math.sqrt(n))
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
    return sorted(result)


def gcd(*args: int) -> int:
    """
    Greatest common divisor of multiple numbers.

    Example:
        gcd(12, 8)
        # Returns: 4

    Example with multiple numbers:
        gcd(24, 36, 48)
        # Returns: 12

    Common use case (simplifying fractions):
        numerator, denominator = 15, 25
        divisor = gcd(numerator, denominator)
        # Returns: 5 → simplified: 3/5
    """
    result = args[0]
    for n in args[1:]:
        result = math.gcd(result, n)
    return result


def lcm(*args: int) -> int:
    """
    Least common multiple of multiple numbers.

    Example:
        lcm(4, 6)
        # Returns: 12

    Example with multiple numbers:
        lcm(3, 4, 5)
        # Returns: 60

    Common use case (cycle detection):
        cycles = [5, 7, 11]  # Different periods
        lcm(*cycles)
        # Returns: 385  # When all cycles align
    """
    result = args[0]
    for n in args[1:]:
        result = result * n // math.gcd(result, n)
    return result


def from_digits(digits: Sequence[int]) -> int:
    """
    Combine digits back into an integer.

    Example:
        digits = [1, 2, 3, 4]
        from_digits(digits)
        # Returns: 1234

    Example (reverse operation of splitting):
        digits = [9, 8, 7]
        from_digits(digits)
        # Returns: 987
    """
    return int("".join(map(str, digits)))


# ─────────────────────────────────────────────────────────
# Range utilities
# ─────────────────────────────────────────────────────────
def ranges_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    """
    Check if two ranges overlap.

    Args:
        r1: First range as (start, end)
        r2: Second range as (start, end)

    Example (overlapping):
        ranges_overlap((1, 5), (3, 8))
        # Returns: True  # They share 3, 4, 5

    Example (not overlapping):
        ranges_overlap((1, 5), (6, 10))
        # Returns: False  # No shared values

    Example (touching):
        ranges_overlap((1, 5), (5, 10))
        # Returns: True  # They share 5
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
        # Returns: (5, 10)

    Example (no overlap):
        range_intersection((1, 5), (7, 10))
        # Returns: None

    Example (one contains other):
        range_intersection((1, 20), (5, 10))
        # Returns: (5, 10)
    """
    start = max(r1[0], r2[0])
    end = min(r1[1], r2[1])
    if start <= end:
        return (start, end)
    return None


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping/adjacent ranges into non-overlapping ones.

    Example:
        ranges = [(1, 5), (3, 8), (10, 15)]
        merge_ranges(ranges)
        # Returns: [(1, 8), (10, 15)]  # First two merged

    Example (adjacent ranges):
        ranges = [(1, 5), (6, 10), (20, 25)]
        merge_ranges(ranges)
        # Returns: [(1, 10), (20, 25)]  # Adjacent 5-6 merged

    Example (unsorted input):
        ranges = [(10, 15), (1, 5), (3, 8)]
        merge_ranges(ranges)
        # Returns: [(1, 8), (10, 15)]  # Sorted and merged
    """
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        if start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged
