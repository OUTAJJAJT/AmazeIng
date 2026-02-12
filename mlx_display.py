from mlx import Mlx

class MlxDisplay:
    CELL_SIZE = 30
    WALL_COLOR = 0x00FFFF
    
    def __init__(self, maze, entry, exit):
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.height = len(maze)
        self.width = len(maze[0])
        
        win_width = self.width * self.CELL_SIZE + 100
        win_height = self.height * self.CELL_SIZE + 100
        
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            win_width,
            win_height,
            "Maze"
        )
    def draw_rectangle(self, x, y, width, height, color):
        for dx in range(width):
            for dy in range(height):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    x + dx,
                    y + dy,
                    color
                )
    def render(self):
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]
                
                px = 50 + x * self.CELL_SIZE
                py = 50 + y * self.CELL_SIZE
                
                if cell & 1:
                    self.draw_rectangle(px, py, self.CELL_SIZE, 3, self.WALL_COLOR)
                
                if cell & 2:
                    self.draw_rectangle(px + self.CELL_SIZE - 3, py, 3, self.CELL_SIZE, self.WALL_COLOR)
                
                if cell & 4:
                    self.draw_rectangle(px, py + self.CELL_SIZE - 3, self.CELL_SIZE, 3, self.WALL_COLOR)
                
                if cell & 8:
                    self.draw_rectangle(px, py, 3, self.CELL_SIZE, self.WALL_COLOR)
                
                if (x, y) == self.entry:
                    self.draw_rectangle(px + 10, py + 10, 10, 10, 0x00FF00)
                
                if (x, y) == self.exit:
                    self.draw_rectangle(px + 10, py + 10, 10, 10, 0xFF0000)