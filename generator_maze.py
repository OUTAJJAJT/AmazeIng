#!/usr/bin/env python3

import random
# from typing import Any
from parser import ConfigParsing


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
                   width: int, height: int) -> None:
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
                # Remove wall between current and neighbor
                grid[row][col][direction] = False
                opposite = get_opposite(direction)
                grid[new_row][new_col][opposite] = False

                # Recursively carve from neighbor
                carve_passages(grid, new_row, new_col, width, height)


def generate_maze(grid: list[list[dict]], width: int, height: int,
                  entry: tuple[int, int]) -> None:
    """Generate maze using recursive backtracking.

    Args:
        grid: The maze grid.
        width: Maze width.
        height: Maze height.
        entry: Starting position (row, col).
    """
    entry_row, entry_col = entry
    carve_passages(grid, entry_row, entry_col, width, height)


def display_maze(grid: list[list[dict]]) -> None:
    """Display the maze as ASCII art.

    Args:
        grid: The maze grid.
    """
    height = len(grid)
    width = len(grid[0])

    print(" " + "_" * (width * 2 - 1))

    for row in range(height):
        line = "|"
        for col in range(width):
            cell = grid[row][col]

            if cell["bottom"]:
                line += "_"
            else:
                line += " "

            if cell["right"]:
                line += "|"
            else:
                line += " "

        print(line)


def is_valid(row: int, col: int, width: int, height: int) -> bool:
    valid = 0
    if (0 <= row < height) and (0 <= col < width):
        valid = 1
    if valid == 0:
        return 0
    return 1


def get_neighbor(row: int, col: int, height: int, width: int, direction: str) \
                        -> tuple[int, int] | None:
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

    for row in range(height):
        row_cells = []
        for col in range(width):
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


def main() -> None:
    parser = ConfigParsing()
    config = parser.parse("config.txt")

    width = config["width"]
    height = config["height"]
    entry = config["entry"]  # Add this line

    grid = create_grid(width, height)
    generate_maze(grid, width, height, entry)
    display_maze(grid)


if __name__ == "__main__":
    main()
