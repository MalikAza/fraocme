"""
Day 04 Example: Range Utility Functions

Demonstrates range manipulation functions from fraocme.common.utils:
- ranges_overlap() - Check if two ranges overlap
- range_intersection() - Get overlapping part
- merge_ranges() - Merge overlapping ranges
- within_range() - Check if value in any range
- range_coverage() - Calculate total coverage
"""

from fraocme import Solver
from fraocme.common import RangeMode
from fraocme.common.parser import ranges, sections
from fraocme.common.printer import print_ranges
from fraocme.common.range_utils import (
    merge_ranges,
    range_coverage,
    range_intersection,
    ranges_overlap,
    within_range,
)
from fraocme.ui.colors import c


class Day4(Solver):
    def parse(self, raw: str) -> list[str]:
        """Parse into sections for demonstration."""
        return sections(raw)

    def part1(self, data: list[str]) -> int:
        """
        Demonstrate basic range utilities.
        """
        self.debug(c.bold("\n=== Part 1: Basic Range Utilities ===\n"))

        # Parse ranges from input
        range_data = ranges(data[0].strip(), range_delimiter="-", entry_delimiter=",")
        self.debug(c.cyan("Input ranges:"))
        self.debug(lambda: print_ranges(range_data, head=5))

        # 1. ranges_overlap() - Check if ranges overlap
        self.debug(c.cyan("\n1. ranges_overlap() - Check overlaps:"))
        test_pairs = [
            ((1, 5), (3, 8)),
            ((1, 5), (6, 10)),
            ((1, 5), (5, 10)),
            ((10, 20), (15, 25)),
        ]
        for r1, r2 in test_pairs:
            overlap = ranges_overlap(r1, r2)
            result = c.green("Yes") if overlap else c.red("No")
            self.debug(f"   {r1} & {r2} → {result}")

        # 2. range_intersection() - Get overlapping part
        self.debug(c.cyan("\n2. range_intersection() - Get overlap:"))
        for r1, r2 in test_pairs:
            intersection = range_intersection(r1, r2)
            if intersection:
                self.debug(f"   {r1} ∩ {r2} = {c.green(str(intersection))}")
            else:
                self.debug(f"   {r1} ∩ {r2} = {c.red('None')}")

        # Count overlapping pairs from input
        overlap_count = 0
        for i, r1 in enumerate(range_data):
            for r2 in range_data[i + 1 :]:
                if ranges_overlap(r1, r2):
                    overlap_count += 1

        self.debug(c.cyan(f"\nTotal overlapping pairs: {c.green(str(overlap_count))}"))

        return overlap_count

    def part2(self, data: list[str]) -> int:
        """
        Demonstrate advanced range utilities.
        """
        self.debug(c.bold("\n=== Part 2: Advanced Range Utilities ===\n"))

        range_data = ranges(data[0].strip(), range_delimiter="-", entry_delimiter=",")

        # 3. merge_ranges() - Merge overlapping ranges
        self.debug(c.cyan("3. merge_ranges() - Merge overlapping:"))
        self.debug(f"   Original: {len(range_data)} ranges")
        merged = merge_ranges(range_data, inclusive=True)
        self.debug(f"   Merged: {c.green(str(len(merged)))} ranges")
        self.debug(lambda: print_ranges(merged, head=5))

        # Show specific merge example
        self.debug(c.muted("\n   Example merge:"))
        example = [(1, 5), (3, 8), (10, 15), (14, 20)]
        merged_example = merge_ranges(example)
        self.debug(f"   {example}")
        self.debug(f"   → {c.green(str(merged_example))}")

        # 4. within_range() - Check if value in ranges
        self.debug(c.cyan("\n4. within_range() - Check if value in ranges:"))
        test_value = ranges(data[1].strip(), range_delimiter="-", entry_delimiter=",")
        test_ranges = merged[:3]  # Use first 3 merged ranges

        for val_range in test_value[:5]:
            val = val_range[0]  # Just use start of range as test value
            is_within = within_range(val, test_ranges)
            result = c.green("Yes") if is_within else c.red("No")
            self.debug(f"   Is {val} in {test_ranges}? {result}")

        # 5. range_coverage() - Calculate total coverage
        self.debug(c.cyan("\n5. range_coverage() - Total coverage:"))

        # Before merge
        coverage_before = range_coverage(range_data)
        self.debug(f"   Original ranges coverage: {c.yellow(str(coverage_before))}")

        # After merge (no overlap)
        coverage_after = range_coverage(merged)
        self.debug(f"   Merged ranges coverage: {c.green(str(coverage_after))}")

        # Difference shows overlap
        overlap_total = coverage_before - coverage_after
        self.debug(f"   Overlap removed: {c.red(str(overlap_total))}")

        # Compare inclusive vs exclusive
        self.debug(c.muted("\n   Inclusive vs Exclusive vs Half-open:"))
        example_ranges = [(1, 5), (10, 15)]
        inclusive = range_coverage(example_ranges, mode=RangeMode.INCLUSIVE)
        half_open = range_coverage(example_ranges, mode=RangeMode.HALF_OPEN)
        exclusive = range_coverage(example_ranges, mode=RangeMode.EXCLUSIVE)
        self.debug(f"   {example_ranges}")
        self.debug(f"   Inclusive (endpoints counted): {c.green(str(inclusive))}")
        half_str = c.yellow(str(half_open))
        self.debug(f"   Half-open (endpoints partially counted): {half_str}")
        self.debug(f"   Exclusive (endpoints not counted): {c.red(str(exclusive))}")

        return coverage_after
