# Example Days

This directory contains example solutions demonstrating the fraocme framework features.

## Structure

Examples are organized by domain:
- **00-99**: Common utilities (parsers, utils, numeric, ranges)
- **100-199**: Grid functionality (navigation, printing, pathfinding, regions)
- **200-299**: (Reserved for future features)

This allows adding more examples in each category as needed.

## Available Examples

### Common Domain (00-99)

#### Day 00 - Framework Basics
**File**: `day_00/solution.py`

**Demonstrates**:
- `Solver` base class usage
- `@timed` decorator for performance measurement
- `@benchmark` decorator for detailed profiling
- Common printer functions:
  - `print_row_stats()` - statistical analysis
  - `print_ranges()` - range visualization
  - `print_dict_row()` - dictionary row display
  - `print_dict_head()` - dictionary preview
- Debug output with `self.debug()`
- Color utilities from `fraocme.ui.colors`

**Run**: `fraocme run 0 --debug`

---

#### Day 01 - Parser Functions
**File**: `day_101/solution.py`

**Demonstrates**:
- All parser functions from `fraocme.common.parser`
- `sections()` - Split by blank lines
- `lines()` - Parse as list of strings
- `ints()` - Parse integers per line
- `char_lines()` - Parse digit characters
- `key_ints()` - Parse key-value format
- `ranges()` - Parse integer ranges
- `mapped()` - Custom line transformation

**Run**: `fraocme run 1 --debug`

---

#### Day 02 - Sequence Utilities
**File**: `day_02/solution.py`

**Demonstrates**:
- Sequence manipulation from `fraocme.common.sequence_utils`
- `frequencies()` - Count occurrences
- `all_equal()` - Check if all same
- `chunks()` - Fixed-size groups
- `windows()` - Sliding windows
- `pairwise()` - Consecutive pairs
- `rotate()` - Rotate sequences
- `unique()` - Remove duplicates
- `flatten()` - Flatten nested lists

**Run**: `fraocme run 2 --debug`

---

#### Day 03 - Numeric Utilities
**File**: `day_03/solution.py`

**Demonstrates**:
- Numeric functions from `fraocme.math`:
- `sign()` - Get sign (-1, 0, 1)
- `digits()` - Extract digits
- `from_digits()` - Combine digits
- `wrap()` - Modulo wrapping
- `divisors()` - All divisors
- `gcd()` - Greatest common divisor
- `lcm()` - Least common multiple

**Run**: `fraocme run 3 --debug`

---

#### Day 04 - Range Utilities
**File**: `day_04/solution.py`

**Demonstrates**:
- Range manipulation from `fraocme.common.range_utils`
- `ranges_overlap()` - Check overlaps
- `range_intersection()` - Get overlap
- `merge_ranges()` - Merge overlapping ranges
- `within_range()` - Check if value in ranges
- `range_coverage()` - Calculate coverage

**Run**: `fraocme run 4 --debug`

---

#### Day 05 - Rectangle / Coordinate Utilities
**File**: `day_05/solution.py`

**Demonstrates**:
- Parsing coordinate lists and character grids
- Building outlines and flood-filling regions with `fraocme.common.coordinate_utils`
- Finding largest valid rectangles using `largest_valid_rectangle()`
- Grid display and highlighting with `fraocme.grid` printers

**Run**: `fraocme run 5 --debug`

---

#### Day 06 - Graph Utilities
**File**: `day_06/solution.py`

**Demonstrates**:
- Counting DAG paths between two nodes with `count_paths_dag()`
- Listing example paths with `enumerate_all_paths()`
- Finding critical nodes that all paths pass through with `find_critical_nodes()`
- Pretty debug printing using `fraocme.graph.printer` and `fraocme.ui.colors`

**Run**: `fraocme run 6 --debug`

---

### Grid Domain (100-199)

#### Day 101 - Grid Navigation & Simulation
**File**: `day_01/solution.py`

**Demonstrates**:
- Grid parsing with `Grid.from_chars()`
- Finding positions with `grid.find_first()`
- Modern direction system (`NORTH, SOUTH, EAST, WEST`)
- Direction operations (`turn_right()`, `turn_left()`)
- Moving with `grid.neighbor(pos, direction)`
- Position tracking and loop detection
- Guard patrol simulation

**Run**: `fraocme run 101 --debug`

---

#### Day 102 - Grid Printer Functions
**File**: `day_102/solution.py`

**Demonstrates**:
- All grid printer functions:
  - `print_grid()` - basic grid display with pagination
  - `print_grid_heatmap()` - value-based color coding
  - `print_grid_path()` - path visualization with arrows
  - `print_grid_diff()` - comparing two grids
  - `print_grid_neighbors()` - neighbor visualization
- Coordinate display options
- Truncation for large grids
- Color-coded value display

**Run**: `fraocme run 102 --debug`

---

#### Day 103 - Animated Grid Visualization
**File**: `day_103/solution.py`

**Demonstrates**:
- `print_grid_animated()` - basic movement animation
- `print_grid_animated_with_direction()` - directional arrows
- Console clearing for smooth animation
- Trail effects showing movement history
- Speed control with `delay` parameter
- Step-by-step visualization
- Real-time guard patrol animation

**Run**: `fraocme run 103 --debug`

**Note**: Use Ctrl+C to stop animations early

---

#### Day 104 - Pathfinding Algorithms
**File**: `day_104/solution.py`

**Demonstrates**:
- BFS (Breadth-First Search) for unweighted pathfinding
- Dijkstra's algorithm for weighted paths
- A* algorithm with heuristics
- Manhattan distance calculations
- Cost functions for different terrain
- Path visualization
- Performance comparison between algorithms

**Run**: `fraocme run 104 --debug`

---

#### Day 105 - Region Analysis
**File**: `day_105/solution.py`

**Demonstrates**:
- `flood_fill()` for connected regions
- `find_regions()` for all connected components
- Region properties (size, bounds)
- 4-directional connectivity (NSEW)
- Region visualization
- Practical applications (island counting, area calculation)

**Run**: `fraocme run 105 --debug`

---

## Running Examples

### Run a specific example:
```bash
fraocme run <day> --debug
```

### Run with profiling:
```bash
fraocme run <day> --debug --profile
```

### Show example input:
```bash
fraocme show <day>
```

## Learning Path

**Beginner - Common Domain**:
1. Day 00 - Learn framework basics
2. Day 01 - Master parser functions
3. Day 02 - Explore sequence utilities
4. Day 03 - Understand numeric operations
5. Day 04 - Work with ranges

**Intermediate - Grid Domain**:
6. Day 101 - Understand grid navigation
7. Day 102 - Explore printer functions
8. Day 103 - Add animations to visualizations

**Advanced - Grid Domain**:
9. Day 104 - Implement pathfinding
### Common Domain Imports
```python
from fraocme import Solver
from fraocme.common.parser import sections, lines, ints, key_ints
from fraocme.common.sequence_utils import chunks, windows, frequencies, pairwise, all_equal
from fraocme.common.printer import print_ranges, print_dict_head
from fraocme.ui.colors import c
```

### Grid Domain Imports
```python
from fraocme import Solver
from fraocme.grid import Grid, NORTH, SOUTH, EAST, WEST
from fraocme.grid.printer import print_grid, print_grid_animated
from fraocme.ui.colors import c
```m fraocme import Solver
from fraocme.grid import Grid, NORTH, SOUTH, EAST, WEST
from fraocme.grid.printer import print_grid, print_grid_animated
from fraocme.ui.colors import c
```

### Basic Solver Structure
```python
class DayX(Solver):
### Common Utilities
```python
# Parsing
blocks = sections(raw)          # Split by blank lines
numbers = ints(raw)             # Parse integers
equations = key_ints(raw)       # Parse key: values

# Sequences
groups = chunks(data, 3)        # Fixed groups
wins = windows(data, 3)         # Sliding windows
pairs = pairwise(data)          # Consecutive pairs

# Numeric
result = gcd(12, 8)             # GCD
aligned = lcm(3, 4, 5)          # LCM
parts = digits(1234)            # [1,2,3,4]
```

### Grid Basics
```python
grid = Grid.from_chars(raw)
pos = grid.find_first("S")
next_pos = grid.neighbor(pos, NORTH)
value = grid.at(x, y)
```     return result
    
    def part2(self, data):
        # Solve part 2
        return result
```

### Grid Basics
```python
grid = Grid.from_chars(raw)
pos = grid.find_first("S")
next_pos = grid.neighbor(pos, NORTH)
value = grid.at(x, y)
```

### Debugging
```python
self.debug("Message")                    # Print in debug mode
self.debug(c.cyan("Colored message"))    # With colors
self.debug(lambda: expensive_function()) # Lazy evaluation
```

## Tips

- Use `--debug` flag to see all debug output
- Examples use realistic Advent of Code style inputs
- Each example is self-contained and runnable
- Modify examples to experiment with features
- Check README.md files in each day folder for detailed explanations
