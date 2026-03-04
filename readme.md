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
python3 main.py
```

With a config file:

```bash
python3 main.py --config config.json
```

With command-line overrides:

```bash
python3 main.py --width 20 --height 15 --algorithm dfs --solver bfs --delay 0.005
```

### Controls

| Key | Action |
|-----|--------|
| `Enter` | Start / replay |
| `q` | Quit |
| `s` | Skip generation animation, jump to completed maze |

---

## Config File Structure

The program reads a JSON config file. Below is the complete schema with all supported fields and their defaults.

```json
{
  "maze": {
    "width": 20,
    "height": 15,
    "entry": [0, 0],
    "exit": [14, 19]
  },
  "generation": {
    "algorithm": "dfs",
    "seed": null,
    "delay": 0.005
  },
  "solver": {
    "algorithm": "bfs",
    "delay": 0.05,
    "show_path": true,
    "path_gradient": true
  },
  "display": {
    "wall_char": "\u2588",
    "path_char": "\u00b7",
    "entry_char": "E",
    "exit_char": "X",
    "color_walls": true,
    "color_path": true,
    "blink_message": true,
    "message": "Ramadan Mubarak \ud83c\udf19"
  }
}
```

### Field Reference

| Field | Type | Default | Description |
|---|---|---|---|
| `maze.width` | int | `20` | Number of columns in the maze |
| `maze.height` | int | `15` | Number of rows in the maze |
| `maze.entry` | [row, col] | `[0, 0]` | Entry cell coordinates (partner format) |
| `maze.exit` | [row, col] | `[height-1, width-1]` | Exit cell coordinates (partner format) |
| `generation.algorithm` | string | `"dfs"` | Generation algorithm: `"dfs"` or `"wilson"` |
| `generation.seed` | int or null | `null` | RNG seed for reproducible mazes |
| `generation.delay` | float | `0.005` | Seconds between generation frames |
| `solver.algorithm` | string | `"bfs"` | Solver: `"bfs"` or `"astar"` |
| `solver.delay` | float | `0.05` | Seconds between path reveal frames |
| `solver.show_path` | bool | `true` | Whether to animate the solution |
| `solver.path_gradient` | bool | `true` | Color path green→yellow→red |
| `display.wall_char` | string | `"█"` | Character used to draw walls |
| `display.path_char` | string | `"·"` | Character used to mark path |
| `display.entry_char` | string | `"E"` | Character for entry cell |
| `display.exit_char` | string | `"X"` | Character for exit cell |
| `display.color_walls` | bool | `true` | ANSI-color the walls |
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

Example:

```
cell = 6  →  0110 binary
             ||||
             |||└─ North: 0 (no wall)
             ||└── East:  1 (wall exists)
             |└─── South: 1 (wall exists)
             └──── West:  0 (no wall)
```

---

## Why This Algorithm

We chose Recursive DFS over other options for several reasons:

**Simplicity:** The implementation is concise and easy to reason about. The recursive structure maps directly to the conceptual model — explore, backtrack, repeat.

**Visual appeal:** DFS tends to produce mazes with long, winding corridors rather than many short dead-ends. This looks dramatic during animation because you can watch the algorithm dive deep before backtracking.

**Animation friendliness:** Because the algorithm modifies one wall at a time, the callback-based animation hook is trivially easy to attach — every wall removal becomes one frame.

**Correctness guarantees:** DFS always produces a perfect maze (connected, acyclic, spanning). No post-processing needed.

**Alternatives considered:**

| Algorithm | Rejected Because |
|---|---|
| Prim's | Produces mazes with many short dead-ends — less visually interesting |
| Kruskal's | Requires a union-find data structure; more complex for similar output |
| Wilson's | Produces unbiased mazes but is slow to start and harder to animate meaningfully |
| Aldous-Broder | Unbiased but can take extremely long on larger grids |

Wilson's algorithm is implemented as an optional advanced feature (see [Advanced Features](#advanced-features)) for users who prefer statistically unbiased mazes.

---

## Reusable Components

The following modules and functions are designed to be decoupled from the rest of the project and reused independently.

### `converter.py`

A standalone module with no project-specific dependencies. Import it into any project that needs to translate between the two data formats.

```python
from converter import grid_to_maze, swap_coords, path_to_directions
```

| Function | Input | Output | Description |
|---|---|---|---|
| `grid_to_maze(grid)` | `list[list[dict]]` | `list[list[int]]` | Converts dict-based wall grid to bitwise integer grid |
| `swap_coords(entry)` | `(row, col)` | `(x, y)` | Swaps coordinate convention between systems |
| `path_to_directions(path)` | `list[(row, col)]` | `list[str]` | Converts position list to `['N','S','E','W']` directions |

### `renderer.py`

The display engine is fully decoupled from the generation logic. It accepts any valid integer grid and renders it.

```python
from renderer import render_maze, render_path, clear_screen
```

- `render_maze(maze, entry, exit, path=None)` — renders a full maze to stdout
- `render_path(maze, path, step)` — renders the maze with path revealed up to `step`
- `clear_screen()` — ANSI escape to clear the terminal without flicker

### `solver.py`

The BFS solver is algorithm-agnostic. It accepts any integer-encoded maze and returns the shortest path.

```python
from solver import bfs_solve, astar_solve
```

Both functions accept `(maze, start, end)` and return a `list[(row, col)]`.

### How to Reuse in Another Project

```python
# Minimal example: generate, solve, and print a path
from generator import generate_maze
from solver import bfs_solve
from renderer import render_maze

maze = generate_maze(width=10, height=10)
path = bfs_solve(maze, start=(0,0), end=(9,9))
render_maze(maze, entry=(0,0), exit=(9,9), path=path)
```

---

## Advanced Features

### Multiple Generation Algorithms

Pass `--algorithm wilson` or set `"algorithm": "wilson"` in the config to use **Wilson's algorithm** instead of DFS. Wilson's produces statistically unbiased mazes (every spanning tree is equally likely), at the cost of a slower and less visually dramatic generation animation.

### Multiple Solver Algorithms

Pass `--solver astar` to use **A\* pathfinding** instead of BFS. A\* uses Manhattan distance as a heuristic and finds the same shortest path as BFS on uniform-cost grids, but explores fewer cells — visible in the animation as a more directional search pattern.

### Color Gradient Path

When `path_gradient` is enabled, the solution path is colored using a green → yellow → red gradient based on each cell's position in the path:

```
t = cell_index / (path_length - 1)

R = lerp(74, 255, t)
G = lerp(222, 0, t)
B = 0
```

This gives an immediate visual sense of progress from entry to exit without needing numbers.

### Blinking End Message

After the path is fully drawn, a message is displayed using ANSI blink (`\033[5m`) and reset (`\033[0m`). The message text, color, and whether to blink are all configurable via `config.json`.

### Seeded Generation

Set `"seed": 42` (or any integer) in the config for fully reproducible mazes. Two runs with the same seed, dimensions, and algorithm will always produce the identical maze.

---

## Team & Project Management

### Team Members and Roles

| Member | Role |
|---|---|
| **Student A** | Maze engine (generator + DFS algorithm), config file parsing, seeded RNG, Wilson's algorithm (advanced) |
| **Student B** | Display module (ASCII renderer, ANSI colors), BFS solver, animation loop, converter functions, A\* solver (advanced) |

Both members collaborated on: the data format contract between modules, integration testing, the README, and code review.

### Anticipated Planning

We began by defining the data contract between our two modules before writing any code — agreeing on the integer bitfield format and the callback interface for animation. This was the most important decision of the project and saved us significant rework later.

**Week 1:** Individual module development in parallel. Student A built the generator; Student B built the renderer and solver using a hand-crafted test maze as a placeholder.

**Week 2:** Integration. We connected the two modules via the converter functions and debugged coordinate mismatches and wall-direction inconsistencies.

**Week 3:** Polish — animation tuning, config file, advanced features, documentation.

### How the Plan Evolved

- The converter layer was initially expected to be trivial (a few lines). It grew into its own module as we discovered more edge cases: coordinate flipping, wall direction naming conventions (our "North" was the partner's "top"), and path format differences.
- We underestimated the time needed to make the animation feel smooth. Early versions had flickering due to naive `clear_screen` usage. We fixed this by redrawing only changed lines using cursor positioning.
- Wilson's algorithm was added late as a bonus after DFS was solid. It required more animation design effort because its "random walk" phase is visually confusing without additional highlighting.

### What Worked Well

- **Defining the interface first.** Working on separate modules with an agreed contract meant we rarely blocked each other.
- **The bitfield encoding.** Storing all four walls in one integer made the renderer, solver, and converter all simpler and faster.
- **Callback-based animation.** Hooking into the generator via a callback rather than modifying it directly kept the two modules clean and separated.

### What Could Be Improved

- **Testing.** We relied heavily on visual inspection. Unit tests for the converter functions and solver correctness would have caught bugs faster.
- **The coordinate swap.** We were bitten by (row, col) vs (x, y) multiple times. In retrospect, a shared `Point` namedtuple used everywhere would have made this impossible to confuse.
- **Config validation.** The config parser currently silently uses defaults for unknown or malformed fields. Proper schema validation with clear error messages would improve usability.

### Tools Used

| Tool | Purpose |
|---|---|
| **Python 3.11** | Primary language |
| **Git + GitHub** | Version control and collaboration |
| **VS Code** | Primary editor |
| **Claude (Anthropic)** | See AI usage below (Resources section) |
| **draw.io** | Sketching the data flow and module architecture |
| **42 peer evaluation system** | Code review and feedback |

---

## Resources

### Documentation & References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Overview of all major approaches including DFS, Prim's, Wilson's, and Aldous-Broder.
- [Buckblog: Maze algorithms](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) — The definitive blog series on maze generation, with animated examples of each algorithm.
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code) — Full reference for terminal color, cursor movement, and effects including blink.
- [Python `time.sleep` documentation](https://docs.python.org/3/library/time.html#time.sleep) — Used for controlling animation frame rate.
- [BFS pathfinding — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search) — Reference for the solving algorithm.
- [A\* search algorithm — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm) — Reference for the advanced solver.
- [Bitwise operations in Python — Real Python](https://realpython.com/python-bitwise-operators/) — Tutorial on the `&`, `|`, `~`, and `<<` operators used in the cell encoding.

### AI Usage

We used **Claude (claude.ai)** during this project in the following specific ways:

**Conceptual explanation:** We used Claude to get detailed explanations of the three animation techniques (incremental generation, gradient path drawing, ANSI blink) before implementing them. This helped us plan the architecture rather than discovering it by trial and error.

**Debugging coordinate bugs:** When the maze was rendering mirrored along one axis, we described the symptom to Claude and it identified the (row, col) vs (x, y) swap as the likely cause within one exchange.

**Code review:** We pasted individual functions (particularly `grid_to_maze` and `path_to_directions`) and asked Claude to identify edge cases or off-by-one errors. Several bugs in the direction converter were found this way.

**README structure:** We asked Claude for feedback on the README outline to ensure nothing required by the 42 specification was missing.

**What we did NOT use AI for:** The actual algorithm implementations (DFS, BFS, A\*), the bitfield encoding design, the module architecture decisions, and all integration work were done by us. AI was used as a reference and reviewer, not as a code generator for core logic.