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
