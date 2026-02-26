import os
import time


class TerminalDisplay:

    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BLINK = '\033[5m'

    def __init__(self, maze, entry, exit, pattern_cells=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.height = len(maze)
        self.width = len(maze[0])
        self.show_path = False
        self.path_cells = set()
        self.path_order = []
        self.wall_color = self.CYAN
        self.pattern_cells = pattern_cells or set()

    # ==========================================================
    # RENDER
    # ==========================================================
    def render(self):
        output = []

        for y in range(self.height):

            # ---------- TOP ----------
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

            # ---------- MIDDLE ----------
            middle = ''
            for x in range(self.width):
                cell = self.maze[y][x]

                # Left wall
                if cell & 8:
                    middle += self.wall_color + '█' + self.RESET
                else:
                    middle += ' '

                # Inside cell (ALWAYS EXACTLY 4 characters)
                if (x, y) in self.pattern_cells:
                    middle += self.YELLOW + '████' + self.RESET

                elif (x, y) == self.entry:
                    middle += self.GREEN + ' E  ' + self.RESET

                elif (x, y) == self.exit:
                    middle += self.RED + ' X  ' + self.RESET

                elif self.show_path and (x, y) in self.path_cells:
                    middle += self.WHITE + ' ●  ' + self.RESET

                else:
                    middle += '    '

            # Right wall
            if self.maze[y][self.width - 1] & 2:
                middle += self.wall_color + '█' + self.RESET
            else:
                middle += ' '

            output.append(middle)

        # ---------- BOTTOM ----------
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

    # ==========================================================
    # DISPLAY
    # ==========================================================
    def display(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.render(), flush=True)
        print()
        print(self.BLINK + self.YELLOW + '𝓡𝓪𝓶𝓪𝓭𝓪𝓷 𝓜𝓾𝓫𝓪𝓻𝓪𝓴!' + self.RESET)
        print()
        print(self.wall_color + 'Controls:' + self.RESET)
        print('  1. show/hide path')
        print('  2. change wall color')
        print('  3. new maze')
        print('  4. quit')
        print()
        print('Enter your choice (1-4): ', end='', flush=True)

    # ==========================================================
    # TOGGLE PATH
    # ==========================================================
    def toggle_path(self):
        self.show_path = not self.show_path

    # ==========================================================
    # WALL COLOR CYCLE
    # ==========================================================
    def cycle_wall_color(self):
        colors = [self.CYAN, self.GREEN, self.YELLOW, self.RED, self.WHITE]

        try:
            idx = colors.index(self.wall_color)
            self.wall_color = colors[(idx + 1) % len(colors)]
        except ValueError:
            self.wall_color = self.CYAN

    # ==========================================================
    # SET PATH
    # ==========================================================
    def set_path(self, path):
        self.path_cells = set()
        self.path_order = []

        x, y = self.entry
        self.path_cells.add((x, y))
        self.path_order.append((x, y))

        moves = {
            'N': (0, -1),
            'E': (1,  0),
            'S': (0,  1),
            'W': (-1, 0)
        }

        for step in path:
            dx, dy = moves[step]
            x += dx
            y += dy

            self.path_cells.add((x, y))
            self.path_order.append((x, y))

    # ==========================================================
    # ANIMATE PATH (SMOOTH + SLOW)
    # ==========================================================
    def animate_path(self, speed='slow'):
        speeds = {
            'slow': 0.08,
            'medium': 0.05,
            'fast': 0.02
        }

        delay = speeds.get(speed, 0.08)

        if not self.path_order:
            return

        for i in range(1, len(self.path_order) + 1):
            self.path_cells = set(self.path_order[:i])
            self.show_path = True

            os.system('clear' if os.name == 'posix' else 'cls')
            print(self.render(), flush=True)

            time.sleep(delay)