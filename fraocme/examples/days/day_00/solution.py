from fraocme import Solver
from fraocme.debug.colors import c
from fraocme.debug.printer import print_max_in_rows
from fraocme.parsers import int_grid
import time

from fraocme.profiling.timer import benchmark, timed

class Day0(Solver):
    def __init__(self, debug: bool = False):
        super().__init__(day=0, debug=debug, copy_input=True)

    @timed # ex timed decorator test
    def parse(self, raw: str) -> list[list[int]]:
        return int_grid(raw)
    
    def part1(self, data: list[list[int]]) -> int:
        # Example debug output
        self.debug(c.muted("Loaded rows:"), len(data))
        self.debug(lambda: print_max_in_rows(data))

        time.sleep(0.1)
        e # ex traceback error test
        return sum(max(line) for line in data)
    
    @benchmark(iterations=10) # ex benchmark decorator test
    def part2(self, data: list[list[int]]) -> int:
        time.sleep(0.05)
        return sum(sum(line) for line in data)