import sys
from config_parser import ConfigParser
from terminal_display import TerminalDisplay
from generator_maze import create_grid, generate_maze, add_pattern_42
from pathfinding import find_path


def get_key():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key


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

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    width  = parser.get_int('WIDTH')
    height = parser.get_int('HEIGHT')
    entry  = parser.get_coords('ENTRY')
    exit   = parser.get_coords('EXIT')

    # entry and exit are (x,y) but partner uses (row,col)
    entry_rc = (entry[1], entry[0])
    exit_rc  = (exit[1],  exit[0])

    grid = create_grid(width, height)
    if height >= 5 and width >= 7:
        add_pattern_42(grid, width, height)
    generate_maze(grid, width, height, entry_rc)

    raw_path = find_path(grid, entry_rc, exit_rc)
    directions = path_to_directions(raw_path)

    maze = grid_to_maze(grid)

    display = TerminalDisplay(maze, entry, exit)
    display.set_path(directions)

    while True:
        display.display()
        key = get_key()
        if key == 'q':
            print("Bye!")
            break
        elif key == 'p':
            display.toggle_path()
        elif key == 'c':
            display.cycle_wall_color()
        elif key == 'r':
            grid = create_grid(width, height)
            if height >= 5 and width >= 7:
                add_pattern_42(grid, width, height)
            generate_maze(grid, width, height, entry_rc)
            raw_path = find_path(grid, entry_rc, exit_rc)
            directions = path_to_directions(raw_path)
            maze = grid_to_maze(grid)
            display.maze = maze
            display.set_path(directions)


main()