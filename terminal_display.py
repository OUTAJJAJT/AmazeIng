class TerminalDisplay:

    RESET  = '\033[0m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    CYAN   = '\033[36m'
    WHITE  = '\033[37m'

    def __init__(self, maze, entry, exit):
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.height = len(maze)
        self.width = len(maze[0])
        self.show_path = False
        self.path_cells = set()
        self.wall_color = self.CYAN

    def render(self):
        output = []

        for y in range(self.height):

            top = ''
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell & 1:
                    top += self.wall_color + '+---' + self.RESET
                else:
                    top += self.wall_color + '+   ' + self.RESET
            top += self.wall_color + '+' + self.RESET
            output.append(top)

            middle = ''
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell & 8:
                    middle += self.wall_color + '|' + self.RESET
                else:
                    middle += ' '
                if (x, y) == self.entry:
                    middle += self.GREEN + ' E ' + self.RESET
                elif (x, y) == self.exit:
                    middle += self.RED + ' X ' + self.RESET
                elif self.show_path and (x, y) in self.path_cells:
                    middle += self.YELLOW + ' . ' + self.RESET
                else:
                    middle += '   '
            if self.maze[y][self.width - 1] & 2:
                middle += self.wall_color + '|' + self.RESET
            else:
                middle += ' '
            output.append(middle)

        bottom = ''
        for x in range(self.width):
            cell = self.maze[self.height - 1][x]
            if cell & 4:
                bottom += self.wall_color + '+---' + self.RESET
            else:
                bottom += self.wall_color + '+   ' + self.RESET
        bottom += self.wall_color + '+' + self.RESET
        output.append(bottom)

        return '\n'.join(output)

    def display(self):
        print('\033[2J\033[H', end='')
        print(self.render())
        print()
        print(self.wall_color + 'Controls:' + self.RESET)
        print('  p = show/hide path')
        print('  c = change wall color')
        print('  r = new maze')
        print('  q = quit')

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
            'N': (0, -1),
            'E': (1,  0),
            'S': (0,  1),
            'W': (-1, 0)
        }
        for step in path:
            dx, dy = moves[step]
            x, y = x + dx, y + dy
            self.path_cells.add((x, y))