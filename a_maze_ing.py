import sys
import random
# from config_parser import ConfigParser
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
    return directions


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    parser = ConfigParsing()
    config = parser.parse("config.txt")

    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit = config["exit"]
    perfect = config["perfect"]
    seed = config["seed"]
    filename = config["output_file"]

    print(seed)
    if seed is not None:
        random.seed(seed)
    grid = create_grid(width, height)
    if height >= 5 and width >= 7:
        add_pattern_42(grid, width, height)
    generate_maze(grid, width, height, entry)

    if not perfect:
        make_imperfect(grid, width, height, 0.2)
    raw_path = find_path(grid, entry, exit)
    directions = path_to_directions(raw_path)

    maze = grid_to_maze(grid)

    pattern_cells = get_pattern_cells(grid)
    display = TerminalDisplay(maze, entry, exit, pattern_cells)
    display.set_path(directions)
    save_maze(grid, entry, exit, raw_path, filename)

    while True:
        display.display()
        key = get_key()

        if key == '4':
            print('\033[2J\033[H', end='')
            print("Bye!")
            break
        elif key == '1':
            display.toggle_path()
        elif key == '2':
            display.cycle_wall_color()
        elif key == '3':
            grid = create_grid(width, height)
            if height >= 5 and width >= 7:
                add_pattern_42(grid, width, height)
            generate_maze(grid, width, height, entry)
            raw_path = find_path(grid, entry, exit)
            directions = path_to_directions(raw_path)
            maze = grid_to_maze(grid)
            pattern_cells = get_pattern_cells(grid)
            display.maze = maze
            display.pattern_cells = pattern_cells
            display.set_path(directions)
        else:
            print("Invalid choice! Enter 1, 2, 3 or 4")


main()
