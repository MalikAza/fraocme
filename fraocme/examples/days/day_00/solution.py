import time

from fraocme import Solver
from fraocme.grid import int_grid, print_grid
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
        self.debug(lambda: print_grid(data))

        time.sleep(0.1)
        return sum(max(line) for line in data)

    @benchmark(iterations=10)  # ex benchmark decorator test
    def part2(self, data: list[list[int]]) -> int:
        time.sleep(0.05)
        return sum(sum(line) for line in data)
