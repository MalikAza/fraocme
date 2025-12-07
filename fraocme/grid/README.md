# Grid Module - Refactored

A high-performance, immutable 2D grid system for Advent of Code puzzles.

## Key Features

- **Immutable with Structural Sharing**: Grid operations return new instances, but reuse unchanged data
- **Generic Type Support**: `Grid[T]` works with any type (int, str, custom types)
- **Modern Direction System**: Dataclass-based directions with rich operations
- **Neighbor Queries**: Ring-based neighbor finding with cardinal/diagonal support
- **Lazy Indexing**: Fast value lookups with automatic caching
- **Pathfinding**: BFS, Dijkstra, and A* implementations
- **Region Analysis**: Flood fill and connected component detection
- **Transformations**: Rotate, flip, transpose operations

## Quick Start

```python
from fraocme.grid import Grid, NORTH, SOUTH, EAST, WEST

# Parse from string
grid = Grid.from_ints("123\n456\n789")
grid = Grid.from_chars("abc\ndef\nghi")
grid = Grid.from_dense("1 2 3\n4 5 6")  # space-separated

# Access cells
value = grid.at(1, 1)  # x=1, y=1 (center cell)
value = grid[1][1]     # also works (row, then column)

# Grid properties
w, h = grid.dimensions
print(grid.width, grid.height)

# Find values
positions = grid.find(5)        # list of all positions with value 5
pos = grid.find_first('a')      # first position with 'a', or None
```

## Neighbor Operations

```python
# Get neighbors at different rings
neighbors = grid.get_neighbors((1, 1), ring=1, include_diagonals=True)
# Ring 1 with diagonals = 8 neighbors (3x3 minus center)
# Ring 1 cardinal only = 4 neighbors (NSEW)

neighbors = grid.get_neighbors((1, 1), ring=2, include_diagonals=True)
# Ring 2 with diagonals = 16 neighbors (5x5 minus inner 3x3)

# Get neighbor values
neighbor_vals = grid.get_neighbor_values((1, 1), ring=1)
# Returns list of (position, value) tuples
```

## Directions

```python
from fraocme.grid import (
    NORTH, SOUTH, EAST, WEST,           # Cardinal
    NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST,  # Diagonals
    turn_left, turn_right, opposite
)

# Get neighbor in a direction
new_pos = grid.neighbor((1, 1), NORTH)  # Returns neighbor position or None if out of bounds
new_pos = grid.neighbor((1, 1), EAST, 3)  # Get position 3 steps east

# Direction operations
left = turn_left(NORTH)    # Returns WEST
right = turn_right(NORTH)  # Returns EAST
back = opposite(NORTH)     # Returns SOUTH

# Access direction properties
print(NORTH.name)   # "north"
print(NORTH.delta)  # (0, -1)
```

## Immutable Updates

```python
# Single cell update (creates new Grid, reuses unchanged rows)
new_grid = grid.set(1, 1, 9)

# Bulk updates (efficient - groups by row)
changes = {(0, 0): 9, (2, 2): 9, (1, 1): 5}
new_grid = grid.bulk_set(changes)

# Original grid is unchanged!
```

## Transformations

```python
# All return new Grid instances
rotated = grid.rotate_90()     # Clockwise
rotated = grid.rotate_180()
rotated = grid.rotate_270()

flipped = grid.flip_horizontal()
flipped = grid.flip_vertical()

transposed = grid.transpose()  # Swap rows/columns
```

## Pathfinding

Built-in algorithms:
- **bfs**: Unweighted shortest path (every step costs 1). No heuristic. Great for mazes and small/medium grids with uniform step cost.
- **dijkstra**: Weighted shortest path. Use when move costs vary (terrain, risk) and you do not have a reliable heuristic.
- **a_star**: Weighted with heuristic guidance. Best balance of speed and optimality if you provide an admissible heuristic.

Heuristics:
- **manhattan_distance(p1, p2)**: Sum of |dx| + |dy|. Use for 4-way movement with equal costs.
- **chebyshev_distance(p1, p2)**: max(|dx|, |dy|). Use for 8-way movement when diagonals cost the same as cardinals.

When to choose which:
- Choose **bfs** for uniform-cost grids where you only care about fewest steps and the map is not huge.
- Choose **dijkstra** for varying costs when you need a guaranteed optimum and lack a good heuristic.
- Choose **a_star** for varying costs when you have a decent heuristic; this is usually fastest on large grids.

Examples:
```python
from fraocme.grid import Grid, bfs, dijkstra, a_star, manhattan_distance
from fraocme.grid.directions import CARDINALS

grid = Grid.from_chars("""
S..
.#.
..E
""")

# BFS (uniform cost)
path = bfs(
    grid,
    start=grid.find_first("S"),
    end=grid.find_first("E"),
    is_walkable=lambda pos, val: val != "#",
    directions=CARDINALS,
)

# Dijkstra (weighted)
cost_map = {".": 1, "~": 5, "#": None}
path = dijkstra(
    grid,
    start=grid.find_first("S"),
    end=grid.find_first("E"),
    cost_fn=lambda src, sv, dst, dv: float("inf") if dv == "#" else cost_map.get(dv, 1),
    directions=CARDINALS,
)

# A* (weighted + heuristic)
path = a_star(
    grid,
    start=grid.find_first("S"),
    end=grid.find_first("E"),
    heuristic=manhattan_distance,
    cost_fn=lambda src, sv, dst, dv: 1 if dv != "#" else float("inf"),
    directions=CARDINALS,
)

if path:
    print(f"Path length: {path.length}")
    print(f"Path cost: {path.cost}")
    print(f"Path: {path.positions}")
```

## Region Analysis

```python
# Flood fill from a position
region = grid.flood_fill(start=(0, 0), predicate='.')
# Or use a function: predicate=lambda cell: cell != '#'

print(f"Region size: {region.size}")
print(f"Bounds: {region.bounds}")  # ((min_x, min_y), (max_x, max_y))

# Find all connected regions
regions = grid.find_regions('#')
for i, region in enumerate(regions):
    print(f"Region {i}: size={region.size}")
```

## Advanced Operations

```python
# Map function over all cells
grid2 = grid.map(lambda x: x * 2)

# Filter positions by predicate
positions = grid.filter_positions(lambda pos, val: val > 5)

# Check bounds
if grid.in_bounds((10, 10)):
    value = grid.at(10, 10)
```

## Position Convention

**Important**: Positions use `(x, y)` where:
- `x` = column (horizontal, increases right)
- `y` = row (vertical, increases down)

Grid access: `grid[y][x]` or `grid.at(x, y)`

```
     x=0 x=1 x=2
y=0   1   2   3
y=1   4   5   6
y=2   7   8   9

Position (1, 1) is the center cell with value 5
```

## Performance Notes

- Grid uses `tuple[tuple[T, ...], ...]` for immutability
- Structural sharing: `set()` only copies affected row
- Lazy indexing: `find()` builds index on first call, cached thereafter
- All transformations create new Grid but reuse data where possible
- Ring neighbors use optimized Chebyshev/Manhattan distance algorithms

## Architecture Notes

The grid module is organized into focused modules:
- `core.py` - Main Grid[T] class with immutable operations
- `directions.py` - Modern direction system with Direction dataclass
- `parser.py` - Factory methods for grid creation
- `transformations.py` - Rotation, flip, transpose operations
- `pathfinding.py` - BFS, Dijkstra, A* algorithms
- `regions.py` - Connected component analysis
- `types.py` - Type definitions (Position)
