# Day 1 Example: Guard Patrol Simulation

This example demonstrates the modern Grid module features with a practical Advent of Code-style puzzle.

## Problem

A guard patrols a mapped area, following these rules:
- Starts at position marked `^`, facing NORTH
- If there's an obstacle `#` directly ahead, turns right 90°
- Otherwise, moves forward one step
- Continues until leaving the mapped area

### Part 1
Count how many distinct positions the guard visits before leaving the area.

### Part 2
Find how many positions you could place a single new obstacle to cause the guard to get stuck in a loop.

## Grid Module Features Demonstrated

### 1. Grid Parsing
```python
grid = Grid.from_chars(raw)  # Parse character grid
```

### 2. Finding Positions
```python
start = grid.find_first('^')  # Find single position
obstacles = grid.find('#')     # Find all obstacles
```

### 3. Grid Properties
```python
width, height = grid.dimensions
in_bounds = grid.in_bounds(pos)
```

### 4. Direction System
```python
from fraocme.grid import NORTH, SOUTH, EAST, WEST, turn_right

direction = NORTH
direction = turn_right(direction)  # Now EAST
```

### 5. Movement with Boundary Checking
```python
next_pos = grid.neighbor(pos, direction)
if next_pos is None:
    # Moved out of bounds
    break
```

### 6. Cell Access
```python
cell = grid.at(x, y)          # Access by (x, y)
cell = grid[y][x]             # Or by [row][col]
```

### 7. Immutable Updates
```python
# Create new grid with obstacle added
new_grid = grid.set(x, y, '#')
# Original grid unchanged!
```

### 8. Position Filtering
```python
empty_positions = grid.filter_positions(lambda pos, val: val == '.')
```

## Running the Example

```python
from fraocme.examples.days.day_01.solution import Day1
from pathlib import Path

solver = Day1(day=1, debug=True)
solver.set_input_dir(Path('fraocme/examples/days/day_01'))
results = solver.run()
```

Or use the CLI:
```bash
fraocme run 1 --example
```

## Expected Output

```
Starting at: (4, 6)
Grid dimensions: (10, 10)
...
Distinct positions visited: 41
  Part one: 41 (0.81ms)

Testing 91 positions for loops
Positions causing loops: 6
  Part two: 6 (3.53ms)
```

## Key Implementation Details

### Loop Detection
Uses state tracking `(position, direction)` to detect when the guard revisits a previous state:
```python
states = {(pos, direction)}
while True:
    # ... movement logic ...
    state = (pos, direction)
    if state in states:
        return True  # Loop detected!
    states.add(state)
```

### Efficient Testing
Tests each empty position by creating a modified grid:
```python
for obstacle_pos in empty_positions:
    test_grid = grid.set(*obstacle_pos, '#')
    if creates_loop(test_grid, start):
        loop_count += 1
```

## Performance Notes

- Grid parsing: < 1ms
- Part 1 simulation: < 1ms
- Part 2 testing ~91 positions: ~3ms
- Total: ~4ms

The immutable Grid with structural sharing makes testing multiple obstacle positions efficient!

## Learning Points

1. **Modern Direction System**: No more string symbols - use Direction objects with names and deltas
2. **Type Safety**: `Grid[str]` ensures type checking throughout
3. **Immutability**: Original grid never changes, making parallel testing safe
4. **Boundary Checking**: `grid.neighbor()` returns `None` when out of bounds
5. **State Tracking**: Tuples like `(pos, direction)` work perfectly in sets for loop detection
6. **Debug Mode**: Toggle with `debug=True` for detailed step-by-step output
