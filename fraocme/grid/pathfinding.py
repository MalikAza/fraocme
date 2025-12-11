"""Pathfinding algorithms for grids."""

import heapq
from collections import deque
from dataclasses import dataclass
from typing import Callable, TypeVar

from .core import Grid
from .directions import CARDINALS, Direction
from .types import Position

T = TypeVar("T")


@dataclass
class Path:
    """Represents a path through a grid."""

    positions: list[Position]
    cost: float

    @property
    def length(self) -> int:
        """Get path length (number of positions)."""
        return len(self.positions)


def manhattan_distance(p1: Position, p2: Position) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        p1: First position
        p2: Second position

    Returns:
        Manhattan distance (sum of absolute differences)
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def chebyshev_distance(p1: Position, p2: Position) -> int:
    """
    Calculate Chebyshev distance between two positions.

    Args:
        p1: First position
        p2: Second position

    Returns:
        Chebyshev distance (maximum absolute difference)
    """
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


def bfs(
    grid: Grid[T],
    start: Position,
    end: Position,
    is_walkable: Callable[[Position, T], bool],
    directions: list[Direction] | None = None,
) -> Path | None:
    """
    Breadth-first search pathfinding.

    Args:
        grid: Grid to search
        start: Starting position
        end: Goal position
        is_walkable: Function that returns True if a position can be walked on
        directions: List of directions to consider (default: CARDINALS)

    Returns:
        Path from start to end, or None if no path exists
    """
    if directions is None:
        directions = CARDINALS

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == end:
            return Path(positions=path, cost=len(path) - 1)

        # Check all directions
        for direction in directions:
            next_pos = grid.neighbor(current, direction)

            if next_pos and next_pos not in visited:
                if is_walkable(next_pos, grid.at(*next_pos)):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

    return None


def dijkstra(
    grid: Grid[T],
    start: Position,
    end: Position,
    cost_fn: Callable[[Position, T, Position, T], float],
    directions: list[Direction] | None = None,
) -> Path | None:
    """
    Dijkstra's algorithm for weighted pathfinding.

    Args:
        grid: Grid to search
        start: Starting position
        end: Goal position
        cost_fn: Function that returns cost to move from one position to another
        directions: List of directions to consider (default: CARDINALS)

    Returns:
        Lowest-cost path from start to end, or None if no path exists
    """
    if directions is None:
        directions = CARDINALS

    # Priority queue: (cost, position, path)
    queue = [(0, start, [start])]
    visited = set()
    costs = {start: 0}

    while queue:
        current_cost, current, path = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            return Path(positions=path, cost=current_cost)

        # Check all directions
        for direction in directions:
            next_pos = grid.neighbor(current, direction)

            if next_pos and next_pos not in visited:
                move_cost = cost_fn(
                    current, grid.at(*current), next_pos, grid.at(*next_pos)
                )
                new_cost = current_cost + move_cost

                if next_pos not in costs or new_cost < costs[next_pos]:
                    costs[next_pos] = new_cost
                    heapq.heappush(queue, (new_cost, next_pos, path + [next_pos]))

    return None


def a_star(
    grid: Grid[T],
    start: Position,
    end: Position,
    heuristic: Callable[[Position, Position], float],
    cost_fn: Callable[[Position, T, Position, T], float],
    directions: list[Direction] | None = None,
) -> Path | None:
    """
    A* algorithm for efficient weighted pathfinding.

    Args:
        grid: Grid to search
        start: Starting position
        end: Goal position
        heuristic: Function estimating cost from position to goal
        cost_fn: Function that returns actual cost to move between positions
        directions: List of directions to consider (default: CARDINALS)

    Returns:
        Optimal path from start to end, or None if no path exists
    """
    if directions is None:
        directions = CARDINALS

    # Priority queue: (f_score, g_score, position, path)
    # f_score = g_score + heuristic (estimated total cost)
    # g_score = actual cost from start
    h_start = heuristic(start, end)
    queue = [(h_start, 0, start, [start])]
    visited = set()
    g_scores = {start: 0}

    while queue:
        f_score, g_score, current, path = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            return Path(positions=path, cost=g_score)

        # Check all directions
        for direction in directions:
            next_pos = grid.neighbor(current, direction)

            if next_pos and next_pos not in visited:
                move_cost = cost_fn(
                    current, grid.at(*current), next_pos, grid.at(*next_pos)
                )
                tentative_g = g_score + move_cost

                if next_pos not in g_scores or tentative_g < g_scores[next_pos]:
                    g_scores[next_pos] = tentative_g
                    h = heuristic(next_pos, end)
                    f = tentative_g + h
                    heapq.heappush(queue, (f, tentative_g, next_pos, path + [next_pos]))

    return None
