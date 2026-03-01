import sys
import random
from parser import ConfigParsing
from terminal_display import TerminalDisplay
from generator_maze import create_grid, generate_maze, add_pattern_42
from pathfinding import find_path
from generator_maze import make_imperfect
from output_hex import save_maze


def get_key():
    key = input()
    return key.strip()


def grid_to_maze(grid):
    maze = []
    for row in grid:
        maze_row = []
        for cell in row:
            value = 0
            if cell["top"]:
                value += 1
            if cell["right"]:
                value += 2
            if cell["bottom"]:
                value += 4
            if cell["left"]:
                value += 8
            maze_row.append(value)
        maze.append(maze_row)
    return maze


def get_pattern_cells(grid):
    pattern = set()
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell.get("pattern", False):
                pattern.add((c, r))
    return pattern


def path_to_directions(path):
    if not path or len(path) < 2:
        return []
    directions = []
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]
        if r2 < r1:
            directions.append('N')
        elif r2 > r1:
            directions.append('S')
        elif c2 > c1:
            directions.append('E')
        elif c2 < c1:
            directions.append('W')

    print(f"DEBUG: path has {len(path)} cells, directions has \
{len(directions)} steps")
    return directions


def main():
    # Early error handling: use temp display for errors before main display
    # exists
    if len(sys.argv) != 2:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error("Usage: python3 a_maze_ing.py config.txt or\
make run")
        sys.exit(1)

    try:
        parser = ConfigParsing()
        config = parser.parse("config.txt")
    except Exception as e:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error(f"Config error: {e}")
        sys.exit(1)

    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit = config["exit"]
    perfect = config["perfect"]
    seed = config.get("seed", None)
    filename = config["output_file"]
    entry = (entry[0], entry[1])
    exit = (exit[0], exit[1])

    if seed is not None:
        random.seed(seed)

    grid = create_grid(width, height)
    if height >= 5 and width >= 7:
        add_pattern_42(grid, width, height)
    pattern_cells = get_pattern_cells(grid)
    if entry in pattern_cells or exit in pattern_cells:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error("Entry or exit is on a pattern 42 cell.\n\
            Please choose different coordinates.")
        sys.exit(1)

    generate_maze(grid, width, height, entry)

    if not perfect:
        make_imperfect(grid, width, height, 0.2)
    raw_path = find_path(grid, entry, exit)
    if not raw_path:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error("No path exists between entry and exit.\n\
            Try different coordinates or regenerate the maze.")
        sys.exit(1)
    directions = path_to_directions(raw_path)

    maze = grid_to_maze(grid)

    display = TerminalDisplay(maze, entry, exit, pattern_cells)
    display.set_path(directions)
    save_maze(grid, entry, exit, raw_path, filename)

    try:
        while True:
            display.display()
            key = get_key()

            if key == '1':
                display.toggle_path()
            elif key == '2':
                display.cycle_wall_color()
            elif key == '3':
                if display.show_path:
                    display.show_path = False
                grid = create_grid(width, height)
                if height >= 5 and width >= 7:
                    add_pattern_42(grid, width, height)
                pattern_cells = get_pattern_cells(grid)
                if entry in pattern_cells or exit in pattern_cells:
                    temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
                    temp_display.show_error("Entry or exit is on a pattern\
                        42 cell.\nPlease choose different coordinates.")
                    continue
                generate_maze(grid, width, height, entry)
                raw_path = find_path(grid, entry, exit)
                if not raw_path:
                    temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
                    temp_display.show_error("No path exists between entry \
                        and exit.\nTry different coordinates or regenerate\
                            the maze.")
                    continue
                directions = path_to_directions(raw_path)
                maze = grid_to_maze(grid)
                pattern_cells = get_pattern_cells(grid)
                display.maze = maze
                display.pattern_cells = pattern_cells
                display.set_path(directions)
            elif key == '4':
                print('\033[2J\033[H', end='')
                print("Bye!")
                break
            else:
                temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
                temp_display.show_error("Invalid choice! Enter 1, 2, 3 or \
                    4")
                continue
    except KeyboardInterrupt:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error("Program interrupted by user (Ctrl+C). \
Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
        temp_display.show_error("Program interrupted by user (Ctrl+C). \
            Exiting...")
        sys.exit(0)
