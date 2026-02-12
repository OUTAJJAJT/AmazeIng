import sys
from config_parser import ConfigParser
from terminal_display import TerminalDisplay


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

    # temporary fake maze until partner is done
    maze = make_fake_maze(width, height)

    display = TerminalDisplay(maze, entry, exit)

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


def make_fake_maze(width, height):
    import random
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = 0xF
            if x > 0:
                cell &= ~8
            if x < width - 1:
                cell &= ~2
            if y > 0:
                cell &= ~1
            if y < height - 1:
                cell &= ~4
            row.append(cell)
        maze.append(row)
    return maze


main()