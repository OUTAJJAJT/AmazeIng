#!/usr/bin/env python3
from generator_maze import create_grid, generate_maze, add_pattern_42



def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def get_valid_neighbors(grid: list[list[dict]],
                        pos: tuple[int, int]) -> list[tuple[int, int]]:
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


def find_path(grid: list[list[dict]], start: tuple[int, int],
              goal: tuple[int, int]):

    queue = [start]
    visited = {start}
    parent = {start: None}

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


# def display_maze_with_path(grid: list[list[dict]], path:
# list[tuple[int, int]]
#                            | None, start: tuple[int, int],
#                            goal: tuple[int, int]) -> None:
#     """Display maze with the solution path highlighted.

#     Args:
#         grid: The maze grid.
#         path: List of coordinates representing the path from start to goal.
#         start: Starting position.
#         goal: Goal position.
#     """
#     height = len(grid)
#     width = len(grid[0])

#     wall_color = "\033[31m"      # Red
#     path_color = "\033[32m"      # Green
#     solution_color = "\033[36m"  # Cyan for solution path
#     start_color = "\033[35m"     # Magenta for start
#     goal_color = "\033[33m"      # Yellow for goal
#     pattern_color = "\033[93m"   # Bright yellow for pattern
#     reset = "\033[0m"

#     path_set = set(path) if path else set()

#     print(" " + wall_color + "_" * (width * 2 - 1) + reset)

#     for row in range(height):
#         line = wall_color + "|" + reset
#         for col in range(width):
#             cell = grid[row][col]
#             pos = (row, col)
#             is_pattern = cell.get("pattern", False)

#             if pos == start:
#                 cell_color = start_color
#             elif pos == goal:
#                 cell_color = goal_color
#             elif pos in path_set:
#                 cell_color = solution_color
#             elif is_pattern:
#                 cell_color = pattern_color
#             else:
#                 cell_color = path_color if not cell["bottom"] else wall_color

#             if cell["bottom"]:
#                 line += wall_color + "_" + reset
#             else:
#                 if pos in path_set or pos == start or pos == goal:
#                     line += cell_color + "●" + reset
#                 else:
#                     line += path_color + " " + reset

#             if cell["right"]:
#                 line += wall_color + "|" + reset
#             else:
#                 line += path_color + " " + reset

#         print(line)
