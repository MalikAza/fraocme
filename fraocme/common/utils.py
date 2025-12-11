import math
from typing import Sequence


# Numeric utilities
def sign(n: int) -> int:
    """
    Return -1, 0, or 1 based on sign of n.

    Example:
        sign(5)   Returns: 1
        sign(-3)  Returns: -1
        sign(0)   Returns: 0

    Example (moving toward target):
        current = 10
        target = 3
        step = sign(target - current)
        Returns: -1 (need to decrease)
    """
    return (n > 0) - (n < 0)


def digits(n: int) -> list[int]:
    """
    Extract digits from an integer.

    Example:
        digits(1234)
        Returns: [1, 2, 3, 4]

    Example (single digit):
        digits(7)
        Returns: [7]
    Example (use with from_digits for round-trip):
        digits(987)        Returns: [9, 8, 7]
        from_digits([9, 8, 7])  Returns: 987
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
        Returns: 5

    Example (negative wrap):
        wrap(-10, 100)
        Returns: 90
    Example (circular position):
        position = 50
        position = wrap(position + 60, 100)
        Returns: 10  # Wrapped around
    """
    return value % size


def divisors(n: int) -> list[int]:
    """
    Get all divisors of n (including 1 and n).

    Example:
        divisors(12)
        Returns: [1, 2, 3, 4, 6, 12]

    Example:
        divisors(28)
        Returns: [1, 2, 4, 7, 14, 28]
    Example (prime number):
        divisors(17)
        Returns: [1, 17]
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
        Returns: 4

    Example with multiple numbers:
        gcd(24, 36, 48)
        Returns: 12

    Common use case (simplifying fractions):
        numerator, denominator = 15, 25
        divisor = gcd(numerator, denominator)
        Returns: 5 → simplified: 3/5
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
        Returns: 12

    Example with multiple numbers:
        lcm(3, 4, 5)
        Returns: 60

    Common use case (cycle detection):
        cycles = [5, 7, 11]  # Different periods
        lcm(*cycles)
        Returns: 385  # When all cycles align
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
        Returns: 1234

    Example (reverse operation of splitting):
        digits = [9, 8, 7]
        from_digits(digits)
        Returns: 987
    """
    return int("".join(map(str, digits)))


def euclidean_distance(p1: Sequence[int | float], p2: Sequence[int | float]) -> float:
    """
    Calculate Euclidean distance between two points in n-dimensional space.

    Args:
        p1: First point as sequence of coordinates
        p2: Second point as sequence of coordinates

    Returns:
        Euclidean distance as float

    Raises:
        ValueError: If points have different dimensions

    Example (2D):
        euclidean_distance((0, 0), (3, 4))
        Returns: 5.0

    Example (3D junction boxes):
        euclidean_distance((162, 817, 812), (57, 618, 57))
        Returns: 760.8...

    Example (with floats):
        euclidean_distance((1.5, 2.5), (4.5, 6.5))
        Returns: 5.0

    Example (finding distance between two positions):
        box1 = (162, 817, 812)
        box2 = (57, 618, 57)
        dist = euclidean_distance(box1, box2)
        Returns: 760.8222985692171
    """
    if len(p1) != len(p2):
        raise ValueError(
            f"Points must have same dimensions: got {len(p1)} and {len(p2)}"
        )
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def squared_euclidean_distance(
    p1: Sequence[int | float], p2: Sequence[int | float]
) -> float:
    """
    Calculate squared Euclidean distance between two points.

    This is faster than euclidean_distance() as it avoids the sqrt operation.
    Useful when only comparing distances (since a < b ⟺ a² < b² for positive numbers).

    Args:
        p1: First point as sequence of coordinates
        p2: Second point as sequence of coordinates

    Returns:
        Squared Euclidean distance as float

    Raises:
        ValueError: If points have different dimensions

    Example (2D):
        squared_euclidean_distance((0, 0), (3, 4))
        Returns: 25.0

    Example (comparing distances without sqrt):
        box1 = (162, 817, 812)
        box2 = (57, 618, 57)
        box3 = (906, 360, 560)

        # Find closer box without expensive sqrt
        dist1 = squared_euclidean_distance(box1, box2)
        dist2 = squared_euclidean_distance(box1, box3)
        closer = box2 if dist1 < dist2 else box3

    Example (nearest neighbor search):
        target = (100, 100, 100)
        boxes = [(162, 817, 812), (57, 618, 57), (906, 360, 560)]

        # Find nearest box efficiently
        nearest = min(boxes, key=lambda b: squared_euclidean_distance(target, b))
    """
    if len(p1) != len(p2):
        raise ValueError(
            f"Points must have same dimensions: got {len(p1)} and {len(p2)}"
        )
    return sum((a - b) ** 2 for a, b in zip(p1, p2))
