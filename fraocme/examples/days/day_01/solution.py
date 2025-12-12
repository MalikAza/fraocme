"""
Day 01 Example: Parser Functions

Demonstrates all common parser functions from fraocme.common.parser:
- sections() - Parse blocks separated by blank lines
- lines() - Parse as list of strings
- ints() - Parse as list of integers
- char_lines() - Parse digits per line
- ranges() - Parse integer ranges
- mapped() - Custom line parser
"""

from fraocme import Solver
from fraocme.common.parser import (
    char_lines,
    ints,
    lines,
    mapped,
    ranges,
    sections,
)
from fraocme.common.printer import print_ranges, print_row_stats
from fraocme.ui.colors import c


class Day1(Solver):
    def parse(self, raw: str) -> str:
        """Keep raw input for demonstration purposes."""
        return raw

    def part1(self, raw: str) -> int:
        """
        Demonstrate basic parser functions.
        """
        self.debug(c.bold("\n=== Part 1: Basic Parsers ===\n"))

        # 1. sections() - Parse blocks separated by blank lines
        self.debug(c.cyan("1. sections() - Parse blocks:"))
        blocks = sections(raw)
        self.debug(f"   Found {len(blocks)} blocks")
        for i, block in enumerate(blocks[:2]):
            self.debug(f"   Block {i}: {block[:50]}...")

        # 2. lines() - Parse each line as string
        self.debug(c.cyan("\n2. lines() - Parse lines:"))
        all_lines = lines(blocks[0])
        self.debug(f"   Block 0 has {len(all_lines)} lines")
        self.debug(f"   First line: {all_lines[0]}")

        # 3. ints() - Parse integers (one per line)
        self.debug(c.cyan("\n3. ints() - Parse integers:"))
        numbers_text = blocks[1]
        numbers = ints(numbers_text)
        self.debug(f"   Parsed {len(numbers)} numbers")
        self.debug(lambda: print_row_stats(numbers))

        # 4. char_lines() - Parse digits per line
        self.debug(c.cyan("\n4. char_lines() - Parse digit lines:"))
        digit_text = blocks[2]
        digit_rows = char_lines(digit_text, as_int=True)
        self.debug(f"   Parsed {len(digit_rows)} rows of digits")
        self.debug(f"   Row 0: {digit_rows[0][:10]}...")
        self.debug(f"   Row 1: {digit_rows[1][:10]}...")

        return sum(numbers)

    def part2(self, raw: str) -> int:
        """
        Demonstrate advanced parser functions.
        """
        self.debug(c.bold("\n=== Part 2: Advanced Parsers ===\n"))

        blocks = sections(raw)

        # 6. ranges() - Parse integer ranges
        self.debug(c.cyan("\n6. ranges() - Parse ranges:"))
        range_text = blocks[4].strip()
        parsed_ranges = ranges(range_text, range_delimiter="-", entry_delimiter=",")
        self.debug(f"   Parsed {len(parsed_ranges)} ranges")
        self.debug(lambda: print_ranges(parsed_ranges, head=5, tail=2))

        # 7. mapped() - Custom line parser
        self.debug(c.cyan("\n7. mapped() - Custom parser:"))
        coord_text = blocks[5]

        def parse_coord(line: str) -> tuple[int, int]:
            parts = line.split(",")
            return (int(parts[0]), int(parts[1]))

        coords = mapped(coord_text, parse_coord)
        self.debug(f"   Parsed {len(coords)} coordinates")
        self.debug(f"   First 3: {coords[:3]}")
        self.debug(f"   Last 3: {coords[-3:]}")

        # Calculate result based on equations
        total = 0
        for x, y in coords:
            total += x * y + x - y

        return total
