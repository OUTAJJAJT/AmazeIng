from typing import Any


Position = tuple[int, int]
Cell = dict[str, Any]
Grid = list[list[Cell]]


def value_of_cell(cell: Cell) -> int:
    value = 0

    if cell["top"]:
        value += 1       # 0001
    if cell["right"]:
        value += 2       # 0010
    if cell["bottom"]:
        value += 4       # 0100
    if cell["left"]:
        value += 8       # 1000

    return value


def path_to_directions(path: list[Position]) -> str:
    """Convert a path (list of coordinates) to direction string.

    Args:
        path: List of (row, col) tuples representing the path.

    Returns:
        String of directions: N (north), S (south), E (east), W (west).
    """
    directions = ""

    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]

        if r2 == r1 - 1:
            directions += "N"
        elif r2 == r1 + 1:
            directions += "S"
        elif c2 == c1 + 1:
            directions += "E"
        elif c2 == c1 - 1:
            directions += "W"

    return directions


def save_maze(
    grid: Grid,
    entry: Position,
    exit_pos: Position,
    path: list[Position] | None,
    filename: str
) -> None:

    height = len(grid)
    width = len(grid[0])
    try:
        with open(filename, "w") as file:
            for row in range(height):
                line = ""
                for col in range(width):
                    value = value_of_cell(grid[row][col])
                    line += format(value, "X")
                file.write(line + "\n")

            # Convert from (row, col) to (x, y) format for output
            file.write(f"\n{entry[1]},{entry[0]}\n")
            file.write(f"{exit_pos[1]},{exit_pos[0]}\n")

            if path:
                directions = path_to_directions(path)
                file.write(directions + "\n")
    except FileNotFoundError:
        print("Error: we have a problem with OUTPUT_FILE")
