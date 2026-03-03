#!/usr/bin/env python3


import random
import sys
sys.setrecursionlimit(100000)


def get_opposite(direction: str) -> str:
    """Get the opposite direction.

    Args:
        direction: One of "top", "right", "bottom", "left".

    Returns:
        The opposite direction.
    """
    opposites = {
        "top": "bottom",
        "right": "left",
        "bottom": "top",
        "left": "right"
    }
    return opposites[direction]


def carve_passages(grid: list[list[dict]], row: int, col: int,
                   width: int, height: int, display_callback=None) -> None:
    """Recursively carve passages through the maze (DFS).

    Args:
        grid: The maze grid.
        row: Current row.
        col: Current column.
        width: Maze width.
        height: Maze height.
    """
    grid[row][col]["visited"] = True

    directions = ["top", "right", "bottom", "left"]
    random.shuffle(directions)

    for direction in directions:
        neighbor = get_neighbor(row, col, direction, width, height)
        if neighbor is not None:
            new_row, new_col = neighbor
            if not grid[new_row][new_col]["visited"]:
                grid[row][col][direction] = False
                opposite = get_opposite(direction)
                grid[new_row][new_col][opposite] = False

                if display_callback is not None:
                    display_callback(grid)

                carve_passages(grid, new_row, new_col, width, height, display_callback)


def generate_maze(grid: list[list[dict]], width: int, height: int,
                  entry: tuple[int, int], display_callback=None) -> None:
    """Generate maze using recursive backtracking.

    Args:
        grid: The maze grid.
        width: Maze width.
        height: Maze height.
        entry: Starting position (row, col).
    """
    entry_row, entry_col = entry
    if display_callback is not None:
        display_callback(grid)
    carve_passages(grid, entry_row, entry_col, width, height, display_callback)


def can_remove_wall(grid, row, col, direction, width, height):

    if row == 0 and direction == "top":
        return False
    if row == height - 1 and direction == "bottom":
        return False
    if col == 0 and direction == "left":
        return False
    if col == width - 1 and direction == "right":
        return False

    if not grid[row][col][direction]:
        return False

    neighbor = get_neighbor(row, col, direction, width, height)
    if neighbor is None:
        return False

    n_row, n_col = neighbor

    if grid[row][col].get("pattern", False):
        return False
    if grid[n_row][n_col].get("pattern", False):
        return False

    return True


def make_imperfect(grid, width, height, removal_percentage):

    total_cells = width + height

    # Safer wall removal amount
    walls_to_remove = max(1, int((total_cells) * removal_percentage))

    removed = 0
    attempts = 0
    max_attempts = walls_to_remove * 30

    directions = ["top", "right", "bottom", "left"]

    while removed < walls_to_remove and attempts < max_attempts:
        attempts += 1

        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)
        direction = random.choice(directions)

        if not grid[row][col][direction]:  # skip if already removed
            continue

        if not can_remove_wall(grid, row, col, direction, width, height):
            continue

        neighbor = get_neighbor(row, col, direction, width, height)

        if not neighbor:
            continue

        n_row, n_col = neighbor
        opposite = get_opposite(direction)

        grid[row][col][direction] = False
        grid[n_row][n_col][opposite] = False

        removed += 1

    return removed


def is_valid(row: int, col: int, width: int, height: int) -> bool:
    return 0 <= row < height and 0 <= col < width


def get_neighbor(row: int, col: int, direction: str,
                 width: int, height: int) -> tuple[int, int] | None:
    if direction == "top":
        new_row, new_col = row - 1, col
    elif direction == "right":
        new_row, new_col = row, col + 1
    elif direction == "bottom":
        new_row, new_col = row + 1, col
    elif direction == "left":
        new_row, new_col = row, col - 1
    else:
        return None
    if is_valid(new_row, new_col, width, height):
        return new_row, new_col
    return None


def create_grid(width: int, height: int) -> list[list[dict]]:
    grid = []

    for _ in range(height):
        row_cells = []
        for _ in range(width):
            cell = {
                "top": True,
                "right": True,
                "bottom": True,
                "left": True,
                "visited": False
            }
            row_cells.append(cell)
        grid.append(row_cells)
    return grid


def add_pattern_42(grid: list[list[dict]], width: int, height: int) -> None:
    """Add ASCII pattern '42' as blocked cells in the maze center.

    Args:
        grid: The maze grid.
        width: Maze width.
        height: Maze height.
    """
    pattern = [
        "#   ###",
        "#     #",
        "### ###",
        "  # #  ",
        "  # ###"
    ]

    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    if width < pattern_width or height < pattern_height:
        return

    start_row = (height - pattern_height) // 2
    start_col = (width - pattern_width) // 2

    for p_row, line in enumerate(pattern):
        for p_col, char in enumerate(line):
            if char == '#':
                grid_row = start_row + p_row
                grid_col = start_col + p_col

                if grid_row < height and grid_col < width:
                    grid[grid_row][grid_col]["top"] = True
                    grid[grid_row][grid_col]["right"] = True
                    grid[grid_row][grid_col]["bottom"] = True
                    grid[grid_row][grid_col]["left"] = True
                    grid[grid_row][grid_col]["visited"] = True
                    grid[grid_row][grid_col]["pattern"] = True
