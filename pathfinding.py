#!/usr/bin/env python3
# from generator_maze import get_neighbor


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
    cell = grid[row][col]
    neighbors = []

    if not cell["top"]:
        neighbors.append((row - 1, col))
    if not cell["right"]:
        neighbors.append((row, col + 1))
    if not cell["bottom"]:
        neighbors.append((row + 1, col))
    if not cell["left"]:
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
#                            list[tuple[int, int]], wall_color:
#                            str = "\033[31m", path_color:
#                            str = "\033[32m", solution_color:
#                            str = "\033[33m") -> None:
#     """Display maze with solution path highlighted."""
#     height = len(grid)
#     width = len(grid[0])
#     reset = "\033[0m"

#     path_set = set(path)

#     print(" " + wall_color + "_" * (width * 2 - 1) + reset)

#     for row in range(height):
#         line = wall_color + "|" + reset
#         for col in range(width):
#             cell = grid[row][col]

#             # Use * for solution path, space for regular
#             is_on_path = (row, col) in path_set

#             if cell["bottom"]:
#                 bottom_char = "_"
#             else:
#                 bottom_char = "*" if is_on_path else " "

#             if is_on_path and not cell["bottom"]:
#                 line += solution_color + bottom_char + reset
#             elif cell["bottom"]:
#                 line += wall_color + bottom_char + reset
#             else:
#                 line += path_color + bottom_char + reset

#             if cell["right"]:
#                 line += wall_color + "|" + reset
#             else:
#                 right_char = "*" if is_on_path else " "
#                 line += solution_color + right_char + reset if is_on_path \
#                     else path_color + right_char + reset

#         print(line)


if __name__ == "__main__":
    from generator_maze import create_grid, generate_maze
    from parser import ConfigParsing

    parser = ConfigParsing()
    config = parser.parse("config.txt")

    width = config["width"]
    height = config["height"]
    entry = config["entry"]

    goal = (height - 1, width - 1)

    grid = create_grid(width, height)
    generate_maze(grid, width, height, entry)

    path = find_path(grid, entry, goal)

    # if path:
    #     print(f"✓ Path found! Length: {len(path)} steps")
    #     print(f"  Start: {entry}")
    #     print(f"  Goal: {goal}")
    #     print("\nMaze with solution (yellow):")
    #     display_maze_with_path(grid, path)
    # else:
    #     print("✗ No path found!")
