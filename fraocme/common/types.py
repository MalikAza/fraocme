from enum import Enum


class RangeMode(Enum):
    """Counting mode for range operations."""

    INCLUSIVE = "inclusive"  # Both endpoints: [start, end]
    HALF_OPEN = "half-open"  # Exclude end: [start, end)
    EXCLUSIVE = "exclusive"  # Exclude both: (start, end)
