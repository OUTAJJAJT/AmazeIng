#!/usr/bin/env python3

from typing import Any

Position = tuple[int, int]
Cell = dict[str, Any]
Grid = list[list[Cell]]


def reconstruct_path(
    parent: dict[Position, Position | None],
    start: Position,
    goal: Position
) -> list[Position]:
    path: list[Position] = []
    current: Position | None = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def get_valid_neighbors(grid: Grid, pos: Position) -> list[Position]:
    """Get all neighbors accessible from current position (no walls between).

    Args:
        grid: The maze grid.
        pos: Current position (row, col).

    Returns:
        List of valid neighbor positions.
    """
    row, col = pos
    height = len(grid)
    width = len(grid[0])
    cell = grid[row][col]

    neighbors = []

    if not cell["top"] and row > 0:
        neighbors.append((row - 1, col))

    if not cell["right"] and col < width - 1:
        neighbors.append((row, col + 1))

    if not cell["bottom"] and row < height - 1:
        neighbors.append((row + 1, col))

    if not cell["left"] and col > 0:
        neighbors.append((row, col - 1))

    return neighbors


def find_path(grid: Grid, start: Position,
              goal: Position) -> list[Position] | None:

    queue = [start]
    visited = {start}
    parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    while queue:
        current = queue.pop(0)
        if current == goal:
            return reconstruct_path(parent, start, goal)

        for neighbor in get_valid_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return None
