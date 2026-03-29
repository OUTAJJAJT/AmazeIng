*This project has been created as part of the 42 curriculum by hiouzddo, so-ait-l.*

---

# 🌀 A-Maze-ing

> A terminal-based maze generator and solver built in Python, featuring real-time animated generation, pathfinding visualization, and a collaborative two-module architecture.

---

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
- [Config File Structure](#config-file-structure)
- [Maze Generation Algorithm](#maze-generation-algorithm)
- [Why This Algorithm](#why-this-algorithm)
- [Reusable Components](#reusable-components)
- [Advanced Features](#advanced-features)
- [Team & Project Management](#team--project-management)
- [Resources](#resources)

---

## Description

**A-Maze-ing** is a terminal application that procedurally generates perfect mazes and solves them in real time. The project is split into two collaborating modules:

- **Module A (Maze Engine):** Generates mazes using a recursive DFS algorithm and exposes a callback-based API for live animation.
- **Module B (Display & Solver):** Consumes the engine's output, renders mazes using ASCII block characters and ANSI escape codes, solves them via BFS pathfinding, and animates the result step-by-step in the terminal.

The two modules use different internal data representations and coordinate systems, bridged by a set of converter functions. The result is a visually rich, animated experience entirely within a standard terminal — no GUI required.

### Goals

- Understand and implement classic maze generation and pathfinding algorithms.
- Practice collaborative development across incompatible data formats.
- Build a real-time animation loop using only the terminal.
- Produce clean, modular, reusable Python code.

---

## Instructions

### Requirements

- Python **3.10+**
- A terminal that supports ANSI escape codes (bash, zsh, most Linux/macOS terminals)
- No external Python packages required (standard library only)

### Installation

```bash
git clone https://github.com/your-org/a-maze-ing.git
cd a-maze-ing
```

### Running the Program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Controls

Once the maze is generated, you can:

| Key | Action |
|-----|--------|
| `1` | Show/hide path solution |
| `2` | Cycle wall color |
| `3` | Generate new maze |
| `4` | Quit program |
## Config File Structure

The program reads a **text-based** config file in `KEY=VALUE` format. Below is the complete structure with all supported fields.

**Example `config.txt`:**

```
WIDTH=23
HEIGHT=23
ENTRY=0,9
EXIT=15,19
OUTPUT_FILE=maze.txt
PERFECT=TRUE
IMPERFECT_PERCENTAGE=0.3
SEED=42
ALGORITHM=recursive_backtracking
```

### Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | int | Yes | Number of columns (2-23) |
| `HEIGHT` | int | Yes | Number of rows (2-23) |
| `ENTRY` | x,y | Yes | Entry cell coordinates (0-indexed) |
| `EXIT` | x,y | Yes | Exit cell coordinates (0-indexed) |
| `OUTPUT_FILE` | string | Yes | Output filename for maze data |
| `PERFECT` | boolean | Yes | `TRUE` for perfect maze (one path), `FALSE` for multiple paths |
| `IMPERFECT_PERCENTAGE` | float | No | When `PERFECT=FALSE`, percentage of walls to remove (0.0-1.0, default 0.3) |
| `SEED` | int/float/str | No | Random seed for reproducible mazes |
| `ALGORITHM` | string | No | `recursive_backtracking` (default) |
| `display.color_path` | bool | `true` | ANSI-color the solution path |
| `display.blink_message` | bool | `true` | Show blinking message at end |
| `display.message` | string | `"Ramadan Mubarak 🌙"` | Text to display after solving |

---

## Maze Generation Algorithm

We used **Recursive Depth-First Search (Recursive Backtracker)**.

### How It Works

1. Start from a random cell. Mark it as visited.
2. Randomly pick an unvisited neighbor.
3. Remove the wall between the current cell and the chosen neighbor.
4. Move to the neighbor and repeat.
5. If no unvisited neighbors exist, backtrack to the previous cell.
6. Repeat until all cells have been visited.

The algorithm naturally produces a **perfect maze** — one with exactly one path between any two cells, no loops, and no isolated regions.

### Internal Representation

Each cell is stored as a single integer where each bit encodes one wall:

```
Bit 0 (value 1) → North wall
Bit 1 (value 2) → East wall
Bit 2 (value 4) → South wall
Bit 3 (value 8) → West wall
```

A cell value of `15` (binary `1111`) means all four walls are intact. Carving a passage between two cells clears the relevant bits on both sides.

## Maze Generation Algorithm

We used **Recursive Depth-First Search (Recursive Backtracker)**.

### How It Works

1. Start at the entry point. Mark it as visited.
2. Randomly pick an unvisited neighbor.
3. Remove the wall between the current and neighbor cell.
4. Move to the neighbor and repeat from step 2.
5. If no unvisited neighbors exist, backtrack to the previous cell.
6. Repeat until all cells are visited.

## Why This Algorithm

**Recursive DFS** was chosen for:

- **Simplicity:** Easy to implement recursively; each recursive call represents moving to a neighbor.
- **Visual appeal:** Creates long, winding corridors that look impressive during animation.
- **Animation-friendly:** The callback mechanism captures each wall removal as a discrete frame.
- **Correctness:** Always produces a perfect maze (connected, acyclic, spanning tree).

### Perfect vs Imperfect Mazes

- **Perfect maze** (`PERFECT=TRUE`): Exactly one path between any two points. Generated by the core DFS algorithm.
- **Imperfect maze** (`PERFECT=FALSE`): Multiple paths exist. Created by randomly removing additional walls after DFS completes. The `IMPERFECT_PERCENTAGE` controls how many walls are removed (0.0 = none, 1.0 = all possible).
Bit 2 (value 4) → Bottom wall
Bit 3 (value 8) → Left wall
```

Example: cell value `15` (binary `1111`) = all walls intact
## Reusable Components

The following modules and functions are designed to be decoupled from the rest of the project and reused independently.

### `converter.py`

A standalone module with no project-specific dependencies. Import it into any project that needs to translate between the two data formats.
## Reusable Components

The following modules are designed to be independent and reusable:

### `mazegen/generator_maze.py`

Maze generation engine with callback-based animation.

```python
from mazegen.generator_maze import create_grid, generate_maze, make_imperfect

grid = create_grid(width, height)
generate_maze(grid, width, height, entry, animation_callback)
if not perfect:
    make_imperfect(grid, width, height, removal_percentage)
```

**Reusable functions:**
- `create_grid(width, height)` — Creates empty maze grid
- `generate_maze(grid, width, height, entry, callback)` — Generates perfect maze with optional live callback
- `make_imperfect(grid, width, height, percentage)` — Adds multiple paths by removing walls

### `mazegen/pathfinding.py`

BFS pathfinding algorithm (shortest path solver).

```python
from mazegen.pathfinding import find_path

path = find_path(grid, start, goal)  # Returns list of (row, col) coordinates
```

**Why reusable:** Works with any grid representation as long as wall structure is respected.

### `terminal_display.py`

Terminal rendering engine with ANSI colors and animations.

```python
from terminal_display import TerminalDisplay

display = TerminalDisplay(maze, entry, exit)
display.render()                    # Draw static maze
display.set_path(directions)        # Set solution path
display.animate_path(speed)         # Animate path reveal
display.animate_generation(grid)    # Show generation live
```

### Using mazegen as a Reusable Library

The `mazegen` package is designed for easy installation and reuse in other projects.

#### Installation

```bash
# Install from source (after pip install build setuptools wheel)
pip install ./mazegen-1.0.0-py3-none-any.whl

# Or build and install from source
python -m build
pip install dist/mazegen-*.whl
```

#### Quick Start: Class-Based API

The recommended way to use `mazegen` is via the `MazeGenerator` class:

```python
from mazegen import MazeGenerator

# Create a generator for a 20×20 perfect maze
gen = MazeGenerator(
    width=20,
    height=20,
    entry=(0, 0),
    exit=(19, 19),
    perfect=True,
    seed=42
)

# Generate the maze (no output yet)
gen.generate()

# Solve it using BFS
path = gen.solve()
print(f"Solution path: {path}")  # [(0,0), (0,1), ..., (19,19)]

# Access the internal grid structure
grid = gen.get_grid()
print(f"Grid dimensions: {len(grid)} rows × {len(grid[0])} cols")

# Convert to integer format for saving/display
int_maze = gen.to_grid_format()
# Each cell is now 0-15: bits represent [North, East, South, West] walls
```

#### Custom Parameters

```python
# Imperfect maze with custom seed
gen = MazeGenerator(
    width=15,
    height=15,
    entry=(5, 5),           # Custom start position
    exit=(10, 10),          # Custom end position
    perfect=False,          # Allow multiple paths
    imperfect_percentage=0.5,  # Remove 50% extra walls
    seed=12345
)

gen.generate()
path = gen.solve()
```

#### Animation Support

Pass a callback to `generate()` to animate each step:

```python
def on_wall_carved(grid):
    """Called after each wall removal."""
    # Render grid, update UI, etc.
    pass

gen = MazeGenerator(20, 20)
gen.generate(animation_callback=on_wall_carved)
```

#### Accessing the Grid Structure

The internal grid is a `list[list[dict]]` where each cell dict has:

```python
cell = {
    "top": True,        # Wall exists on north side
    "right": False,     # Wall removed on east side
    "bottom": True,     # Wall exists on south side
    "left": False,      # Wall removed on west side
    "visited": True,    # Cell was visited during generation
    "pattern": False    # Optional: part of the '42' pattern
}
```

This allows flexible access and modification after generation:

```python
grid = gen.get_grid()
for row in grid:
    for cell in row:
        if cell.get("pattern"):
            # Mark pattern cells differently
            pass
```

#### API Reference

**`MazeGenerator` class:**

- `__init__(width, height, entry=(0,0), exit=None, perfect=True, seed=None, imperfect_percentage=0.3)`
  - Creates a new generator (does not generate yet).
  
- `generate(animation_callback=None)`
  - Generates the maze using recursive DFS.
  - Optional callback receives grid after each wall removal.
  
- `solve()`
  - Finds shortest path from entry to exit using BFS.
  - Returns `list[(row, col)]` or `None` if no path exists.
  
- `get_grid()`
  - Returns the internal grid structure (`list[list[dict]]`).
  - Raises `RuntimeError` if `generate()` hasn't been called.
  
- `get_solution()`
  - Returns the last solved path, or `None` if not solved yet.
  
- `to_grid_format()`
  - Converts internal grid to integer format (bits for walls).
  - Returns `list[list[int]]` where each cell is 0–15.

#### Example: Generate, Solve, and Export

```python
from mazegen import MazeGenerator
import json

# Generate
gen = MazeGenerator(width=20, height=20, seed=99)
gen.generate()

# Solve
path = gen.solve()

# Export to JSON
export = {
    "grid": gen.to_grid_format(),
    "entry": gen.entry,
    "exit": gen.exit,
    "solution": path
}

with open("my_maze.json", "w") as f:
    json.dump(export, f)
```

#### Backward Compatibility: Functional API

For advanced use cases, the original functional API is still available:

```python
from mazegen.generator_maze import create_grid, generate_maze, make_imperfect
from mazegen.pathfinding import find_path

grid = create_grid(20, 20)
generate_maze(grid, 20, 20, entry=(0, 0))
make_imperfect(grid, 20, 20, 0.3)
path = find_path(grid, (0, 0), (19, 19))
```

---

## Advanced Features

### Pattern '42' 

For mazes 5×7 or larger, a ASCII pattern "42" is automatically drawn in the center as a visual Easter egg.

### Imperfect Mazes

Set `PERFECT=FALSE` and adjust `IMPERFECT_PERCENTAGE` (0.0–1.0) to generate mazes with multiple solutions:

```
PERFECT=FALSE
IMPERFECT_PERCENTAGE=0.5  # Remove 50% more walls after DFS
```

Higher percentage = more alternative paths.

### Wall Color Cycling

During execution, press `2` to cycle through wall colors:
- Cyan (default)
- Green
- Yellow
- Red
- White
After the path is fully drawn, a message is displayed using ANSI blink (`\033[5m`) and reset (`\033[0m`). The message text, color, and whether to blink are all configurable via `config.json`.

### Seeded Generation

Set `"seed": 42` (or any integer) in the config for fully reproducible mazes. Two runs with the same seed, dimensions, and algorithm will always produce the identical maze.

---

## Team & Project Management
## Team & Project Management

### Team Members and Roles

This is a **solo project** by **hiouzddo** and **so-ait-l**.

- **Maze generation & algorithm design**
- **Display, rendering, and animation**
- **Pathfinding (BFS) implementation**
- **Config parsing and validation**
- **Integration testing**

### Development Process

1. **Planning:** Defined the maze format (cell dictionaries vs. integers), coordinate system (row, col), and callback interface for animation.
2. **Core implementation:** Built generator, pathfinder, and display modules independently.
3. **Integration:** Connected modules via converter functions to bridge data format differences.
4. **Polish:** Added features like imperfect mazes, wall color cycling, and pattern '42'.
5. **Testing:** Manual testing in the terminal; type checking with mypy.

### Key Decisions

- **Dictionary-based cells during generation:** Clearer semantics (`cell["top"]` vs bitfield). Converted to integers for display.
- **Callback-based animation:** Allows generation to remain pure; display layer plugs in via callback.
- **BFS for pathfinding:** Guarantees shortest path; simple to implement and understand.
- **Config file format:** Text-based `KEY=VALUE` for human readability and ease of parsing.

### What Worked Well

- **Separating generation, solving, and display:** Each can be tested and reused independently.
- **Callback mechanism:** Generation algorithm doesn't need to know about display details.
- **Type hints:** mypy caught several coordinate swap bugs early.

### What Could Be Improved

- **More comprehensive unit tests:** Currently relies on visual inspection and manual testing.
- **Better error messages for invalid config:** Specific line numbers and hints for fixing errors.
- **Support for non-square mazes:** Some display calculations assume similar aspect ratios.
- **Keyboard response during animation:** Currently not responsive until animation completes.
---

### Tools & Technologies Used

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Primary language |
| **mypy** | Static type checking |
| **flake8** | Code linting |
| **Git** | Version control |
| **VS Code** | Editor |
| **Claude AI** | Debugging, algorithm explanations, code review |
| **Make** | Build automation (Makefile) |g/wiki/A*_search_algorithm) — Reference for the advanced solver.
- [Bitwise operations in Python — Real Python](https://realpython.com/python-bitwise-operators/) — Tutorial on the `&`, `|`, `~`, and `<<` operators used in the cell encoding.

## Resources

### Algorithm References

- [Recursive Backtracker — Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maze Generation — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

### Technical References

- [ANSI Escape Codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code) — Terminal colors, cursor control, effects
- [Python Bitwise Operators — Real Python](https://realpython.com/python-bitwise-operators/)
- [Python Type Hints — Python Docs](https://docs.python.org/3/library/typing.html)

### AI Usage

**Claude AI** (claude.ai) was used for:

1. **Algorithm explanations:** Understanding BFS guarantees shortest path, how DFS naturally produces spanning trees.
2. **Debugging:** Identifying coordinate swap bugs (row,col vs x,y) by describing visual symptoms.
3. **Code review:** Checking for type safety issues, off-by-one errors in path reconstruction.
4. **Type checking guidance:** Understanding mypy errors and how to structure type hints properly.

**What was NOT generated by AI:**
- Algorithm implementations (generator, pathfinder, display rendering)
- Core architecture decisions
- Config parsing and validation logic
- All integration and debugging work