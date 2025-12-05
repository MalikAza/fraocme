import time

from fraocme import Solver
from fraocme.common.printer import (
    print_dict_head,
    print_dict_row,
    print_ranges,
    print_row_stats,
)
from fraocme.grid import int_grid
from fraocme.profiling.timer import benchmark, timed
from fraocme.ui.colors import c


class Day0(Solver):
    def __init__(self, day: int = 0, debug: bool = False):
        super().__init__(day=day, debug=debug, copy_input=True)

    @timed  # ex timed decorator test
    def parse(self, raw: str) -> list[list[int]]:
        return int_grid(raw)

    def part1(self, data: list[list[int]]) -> int:
        # Example debug output
        self.debug(c.muted("Loaded rows:"), len(data))
        self.debug(lambda: print_row_stats(data[0]))

        # Example: print_ranges
        example_ranges = [(1, 5), (10, 25), (30, 35), (50, 100), (120, 150)]
        self.debug(lambda: print_ranges(example_ranges, head=3, tail=1))

        # Example: print_dict_row
        example_dict = {
            190: [10, 19],
            3267: [81, 40, 27],
            83: [17, 5],
            156: [15, 6, 20],
        }
        self.debug(lambda: print_dict_row(example_dict, 3267))

        # Example: print_dict_head
        self.debug(lambda: print_dict_head(example_dict, n=3))

        time.sleep(0.1)
        return sum(max(line) for line in data)

    @benchmark(iterations=10)  # ex benchmark decorator test
    def part2(self, data: list[list[int]]) -> int:
        time.sleep(0.05)
        return sum(sum(line) for line in data)
