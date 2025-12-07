# Example Days

This directory contains example solutions demonstrating the fraocme framework features.

## Available Examples

### Day 00 - Framework Basics
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

### Day 01 - Grid Navigation & Simulation
**File**: `day_01/solution.py`

**Demonstrates**:
- Grid parsing with `Grid.from_chars()`
- Finding positions with `grid.find_first()`
- Modern direction system (`NORTH, SOUTH, EAST, WEST`)
- Direction operations (`turn_right()`, `turn_left()`)
- Moving with `grid.neighbor(pos, direction)`
- Position tracking and loop detection
- Guard patrol simulation

**Run**: `fraocme run 1 --debug`

---

### Day 02 - Grid Printer Functions
**File**: `day_02/solution.py`

**Demonstrates**:
- All grid printer functions:
  - `print_grid()` - basic grid display with pagination
  - `print_grid_heatmap()` - value-based color coding
  - `print_grid_path()` - path visualization with arrows
  - `print_grid_diff()` - comparing two grids
  - `print_grid_region()` - highlighting regions
  - `print_grid_neighbors()` - neighbor visualization
- Coordinate display options
- Truncation for large grids
- Color-coded value display

**Run**: `fraocme run 2 --debug`

---

### Day 03 - Animated Grid Visualization
**File**: `day_03/solution.py`

**Demonstrates**:
- `print_grid_animated()` - basic movement animation
- `print_grid_animated_with_direction()` - directional arrows
- Console clearing for smooth animation
- Trail effects showing movement history
- Speed control with `delay` parameter
- Step-by-step visualization
- Real-time guard patrol animation

**Run**: `fraocme run 3 --debug`

**Note**: Use Ctrl+C to stop animations early

---

### Day 04 - Pathfinding Algorithms
**File**: `day_04/solution.py`

**Demonstrates**:
- BFS (Breadth-First Search) for unweighted pathfinding
- Dijkstra's algorithm for weighted paths
- A* algorithm with heuristics
- Manhattan distance calculations
- Cost functions for different terrain
- Path visualization
- Performance comparison between algorithms

**Run**: `fraocme run 4 --debug`

---

### Day 05 - Region Analysis
**File**: `day_05/solution.py`

**Demonstrates**:
- `flood_fill()` for connected regions
- `find_regions()` for all connected components
- Region properties (size, bounds)
- 4-directional connectivity (NSEW)
- Region visualization
- Practical applications (island counting, area calculation)

**Run**: `fraocme run 5 --debug`

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

**Beginner**:
1. Day 00 - Learn framework basics
2. Day 01 - Understand grid navigation
3. Day 02 - Explore printer functions

**Intermediate**:
4. Day 03 - Add animations to visualizations
5. Day 04 - Implement pathfinding

**Advanced**:
6. Day 05 - Work with regions and connected components

## Quick Reference

### Common Imports
```python
from fraocme import Solver
from fraocme.grid import Grid, NORTH, SOUTH, EAST, WEST
from fraocme.grid.printer import print_grid, print_grid_animated
from fraocme.ui.colors import c
```

### Basic Solver Structure
```python
class DayX(Solver):
    def parse(self, raw: str):
        # Parse input
        return data
    
    def part1(self, data):
        # Solve part 1
        return result
    
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
