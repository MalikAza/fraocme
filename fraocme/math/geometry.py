import math
from typing import Sequence


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
