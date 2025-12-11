

# =============================================================================
# CORE: Lines and Outlines
# =============================================================================


def line_points(p1: tuple[int, int], p2: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Return all points along a straight horizontal or vertical line (inclusive).

    Args:
        p1: First point (x, y)
        p2: Second point (x, y)

    Returns:
        Set of all points on the line

    Raises:
        ValueError: If the line is not horizontal or vertical

    Example:
        >>> line_points((1, 1), (1, 4))
        {(1, 1), (1, 2), (1, 3), (1, 4)}
    """
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:  # Vertical line
        return {(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)}
    elif y1 == y2:  # Horizontal line
        return {(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)}
    else:
        raise ValueError(f"Only horizontal or vertical lines allowed, got {p1} -> {p2}")


def build_outline_from_vertices(
    vertices: list[tuple[int, int]], closed: bool = True
) -> set[tuple[int, int]]:
    """
    Build an outline by connecting consecutive vertices with straight lines.

    Args:
        vertices: List of vertices [(x1, y1), (x2, y2), ...]
        closed: If True, connect last vertex back to first

    Returns:
        Set of all points on the outline

    Example:
        >>> build_outline_from_vertices([(0, 0), (0, 2), (2, 2), (2, 0)])
        {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)}
    """
    outline = set()
    n = len(vertices)

    for i in range(n - 1):
        outline.update(line_points(vertices[i], vertices[i + 1]))

    if closed and n > 1:
        outline.update(line_points(vertices[-1], vertices[0]))

    return outline


# =============================================================================
# CORE: Filling Algorithms
# =============================================================================


def fill_outline_floodfill(outline: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Fill the interior of a closed outline using flood fill from outside.

    Identifies all points NOT reachable from outside the bounding box.

    Args:
        outline: Set of points forming the closed outline

    Returns:
        Set of all points inside the outline (including the outline itself)

    Example:
        >>> outline = build_outline_from_vertices([(1, 1), (1, 3), (3, 3), (3, 1)])
        >>> sorted(fill_outline_floodfill(outline))
        [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    """
    if not outline:
        return set()

    xs = [x for x, y in outline]
    ys = [y for x, y in outline]
    min_x, max_x = min(xs) - 1, max(xs) + 1
    min_y, max_y = min(ys) - 1, max(ys) + 1

    # Flood fill from outside
    outside = set()
    queue = [(min_x, min_y)]

    while queue:
        x, y = queue.pop()

        if (x, y) in outside or (x, y) in outline:
            continue
        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue

        outside.add((x, y))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in outside and (nx, ny) not in outline:
                queue.append((nx, ny))

    # Interior = everything in bounding box that's not outside
    return {
        (x, y)
        for x in range(min_x + 1, max_x)
        for y in range(min_y + 1, max_y)
        if (x, y) not in outside
    }


# =============================================================================
# CONVENIENCE: Polygons (uses core functions)
# =============================================================================


def polygon_interior_points(vertices: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Return all points inside a polygon defined by vertices.

    The polygon must have only horizontal/vertical edges (grid-aligned).

    Args:
        vertices: List of polygon vertices in order

    Returns:
        Set of all points inside the polygon (including boundary)

    Example:
        >>> len(polygon_interior_points([(1, 1), (1, 4), (4, 4), (4, 1)]))
        16
    """
    outline = build_outline_from_vertices(vertices, closed=True)
    return fill_outline_floodfill(outline)


# =============================================================================
# RECTANGLES: Kept separate for PERFORMANCE
#
# - rectangle_area: O(1) vs O(width * height) for generating all points
# - rectangle_points: Still O(w*h), but simpler than building outline + flood fill
# - For 90,000 x 90,000 grids, this matters!
# =============================================================================


def rectangle_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """
    Calculate rectangle area from two opposite corners. O(1) operation.

    Args:
        p1: First corner (x1, y1)
        p2: Opposite corner (x2, y2)

    Returns:
        Area of the rectangle (number of grid cells)

    Example:
        >>> rectangle_area((1, 1), (3, 2))
        6
    """
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def rectangle_points(p1: tuple[int, int], p2: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Return all points inside a rectangle. Use rectangle_area() if you only need the count.

    Args:
        p1: First corner (x1, y1)
        p2: Opposite corner (x2, y2)

    Returns:
        Set of all points inside the rectangle (inclusive)

    Example:
        >>> sorted(rectangle_points((1, 1), (2, 2)))
        [(1, 1), (1, 2), (2, 1), (2, 2)]
    """
    x1, y1 = p1
    x2, y2 = p2
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    return {(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)}


def rectangle_contains(
    p1: tuple[int, int], p2: tuple[int, int], point: tuple[int, int]
) -> bool:
    """
    Check if a point is inside a rectangle. O(1) operation.

    Args:
        p1: First corner of rectangle
        p2: Opposite corner of rectangle
        point: Point to check

    Returns:
        True if point is inside rectangle (inclusive)

    Example:
        >>> rectangle_contains((1, 1), (3, 3), (2, 2))
        True
        >>> rectangle_contains((1, 1), (3, 3), (5, 5))
        False
    """
    x1, y1 = p1
    x2, y2 = p2
    px, py = point
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


# =============================================================================
# SEARCH: Finding largest shapes
# =============================================================================


def largest_valid_rectangle(
    corners: list[tuple[int, int]], allowed: set[tuple[int, int]]
) -> tuple[int, tuple[tuple[int, int], tuple[int, int]] | None]:
    """
    Find the largest rectangle using any two points as opposite corners,
    where all rectangle points are within the allowed set.

    Args:
        corners: List of potential corner points
        allowed: Set of allowed points for the rectangle interior

    Returns:
        Tuple of (max_area, (corner1, corner2)) or (0, None) if no valid rectangle

    Example:
        >>> corners = [(1, 1), (3, 3)]
        >>> allowed = {(x, y) for x in range(1, 4) for y in range(1, 4)}
        >>> largest_valid_rectangle(corners, allowed)
        (9, ((1, 1), (3, 3)))
    """
    max_area = 0
    best_corners = None

    n = len(corners)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = corners[i], corners[j]
            rect = rectangle_points(p1, p2)

            if rect.issubset(allowed):
                area = len(rect)
                if area > max_area:
                    max_area = area
                    best_corners = (p1, p2)

    return max_area, best_corners


def largest_valid_polygon(
    polygons: list[list[tuple[int, int]]], allowed: set[tuple[int, int]] | None = None
) -> tuple[int, list[tuple[int, int]] | None]:
    """
    Find the largest polygon (by interior area) from a list of polygons.

    Args:
        polygons: List of polygons, each as list of vertices
        allowed: Optional set of allowed points (if None, all polygons are valid)

    Returns:
        Tuple of (max_area, winning_polygon_vertices) or (0, None)

    Example:
        >>> polygons = [
        ...     [(1, 1), (1, 4), (4, 4), (4, 1)],  # 16 points
        ...     [(2, 2), (2, 3), (3, 3), (3, 2)]   # 4 points
        ... ]
        >>> largest_valid_polygon(polygons)
        (16, [(1, 1), (1, 4), (4, 4), (4, 1)])
    """
    max_area = 0
    best_polygon = None

    for vertices in polygons:
        interior = polygon_interior_points(vertices)

        if allowed is None or interior.issubset(allowed):
            area = len(interior)
            if area > max_area:
                max_area = area
                best_polygon = vertices

    return max_area, best_polygon
