from parser import ConfigParsing
import os
import time
import shutil


class TerminalDisplay:

    def show_error(self, message):
        box_width = 60
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.RED + "╔" + "═" * box_width + "╗" + self.RESET)
        print(self.RED + f"║{'ERROR':^{box_width}}║" + self.RESET)
        print(self.RED + "╠" + "═" * box_width + "╣" + self.RESET)
        for line in message.splitlines():
            # Print the message in chunks if it's longer than box_width
            for i in range(0, len(line), box_width):
                print(self.RED + f"║{line[i:i+box_width]:^{box_width}}║" +
                      self.RESET)
        print(self.RED + "╚" + "═" * box_width + "╝" + self.RESET)
        print()

    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    def __init__(self, maze, entry, exit, pattern_cells=None):
        self.maze = maze
        self.entry = (entry[1], entry[0])
        self.exit = (exit[1], exit[0])
        self.height = len(maze)
        self.width = len(maze[0])
        self.show_path = False
        self.path_cells = set()
        self.wall_color = self.CYAN
        self.pattern_cells = pattern_cells or set()

    def render(self):
        output = []

        for y in range(self.height):

            top = ''
            for x in range(self.width):
                cell = self.maze[y][x]
                if (x, y) in self.pattern_cells:
                    top += self.YELLOW + '█████' + self.RESET
                elif cell & 1:
                    top += self.wall_color + '█████' + self.RESET
                else:
                    top += self.wall_color + '█' + self.RESET + '    '
            top += self.wall_color + '█' + self.RESET
            output.append(top)

            middle = ''
            for x in range(self.width):
                cell = self.maze[y][x]
                if (x, y) in self.pattern_cells:
                    middle += self.YELLOW + '█████' + self.RESET
                else:
                    if cell & 8:
                        middle += self.wall_color + '█' + self.RESET
                    else:
                        middle += ' '
                    if (x, y) == self.entry:
                        middle += self.GREEN + ' E  ' + self.RESET
                    elif (x, y) == self.exit:
                        middle += self.RED + ' X  ' + self.RESET
                    elif self.show_path and (x, y) in self.path_cells:
                        middle += self.YELLOW + ' ●  ' + self.RESET
                    else:
                        middle += '    '
            if self.maze[y][self.width - 1] & 2:
                middle += self.wall_color + '█' + self.RESET
            else:
                middle += ' '
            output.append(middle)

        bottom = ''
        for x in range(self.width):
            cell = self.maze[self.height - 1][x]
            if (x, self.height - 1) in self.pattern_cells:
                bottom += self.YELLOW + '█████' + self.RESET
            elif cell & 4:
                bottom += self.wall_color + '█████' + self.RESET
            else:
                bottom += self.wall_color + '█' + self.RESET + '    '
        bottom += self.wall_color + '█' + self.RESET
        output.append(bottom)

        return '\n'.join(output)

    def display(self):
        parser = ConfigParsing()
        config = parser.parse("config.txt")

        width = config["width"]
        height = config["height"]

        # Required terminal size
        required_width = self.width * 5 + 1
        required_height = self.height * 2 + 1 + 8

        def clear():
            os.system('cls' if os.name == 'nt' else 'clear')

        def get_term_size():
            try:
                size = shutil.get_terminal_size()
                return size.columns, size.lines
            except OSError:
                return None, None

        # 🔥 Try auto-resize (best effort)
        print(f"\033[8;{required_height};{required_width}t", end="")

        # 🔒 Wait until terminal is big enough (LIVE, no Enter)
        while True:
            cols, lines = get_term_size()

            if cols is None:
                break  # can't detect → continue anyway

            if cols >= required_width and lines >= required_height:
                break

            clear()

            # ✨ nicer warning box
            print(self.RED + "╔" + "═" * 40 + "╗" + self.RESET)
            print(self.RED + "║        TERMINAL TOO SMALL              ║" +
                  self.RESET)
            print(self.RED + "╠" + "═" * 40 + "╣" + self.RESET)
            print(f" Required : {required_width} x {required_height}")
            print(f" Current  : {cols} x {lines}")
            print()
            print(" ➜ Please enlarge your terminal window...")
            print(self.RED + "╚" + "═" * 40 + "╝" + self.RESET)

            time.sleep(0.25)  # smooth refresh

        # ✅ Final render
        clear()
        print(self.render(), flush=True)

        print()
        print(self.YELLOW + '𝓡𝓪𝓶𝓪𝓭𝓪𝓷 𝓜𝓾𝓫𝓪𝓻𝓪𝓴!' + self.RESET)
        print()
        print(self.wall_color + 'Controls:' + self.RESET)
        print('  1. show/hide path')
        print('  2. change wall color')
        print('  3. new maze')
        print('  4. quit')

        if height < 5 or width < 7:
            print("\nyour maze is small to show pattern 42\n")

        print('Enter your choice (1-4): ', end='', flush=True)

    def toggle_path(self):
        self.show_path = not self.show_path

    def cycle_wall_color(self):
        colors = [self.CYAN, self.GREEN, self.YELLOW, self.RED, self.WHITE]
        try:
            idx = colors.index(self.wall_color)
            self.wall_color = colors[(idx + 1) % len(colors)]
        except ValueError:
            self.wall_color = self.CYAN

    def set_path(self, path):
        self.path_cells = set()
        x, y = self.entry
        self.path_cells.add((x, y))
        moves = {
            'N': (0, -1),   # North: y decreases
            'E': (1,  0),   # East: x increases
            'S': (0,  1),   # South: y increases
            'W': (-1, 0)    # West: x decreases
        }
        for step in path:
            dx, dy = moves[step]
            x, y = x + dx, y + dy
            self.path_cells.add((x, y))
