text

# Fraocme

A Python framework for Advent of Code solutions.

## Installation

```bash
pip install -e .

Quick Start
1. Create project structure

text

my-aoc-2024/
├── days/
│   └── day_01/
│       ├── input.txt
│       └── solution.py

2. Write your solution

python

# days/day_01/solution.py

from fraocme import Solver
from fraocme.parsers import int_grid


class Day1(Solver):
    def __init__(self, debug: bool = False):
        super().__init__(day=1, debug=debug)
    
    def parse(self, raw: str) -> list[list[int]]:
        return int_grid(raw)
    
    def part1(self, data: list[list[int]]) -> int:
        return sum(max(line) for line in data)
    
    def part2(self, data: list[list[int]]) -> int:
        return sum(sum(line) for line in data)

3. Run it

bash

fraocme run 1

CLI Commands

bash

# Run a specific day
fraocme run 1

# Run specific part only
fraocme run 1 -p 1

# Run with debug output
fraocme run 1 --debug

# Run all days
fraocme run --all

# View stats
fraocme stats
fraocme stats 1
fraocme stats --best

# Create new day from template
fraocme init 5

Available Parsers

python

from fraocme.parsers import (
    # Basic
    lines,          # ["line1", "line2"]
    ints,           # [1, 2, 3] (one int per line)
    ints_per_line,  # [[1, 2], [3, 4]] (multiple ints per line)
    
    # Grid
    char_grid,      # [['a','b'], ['c','d']]
    int_grid,       # [[1,2], [3,4]] (single digits)
    
    # Blocks
    blocks,         # Split by blank lines
    
    # CSV
    csv,            # ["a", "b", "c"]
    csv_ints,       # [1, 2, 3]
    
    # Regex
    extract_ints,   # All ints in string: "x=42, y=-10" -> [42, -10]
    groups,         # Regex groups
    
    # Grid class
    Grid,           # 2D grid with utilities
    Point,          # (x, y) with helpers
    Direction,      # N, S, E, W, etc.
)

Grid Example

python

from fraocme import Solver
from fraocme.parsers import Grid, Point, CARDINALS


class Day10(Solver):
    def __init__(self, debug: bool = False):
        super().__init__(day=10, debug=debug)
    
    def parse(self, raw: str) -> Grid[int]:
        return Grid.from_string(raw, int)
    
    def part1(self, grid: Grid[int]) -> int:
        start = grid.find(0)
        
        for neighbor in grid.neighbors(start):
            value = grid[neighbor]
            # ...
        
        return 0
    
    def part2(self, grid: Grid[int]) -> int:
        return 0

Debug Mode

python

class Day1(Solver):
    def part1(self, data) -> int:
        self.debug("Processing data:", len(data))  # Only prints with --debug flag
        
        # Use internal timer for profiling sections
        self.timer.start()
        result = self.heavy_computation(data)
        self.debug(f"Heavy computation: {self.timer.stop():.2f}ms")
        
        return result

Stats

Times are automatically saved to stats.json after each run.

bash

# View all stats
fraocme stats

# Summary table
fraocme stats --best

Output:

text

══════════════════════════════════════════════════
  Advent of Code Stats
══════════════════════════════════════════════════

  Day    Part 1         Part 2        
  ------ -------------- --------------
  1      0.42ms         1.23ms        
  2      12.34ms        45.67ms       

──────────────────────────────────────────────────
  Total (4 parts): 59.66ms

text