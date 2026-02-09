#!/usr/bin/env python3

import random
import sys
# from typing import Any
from parser import ConfigParsing
from pathfinding import find_path

# Increase recursion limit for large mazes
sys.setrecursionlimit(100000)

# Color schemes: (wall_color, path_color, solution_color)
# COLOR_SCHEMES = {
#     0: ("\033[31m", "\033[32m", "\033[33m"),  # Red/Green/Yellow
#     1: ("\033[34m", "\033[33m", "\033[35m"),  # Blue/Yellow/Magenta
#     2: ("\033[35m", "\033[36m", "\033[31m"),  # Magenta/Cyan/Red
#     3: ("\033[37m", "\033[30m", "\033[36m")   # White/Black/Cyan
# }


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


def display_maze(grid: list[list[dict]], wall_color: str = "\033[31m",
                 path_color: str = "\033[32m") -> None:
    """Display the maze as ASCII art with ANSI colors.

    Args:
        grid: The maze grid.
        wall_color: ANSI color code for walls (default red).
        path_color: ANSI color code for paths (default green).
    """
    height = len(grid)
    width = len(grid[0])

    reset = "\033[0m"

    print(" " + wall_color + "_" * (width * 2 - 1) + reset)

    for row in range(height):
        line = wall_color + "|" + reset
        for col in range(width):
            cell = grid[row][col]

            if cell["bottom"]:
                line += wall_color + "_" + reset
            else:
                line += path_color + " " + reset

            if cell["right"]:
                line += wall_color + "|" + reset
            else:
                line += path_color + " " + reset

        print(line)


def is_valid(row: int, col: int, width: int, height: int) -> bool:
    # valid = 0
    # if (0 <= row < height) and (0 <= col < width):
    #     valid = 1
    # if valid == 0:
    #     return 0
    # return 1
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
    entry = config["entry"]

    grid = create_grid(width, height)
    generate_maze(grid, width, height, entry)

#     # Interactive color selection
#     current_color_scheme = 0
#     wall_color, path_color, solution_color = COLOR_SCHEMES[
#         current_color_scheme
#     ]

    # Find solution path
    exit_row, exit_col = config["exit"]
    find_path(grid, entry, (exit_row, exit_col))
    # solution_path = find_path(grid, entry, (exit_row, exit_col))

#     print("\n=== Maze Color Schemes ===")
#     print("0: Red walls, Green paths")
#     print("1: Blue walls, Yellow paths")
#     print("2: Magenta walls, Cyan paths")
#     print("3: White walls, Black paths")
#     print("\nCommands:")
#     print("  'c' - Next color scheme")
#     print("  'p' - Previous color scheme")
#     print("  's' - Show solution path")
#     print("  'q' - Quit\n")

#     show_solution = False

#     while True:
#         if show_solution and solution_path:
#             display_maze_with_path(
#                 grid,
#                 solution_path,
#                 wall_color,
#                 path_color,
#                 solution_color,
#             )
#         else:
#             display_maze(grid, wall_color, path_color)

#         user_input = input("\nCommand (c=next, p=previous, s=solution, \
# q=quit): ").strip().lower()

#         if user_input == 'c':
#             current_color_scheme = (current_color_scheme + 1) % \
#                 len(COLOR_SCHEMES)
#             wall_color, path_color, solution_color = COLOR_SCHEMES[
#                 current_color_scheme
#             ]
#             print(f"Switched to scheme {current_color_scheme}")
#         elif user_input == 'p':
#             current_color_scheme = (current_color_scheme - 1) % \
#                 len(COLOR_SCHEMES)
#             wall_color, path_color, solution_color = COLOR_SCHEMES[
#                 current_color_scheme
#             ]
#             print(f"Switched to scheme {current_color_scheme}")
#         elif user_input == 's':
#             if solution_path:
#                 show_solution = not show_solution
#                 status = "ON" if show_solution else "OFF"
#                 print(f"Solution display: {status}")
#             else:
#                 print("No solution found!")
#         elif user_input == 'q':
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid command. Use 'c', 'p', 's', or 'q'")


if __name__ == "__main__":
    main()
