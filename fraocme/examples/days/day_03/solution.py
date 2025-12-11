"""
Day 03 Example: Numeric Utility Functions

Demonstrates numeric functions from fraocme.common.utils:
- sign() - Get sign of number (-1, 0, 1)
- digits() - Extract digits from integer
- from_digits() - Combine digits into integer
- wrap() - Wrap value into range
- divisors() - Get all divisors
- gcd() - Greatest common divisor
- lcm() - Least common multiple
"""

from fraocme import Solver
from fraocme.common.parser import ints, sections
from fraocme.common.utils import (
    digits,
    divisors,
    from_digits,
    gcd,
    lcm,
    sign,
    wrap,
)
from fraocme.ui.colors import c


class Day3(Solver):
    def parse(self, raw: str) -> list[str]:
        """Parse into sections for demonstration."""
        return sections(raw)

    def part1(self, data: list[str]) -> int:
        """
        Demonstrate basic numeric utilities.
        """
        self.debug(c.bold("\n=== Part 1: Basic Numeric Utilities ===\n"))

        # 1. sign() - Get sign of number
        self.debug(c.cyan("1. sign() - Get sign of number:"))
        test_numbers = [42, -17, 0, 100, -5]
        for num in test_numbers:
            s = sign(num)
            color = c.green if s > 0 else (c.red if s < 0 else c.yellow)
            self.debug(f"   sign({num:4d}) = {color(str(s))}")

        self.debug(c.muted("\n   Use case: Moving toward target"))
        current, target = 10, 3
        step = sign(target - current)
        step_str = c.red(str(step))
        self.debug(f"   Current: {current}, Target: {target} → step: {step_str}")

        # 2. digits() - Extract digits
        self.debug(c.cyan("\n2. digits() - Extract digits:"))
        numbers = ints(data[0])
        for num in numbers[:3]:
            d = digits(num)
            self.debug(f"   digits({num}) = {d}")

        # 3. from_digits() - Combine digits
        self.debug(c.cyan("\n3. from_digits() - Combine digits:"))
        digit_list = [9, 8, 7, 6, 5]
        combined = from_digits(digit_list)
        self.debug(f"   from_digits({digit_list}) = {c.green(str(combined))}")

        # Round-trip example
        original = 12345
        d = digits(original)
        back = from_digits(d)
        self.debug(f"   Round-trip: {original} → {d} → {c.green(str(back))}")

        # 4. wrap() - Wrap into range
        self.debug(c.cyan("\n4. wrap() - Wrap value into range:"))
        examples = [(105, 100), (-10, 100), (50, 100), (250, 100)]
        for value, size in examples:
            wrapped = wrap(value, size)
            self.debug(f"   wrap({value:4d}, {size}) = {c.green(str(wrapped))}")

        # Sum of digit sums
        result = sum(sum(digits(n)) for n in numbers)
        return result

    def part2(self, data: list[str]) -> int:
        """
        Demonstrate advanced numeric utilities.
        """
        self.debug(c.bold("\n=== Part 2: Advanced Numeric Utilities ===\n"))

        # 5. divisors() - Get all divisors
        self.debug(c.cyan("5. divisors() - Find all divisors:"))
        test_nums = [12, 28, 100, 17]
        for num in test_nums:
            divs = divisors(num)
            self.debug(f"   divisors({num:3d}) = {divs}")
            is_prime = len(divs) == 2
            if is_prime:
                self.debug(f"              → {c.green('Prime!')}")

        # 6. gcd() - Greatest common divisor
        self.debug(c.cyan("\n6. gcd() - Greatest common divisor:"))
        pairs = [(12, 8), (24, 36), (15, 25)]
        for a, b in pairs:
            result = gcd(a, b)
            self.debug(f"   gcd({a}, {b}) = {c.green(str(result))}")

        # Multiple numbers
        nums = [24, 36, 48]
        result = gcd(*nums)
        self.debug(f"   gcd({', '.join(map(str, nums))}) = {c.green(str(result))}")

        # Simplify fraction example
        self.debug(c.muted("\n   Use case: Simplify fraction"))
        numerator, denominator = 15, 25
        divisor = gcd(numerator, denominator)
        simplified = (numerator // divisor, denominator // divisor)
        self.debug(f"   {numerator}/{denominator} → {simplified[0]}/{simplified[1]}")

        # 7. lcm() - Least common multiple
        self.debug(c.cyan("\n7. lcm() - Least common multiple:"))
        pairs = [(4, 6), (3, 7), (12, 18)]
        for a, b in pairs:
            result = lcm(a, b)
            self.debug(f"   lcm({a}, {b}) = {c.green(str(result))}")

        # Multiple numbers
        cycles = [3, 4, 5]
        result = lcm(*cycles)
        self.debug(f"   lcm({', '.join(map(str, cycles))}) = {c.green(str(result))}")

        self.debug(c.muted("\n   Use case: Cycle alignment"))
        cycle_periods = ints(data[1])
        aligned = lcm(*cycle_periods)
        self.debug(f"   Cycles {cycle_periods} align at: {c.green(str(aligned))}")

        return aligned
