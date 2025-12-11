"""
Day 02 Example: Sequence Utility Functions

Demonstrates sequence manipulation functions from fraocme.common.utils:
- frequencies() - Count element occurrences
- all_equal() - Check if all elements are identical
- chunks() - Split into fixed-size groups
- windows() - Sliding window over sequence
- pairwise() - Consecutive pairs
- rotate() - Rotate sequence
- unique() - Remove duplicates preserving order
- flatten() - Flatten nested lists
"""

from fraocme import Solver
from fraocme.common.parser import ints, lines, sections
from fraocme.common.utils import (
    all_equal,
    chunks,
    flatten,
    frequencies,
    pairwise,
    rotate,
    unique,
    windows,
)
from fraocme.ui.colors import c


class Day2(Solver):
    def parse(self, raw: str) -> list[str]:
        """Parse into sections for demonstration."""
        return sections(raw)

    def part1(self, data: list[str]) -> int:
        """
        Demonstrate basic sequence utilities.
        """
        self.debug(c.bold("\n=== Part 1: Basic Sequence Utilities ===\n"))

        # 1. frequencies() - Count occurrences
        self.debug(c.cyan("1. frequencies() - Count elements:"))
        letters = list(data[0].replace("\n", ""))
        freq = frequencies(letters)
        self.debug("   Character frequencies:")
        for char, count in sorted(freq.items(), key=lambda x: -x[1])[:5]:
            if char != " ":
                self.debug(f"   '{char}': {c.green(str(count))} times")

        # 2. all_equal() - Check if all same
        self.debug(c.cyan("\n2. all_equal() - Check equality:"))
        test_data = [5, 5, 5, 5]
        result1 = c.green("True") if all_equal(test_data) else c.red("False")
        self.debug(f"   {test_data} → {result1}")
        test_data2 = [5, 5, 3, 5]
        result2 = c.green("True") if all_equal(test_data2) else c.red("False")
        self.debug(f"   {test_data2} → {result2}")

        # 3. chunks() - Split into groups
        self.debug(c.cyan("\n3. chunks() - Fixed-size groups:"))
        numbers = ints(data[1])
        grouped = chunks(numbers, 3)
        self.debug(f"   Split {len(numbers)} numbers into {len(grouped)} groups of 3:")
        for i, group in enumerate(grouped[:3]):
            self.debug(f"   Group {i}: {group}")

        # 4. windows() - Sliding window
        self.debug(c.cyan("\n4. windows() - Sliding window:"))
        sequence = ints(data[2])
        win = windows(sequence, 3)
        self.debug(f"   Windows of size 3 from {len(sequence)} numbers:")
        for i, window in enumerate(win[:4]):
            self.debug(f"   Window {i}: {window} → sum = {c.green(str(sum(window)))}")

        # Count increases using windows
        increases = sum(1 for w in windows(sequence, 2) if w[1] > w[0])
        return increases

    def part2(self, data: list[str]) -> int:
        """
        Demonstrate advanced sequence utilities.
        """
        self.debug(c.bold("\n=== Part 2: Advanced Sequence Utilities ===\n"))

        # 5. pairwise() - Consecutive pairs
        self.debug(c.cyan("5. pairwise() - Consecutive pairs:"))
        values = ints(data[2])
        pairs = pairwise(values)
        self.debug(f"   Analyzing {len(pairs)} consecutive pairs:")
        increases = sum(1 for a, b in pairs if b > a)
        decreases = sum(1 for a, b in pairs if b < a)
        same = sum(1 for a, b in pairs if b == a)
        self.debug(f"   Increases: {c.green(str(increases))}")
        self.debug(f"   Decreases: {c.red(str(decreases))}")
        self.debug(f"   Same: {c.yellow(str(same))}")

        # 6. rotate() - Rotate sequence
        self.debug(c.cyan("\n6. rotate() - Rotate sequence:"))
        original = [1, 2, 3, 4, 5]
        rotated_right = rotate(original, 2)
        rotated_left = rotate(original, -2)
        self.debug(f"   Original: {original}")
        self.debug(f"   Rotate right 2: {rotated_right}")
        self.debug(f"   Rotate left 2: {rotated_left}")

        # 7. unique() - Remove duplicates
        self.debug(c.cyan("\n7. unique() - Remove duplicates:"))
        duplicates_text = data[3]
        numbers_with_dups = [int(x) for x in duplicates_text.split()]
        unique_nums = unique(numbers_with_dups)
        orig_preview = numbers_with_dups[:10]
        self.debug(f"   Original ({len(numbers_with_dups)} items): {orig_preview}...")
        self.debug(f"   Unique ({len(unique_nums)} items): {unique_nums[:10]}...")

        # 8. flatten() - Flatten nested lists
        self.debug(c.cyan("\n8. flatten() - Flatten nested lists:"))
        nested_data = lines(data[4])
        nested = [list(map(int, line.split())) for line in nested_data]
        flat = flatten(nested)
        self.debug(f"   Nested structure: {nested}")
        self.debug(f"   Flattened: {flat}")
        self.debug(f"   Total elements: {c.green(str(len(flat)))}")

        return sum(flat)
