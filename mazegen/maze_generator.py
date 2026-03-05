#!/usr/bin/env python3

from typing import Any, Callable
import random
from mazegen.generator_maze import (
    create_grid,
    generate_maze,
    make_imperfect,
)
from mazegen.pathfinding import find_path
from terminal_display import TerminalDisplay


Cell = dict[str, Any]
Grid = list[list[Cell]]
Position = tuple[int, int]


class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        entry: Position = (0, 0),
        exit: Position | None = None,
        perfect: bool = True,
        seed: int | None = None,
        imperfect_percentage: float = 0.3,
    ) -> None:

        if width < 2 or height < 2:
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error("Width and height must be at least 2.")

        if not (0 <= entry[0] < height and 0 <= entry[1] < width):
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error(f"Entry {entry} out of bounds \
[0-{height-1}, 0-{width-1}].")

        default_exit = (height - 1, width - 1)
        if exit is None:
            exit = default_exit
        if not (0 <= exit[0] < height and 0 <= exit[1] < width):
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error(f"Exit {exit} out of bounds [0-{height-1},\
 0-{width-1}].")

        if entry == exit:
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error("Entry and exit cannot be the same \
position.")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.imperfect_percentage = imperfect_percentage
        self.grid: Grid = []
        self.solution: list[Position] | None = None

        if seed is not None:
            random.seed(seed)

    def generate(
        self,
        animation_callback: Callable[[Grid], None] | None = None,
    ) -> None:

        self.grid = create_grid(self.width, self.height)

        entry_row, entry_col = self.entry
        generate_maze(
            self.grid,
            self.width,
            self.height,
            self.entry,
            animation_callback,
        )

        if not self.perfect:
            make_imperfect(
                self.grid,
                self.width,
                self.height,
                self.imperfect_percentage,
            )

    def solve(self) -> list[Position] | None:
        if not self.grid:
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error("Call generate() before solve().")

        self.solution = find_path(self.grid, self.entry, self.exit)
        return self.solution

    def get_grid(self) -> Grid:

        if not self.grid:
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error("Call generate() before accessing \
the grid.")
        return self.grid

    def get_solution(self) -> list[Position] | None:
        return self.solution

    def to_grid_format(self) -> list[list[int]]:

        if not self.grid:
            temp_display = TerminalDisplay([[0]], (0, 0), (0, 0))
            temp_display.show_error("Call generate() before converting to \
integer format.")

        result: list[list[int]] = []
        for row in self.grid:
            result_row: list[int] = []
            for cell in row:
                value = 0
                if cell.get("top", True):
                    value += 1
                if cell.get("right", True):
                    value += 2
                if cell.get("bottom", True):
                    value += 4
                if cell.get("left", True):
                    value += 8
                result_row.append(value)
            result.append(result_row)
        return result


__all__ = ["MazeGenerator"]
