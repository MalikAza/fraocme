import time
from statistics import median
from typing import TYPE_CHECKING, Any, Callable

from ..ui.colors import c
from .types import Position

if TYPE_CHECKING:
    from .core import Grid


def print_grid(
    grid: "Grid | list[list[Any]]",
    separator: str = "",
    highlight: set[Position] | None = None,
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print a 2D grid with optional position highlighting and size limits.

    Args:
        grid: 2D grid to print
        separator: String to place between cells (default: no separator)
        highlight: Optional set of positions to highlight in cyan
        max_rows: Maximum rows to display (None = all). Default: 25
        max_cols: Maximum cols to display (None = all). Default: 80
        show_coords: Show row/column coordinates

    Example:
        grid = Grid.from_chars("abc\\ndef\\nghi")
        print_grid(grid, separator=' ', highlight={(1, 1)}, show_coords=True)
    """
    # Get dimensions
    if hasattr(grid, "height"):
        height, width = grid.height, grid.width
    else:
        height, width = len(grid), len(grid[0]) if grid else 0

    # Determine what to print
    rows_to_print = min(height, max_rows) if max_rows else height
    cols_to_print = min(width, max_cols) if max_cols else width

    truncated_rows = height > rows_to_print
    truncated_cols = width > cols_to_print

    # Print header if coords enabled
    if show_coords and cols_to_print > 0:
        header = "   " if show_coords else ""
        header += separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        # Row coordinate
        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        # Cells
        for x in range(cols_to_print):
            cell = grid[y][x] if isinstance(grid, list) else grid.at(x, y)
            cell_str = str(cell)
            if highlight and (x, y) in highlight:
                cell_str = c.cyan(cell_str)
            line_parts.append(cell_str)

        # Truncation indicator
        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    # Footer if truncated
    if truncated_rows:
        footer = c.dim(
            f"... ({height - rows_to_print} more rows, {height}x{width} total)"
        )
        print(footer)


def print_grid_heatmap(
    grid: "Grid",
    value_fn: Callable[[Any], float] | None = None,
    separator: str = " ",
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print grid with color-coded values (heat map visualization).

    Automatically colors cells based on min/max/median values using c.stat().

    Args:
        grid: Grid to visualize
        value_fn: Optional function to extract numeric value from cell
                  (default: identity)
        separator: String between cells
        max_rows: Maximum rows to display (None = all)
        max_cols: Maximum cols to display (None = all)
        show_coords: Show row/column coordinates

    Example:
        grid = Grid.from_ints("123\\n456\\n789")
        print_grid_heatmap(grid)  # Colors: 1=red(min), 5=yellow(median), 9=green(max)
    """
    # Extract all values
    values = []
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.at(x, y)
            val = value_fn(cell) if value_fn else cell
            if isinstance(val, (int, float)):
                values.append(val)

    if not values:
        print(c.dim("(empty or non-numeric grid)"))
        return

    min_val, max_val, median_val = min(values), max(values), median(values)

    # Determine what to print
    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    truncated_rows = grid.height > rows_to_print
    truncated_cols = grid.width > cols_to_print

    # Print header
    if show_coords:
        header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    # Print legend
    legend = (
        f"Legend: {c.green('max')}={max_val} "
        f"{c.yellow('median')}={median_val} {c.red('min')}={min_val}"
    )
    print(c.dim(legend))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        for x in range(cols_to_print):
            cell = grid.at(x, y)
            val = value_fn(cell) if value_fn else cell

            # Color based on value
            if isinstance(val, (int, float)):
                cell_str = c.stat(val, min_val, max_val, median_val)
            else:
                cell_str = c.dim(str(cell))

            line_parts.append(cell_str)

        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    if truncated_rows:
        footer = (
            f"... ({grid.height - rows_to_print} more rows, "
            f"{grid.height}x{grid.width} total)"
        )
        print(c.dim(footer))


def print_grid_path(
    grid: "Grid",
    path: list[Position],
    separator: str = " ",
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print grid with a path highlighted (shows direction arrows).

    Args:
        grid: Grid to print
        path: List of positions forming a path
        separator: String between cells
        max_rows: Maximum rows to display
        max_cols: Maximum cols to display
        show_coords: Show coordinates

    Example:
        from fraocme.grid import bfs
        path_result = bfs(grid, start=(0,0), end=(5,5), is_walkable=lambda p,v: v!='#')
        if path_result:
            print_grid_path(grid, path_result.positions)
    """
    path_set = set(path)
    path_indices = {pos: i for i, pos in enumerate(path)}

    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    truncated_rows = grid.height > rows_to_print
    truncated_cols = grid.width > cols_to_print

    # Header
    if show_coords:
        header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        for x in range(cols_to_print):
            pos = (x, y)
            cell = grid.at(x, y)

            if pos in path_set:
                idx = path_indices[pos]

                # Determine arrow direction
                if idx == 0:
                    arrow = "S"  # Start
                elif idx == len(path) - 1:
                    arrow = "E"  # End
                else:
                    prev_pos = path[idx - 1]
                    next_pos = path[idx + 1]
                    dx = next_pos[0] - prev_pos[0]
                    dy = next_pos[1] - prev_pos[1]

                    # Arrow mapping
                    if dx > 0:
                        arrow = "→"
                    elif dx < 0:
                        arrow = "←"
                    elif dy > 0:
                        arrow = "↓"
                    elif dy < 0:
                        arrow = "↑"
                    else:
                        arrow = "•"

                cell_str = c.cyan(arrow)
            else:
                cell_str = c.dim(str(cell))

            line_parts.append(cell_str)

        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    if truncated_rows:
        footer = (
            f"... ({grid.height - rows_to_print} more rows, "
            f"{grid.height}x{grid.width} total)"
        )
        print(c.dim(footer))

    print(c.dim(f"Path length: {len(path)} steps"))


def print_grid_diff(
    grid1: "Grid",
    grid2: "Grid",
    separator: str = " ",
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print difference between two grids (highlights changes).

    Args:
        grid1: First grid (baseline)
        grid2: Second grid (comparison)
        separator: String between cells
        max_rows: Maximum rows to display
        max_cols: Maximum cols to display
        show_coords: Show coordinates

    Example:
        original = Grid.from_chars("abc\\ndef\\nghi")
        modified = original.set(1, 1, "X")
        print_grid_diff(original, modified)  # Shows X highlighted
    """
    if grid1.dimensions != grid2.dimensions:
        print(c.error(f"Dimension mismatch: {grid1.dimensions} vs {grid2.dimensions}"))
        return

    rows_to_print = min(grid1.height, max_rows) if max_rows else grid1.height
    cols_to_print = min(grid1.width, max_cols) if max_cols else grid1.width

    truncated_rows = grid1.height > rows_to_print
    truncated_cols = grid1.width > cols_to_print

    changes = 0

    # Header
    if show_coords:
        header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        for x in range(cols_to_print):
            cell1 = grid1.at(x, y)
            cell2 = grid2.at(x, y)

            if cell1 != cell2:
                cell_str = c.success(str(cell2))  # Green for changes
                changes += 1
            else:
                cell_str = c.dim(str(cell2))

            line_parts.append(cell_str)

        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    if truncated_rows:
        footer = (
            f"... ({grid1.height - rows_to_print} more rows, "
            f"{grid1.height}x{grid1.width} total)"
        )
        print(c.dim(footer))

    print(c.dim(f"Changes: {changes} cells"))


def print_grid_region(
    grid: "Grid",
    region: Any,  # Region type
    separator: str = " ",
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print grid with a region highlighted.

    Args:
        grid: Grid to print
        region: Region object with .positions attribute
        separator: String between cells
        max_rows: Maximum rows to display
        max_cols: Maximum cols to display
        show_coords: Show coordinates

    Example:
        from fraocme.grid import flood_fill
        region = grid.flood_fill((0, 0), '#')
        print_grid_region(grid, region)
    """
    region_positions = region.positions if hasattr(region, "positions") else set(region)

    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    truncated_rows = grid.height > rows_to_print
    truncated_cols = grid.width > cols_to_print

    # Header
    if show_coords:
        header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    print(c.dim(f"Region size: {len(region_positions)} cells"))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        for x in range(cols_to_print):
            pos = (x, y)
            cell = grid.at(x, y)

            if pos in region_positions:
                cell_str = c.cyan(str(cell))
            else:
                cell_str = c.dim(str(cell))

            line_parts.append(cell_str)

        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    if truncated_rows:
        footer = (
            f"... ({grid.height - rows_to_print} more rows, "
            f"{grid.height}x{grid.width} total)"
        )
        print(c.dim(footer))


def print_grid_neighbors(
    grid: "Grid",
    pos: Position,
    ring: int = 1,
    include_diagonals: bool = True,
    separator: str = " ",
    max_rows: int | None = 25,
    max_cols: int | None = 80,
    show_coords: bool = False,
) -> None:
    """
    Print grid with neighbors of a position highlighted.

    Args:
        grid: Grid to print
        pos: Center position
        ring: Neighbor ring distance (1=immediate, 2=next layer, etc.)
        include_diagonals: Include diagonal neighbors
        separator: String between cells
        max_rows: Maximum rows to display
        max_cols: Maximum cols to display
        show_coords: Show coordinates

    Example:
        grid = Grid.from_chars("abc\\ndef\\nghi")
        print_grid_neighbors(grid, (1, 1), ring=1, include_diagonals=True)
    """
    neighbors = grid.get_neighbors(pos, ring=ring, include_diagonals=include_diagonals)
    neighbor_set = set(neighbors)

    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    truncated_rows = grid.height > rows_to_print
    truncated_cols = grid.width > cols_to_print

    # Header
    if show_coords:
        header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
        if truncated_cols:
            header += f" {c.dim('...')}"
        print(c.dim(header))

    diagonal_text = "with diagonals" if include_diagonals else "cardinal only"
    info = f"Center: {pos}, Ring: {ring} ({diagonal_text}), Neighbors: {len(neighbors)}"
    print(c.dim(info))

    # Print rows
    for y in range(rows_to_print):
        line_parts = []

        if show_coords:
            line_parts.append(c.dim(f"{y:2} "))

        for x in range(cols_to_print):
            cell_pos = (x, y)
            cell = grid.at(x, y)

            if cell_pos == pos:
                cell_str = c.success(str(cell))  # Green for center
            elif cell_pos in neighbor_set:
                cell_str = c.cyan(str(cell))  # Cyan for neighbors
            else:
                cell_str = c.dim(str(cell))

            line_parts.append(cell_str)

        if truncated_cols:
            line_parts.append(c.dim("..."))

        print(separator.join(line_parts))

    if truncated_rows:
        footer = (
            f"... ({grid.height - rows_to_print} more rows, "
            f"{grid.height}x{grid.width} total)"
        )
        print(c.dim(footer))


def print_grid_animated(
    grid: "Grid",
    positions: list[Position],
    delay: float = 0.1,
    separator: str = " ",
    max_rows: int | None = 50,
    max_cols: int | None = 100,
    show_coords: bool = True,
    trail_length: int = 0,
    show_step_count: bool = True,
    max_iterations: int = 200,
) -> None:
    """
    Animate movement through grid positions (clears console each frame).

    Perfect for visualizing guard patrols, pathfinding, or any sequential movement.

    Args:
        grid: Grid to display
        positions: List of positions to animate through
        delay: Seconds between frames (default: 0.1)
        separator: String between cells
        max_rows: Maximum rows to display (default: 50 for animations)
        max_cols: Maximum cols to display (default: 100 for animations)
        show_coords: Show row/column coordinates
        trail_length: Number of previous positions to show as trail (0=none)
        show_step_count: Show current step number
        max_iterations: Maximum frames to display (default: 200). If positions > max,
                        frames are skipped to stay within limit

    Example:
        # Day 1 guard patrol animation
        grid = Grid.from_chars(raw_input)
        path = simulate_guard_patrol(grid)
        print_grid_animated(grid, path, delay=0.05, trail_length=10)
    """
    if not positions:
        print(c.dim("(no positions to animate)"))
        return

    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    # Calculate frame skipping if needed
    total_positions = len(positions)
    if total_positions > max_iterations:
        # Calculate step size to reduce frames to max_iterations
        step_size = total_positions / max_iterations
        frame_indices = [int(i * step_size) for i in range(max_iterations)]
        # Always include the last position
        if frame_indices[-1] != total_positions - 1:
            frame_indices[-1] = total_positions - 1
        print(
            c.dim(
                f"Showing {max_iterations}/{total_positions} positions "
                f"(skipping frames)"
            )
        )
    else:
        frame_indices = list(range(total_positions))

    # Calculate total lines for the animation area
    total_lines = rows_to_print
    if show_coords:
        total_lines += 1  # Header line
    if show_step_count:
        total_lines += 1  # Step counter line

    for frame_num, step in enumerate(frame_indices):
        current_pos = positions[step]

        # Move cursor up to overwrite previous frame (except first frame)
        if frame_num > 0:
            # ANSI escape: move cursor up N lines
            print(f"\033[{total_lines}A", end="")

        # Calculate trail positions
        trail_positions = set()
        if trail_length > 0 and step > 0:
            trail_start = max(0, step - trail_length)
            trail_positions = set(positions[trail_start:step])

        # Print header
        if show_coords:
            header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
            print(c.dim(header))

        if show_step_count:
            print(c.dim(f"Step {step + 1}/{total_positions} - Position: {current_pos}"))

        # Print rows
        for y in range(rows_to_print):
            line_parts = []

            if show_coords:
                line_parts.append(c.dim(f"{y:2} "))

            for x in range(cols_to_print):
                pos = (x, y)
                cell = grid.at(x, y)

                if pos == current_pos:
                    # Current position - bright cyan/bold @ symbol
                    cell_str = c.cyan(c.bold("@"))
                elif pos in trail_positions:
                    # Trail - bright yellow + symbol
                    cell_str = c.yellow("+")
                else:
                    # Normal cell
                    cell_str = c.dim(str(cell))

                line_parts.append(cell_str)

            print(separator.join(line_parts))

        # Sleep before next frame
        time.sleep(delay)

    # Final message
    print(c.success(f"\n Animation complete! ({total_positions} steps)"))


def print_grid_animated_with_direction(
    grid: "Grid",
    positions: list[Position],
    directions: list[Any] | None = None,
    delay: float = 0.1,
    separator: str = " ",
    max_rows: int | None = 50,
    max_cols: int | None = 100,
    show_coords: bool = True,
    trail_length: int = 0,
    show_step_count: bool = True,
    max_iterations: int = 200,
) -> None:
    """
    Animate movement with directional arrows (for guard patrol simulations).

    Args:
        grid: Grid to display
        positions: List of positions to animate through
        directions: Optional list of Direction objects (same length as positions)
        delay: Seconds between frames
        separator: String between cells
        max_rows: Maximum rows to display
        max_cols: Maximum cols to display
        show_coords: Show coordinates
        trail_length: Previous positions to show as trail
        show_step_count: Show current step
        max_iterations: Maximum frames to display (default: 200). If positions > max,
                        frames are skipped to stay within limit

    Example:
        # With direction tracking
        path = [(0,0), (1,0), (2,0)]
        dirs = [EAST, EAST, EAST]
        print_grid_animated_with_direction(grid, path, dirs, delay=0.05)
    """
    if not positions:
        print(c.dim("(no positions to animate)"))
        return

    # Direction to arrow mapping
    direction_arrows = {
        "north": "^",
        "south": "v",
        "east": ">",
        "west": "<",
        "northeast": "/",
        "southeast": "\\",
        "southwest": "\\",
        "northwest": "/",
    }

    rows_to_print = min(grid.height, max_rows) if max_rows else grid.height
    cols_to_print = min(grid.width, max_cols) if max_cols else grid.width

    # Calculate frame skipping if needed
    total_positions = len(positions)
    if total_positions > max_iterations:
        # Calculate step size to reduce frames to max_iterations
        step_size = total_positions / max_iterations
        frame_indices = [int(i * step_size) for i in range(max_iterations)]
        # Always include the last position
        if frame_indices[-1] != total_positions - 1:
            frame_indices[-1] = total_positions - 1
        print(
            c.dim(
                f"Showing {max_iterations}/{total_positions} positions "
                f"(skipping frames)"
            )
        )
    else:
        frame_indices = list(range(total_positions))

    # Calculate total lines for the animation area
    total_lines = rows_to_print
    if show_coords:
        total_lines += 1  # Header line
    if show_step_count:
        total_lines += 1  # Step counter line

    for frame_num, step in enumerate(frame_indices):
        current_pos = positions[step]

        # Move cursor up to overwrite previous frame (except first frame)
        if frame_num > 0:
            # ANSI escape: move cursor up N lines
            print(f"\033[{total_lines}A", end="")

        # Get current direction
        current_dir = None
        if directions and step < len(directions):
            current_dir = directions[step]

        # Calculate trail
        trail_positions = set()
        if trail_length > 0 and step > 0:
            trail_start = max(0, step - trail_length)
            trail_positions = set(positions[trail_start:step])

        # Print header
        if show_coords:
            header = "   " + separator.join(str(x % 10) for x in range(cols_to_print))
            print(c.dim(header))

        if show_step_count:
            dir_text = ""
            if current_dir:
                dir_name = (
                    current_dir.name
                    if hasattr(current_dir, "name")
                    else str(current_dir)
                )
                dir_text = f" - Facing: {dir_name}"
            print(
                c.dim(
                    f"Step {step + 1}/{total_positions} - "
                    f"Position: {current_pos}{dir_text}"
                )
            )

        # Print rows
        for y in range(rows_to_print):
            line_parts = []

            if show_coords:
                line_parts.append(c.dim(f"{y:2} "))

            for x in range(cols_to_print):
                pos = (x, y)
                cell = grid.at(x, y)

                if pos == current_pos:
                    # Show arrow for current direction
                    if current_dir:
                        dir_name = (
                            current_dir.name
                            if hasattr(current_dir, "name")
                            else str(current_dir).lower()
                        )
                        arrow = direction_arrows.get(dir_name, "@")
                        cell_str = c.cyan(c.bold(arrow))
                    else:
                        cell_str = c.cyan(c.bold("@"))
                elif pos in trail_positions:
                    # Trail - bright yellow
                    cell_str = c.yellow("+")
                else:
                    # Normal cell
                    cell_str = c.dim(str(cell))

                line_parts.append(cell_str)

            print(separator.join(line_parts))

        # Sleep
        time.sleep(delay)

    # Final message
    print(c.success(f"\n Animation complete! ({total_positions} steps)"))
