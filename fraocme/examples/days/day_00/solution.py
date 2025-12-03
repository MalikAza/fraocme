from fraocme import Solver
from fraocme.parsers import int_grid


class Day0(Solver):
    def __init__(self, debug: bool = False):
        super().__init__(day=0, debug=debug)
    
    def parse(self, raw: str) -> list[list[int]]:
        return int_grid(raw)
    
    def part1(self, data: list[list[int]]) -> int:
        # Sum of max per line
        return sum(max(line) for line in data)
    
    def part2(self, data: list[list[int]]) -> int:
        # Sum of all
        return sum(sum(line) for line in data)