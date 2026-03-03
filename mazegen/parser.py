#!/usr/bin/env python3

"""Custom exceptions for the AmazeIng maze generator."""

from typing import Any, Dict, Tuple


class MazeError(Exception):
    """Base exception for maze-related errors."""
    pass


class ConfigError(MazeError):
    """Raised when configuration file cannot be read or parsed."""
    pass


class InvalidDimensionsError(MazeError):
    """Raised when maze dimensions are invalid."""
    pass


class InvalidCoordinatesError(MazeError):
    """Raised when entry or exit coordinates are invalid."""
    pass


class ConfigParsing:
    """Parser for maze configuration files."""

    def parse_line(self, line: str) -> tuple[str, str]:
        """Parse a key-value line, supporting = or : separators.

        Args:
            line: A configuration line.

        Returns:
            Tuple of (key, value) normalized to lowercase and stripped.

        Raises:
            ConfigError: If line format is invalid.
        """
        if "=" in line:
            key, value = line.split("=", 1)
        else:
            raise ConfigError("Invalid line format: expected '='")

        key = key.strip().lower()
        value = value.split("#")[0].strip()
        return key, value

    def parse(self, filename: str) -> Dict[str, Any]:
        """Parse configuration file and return maze parameters.

        Args:
            filename: Path to configuration file.

        Returns:
            Dictionary containing maze configuration with keys:
            width, height, entry, exit, output_file, algorithm.

        Raises:
            ConfigError: If file not found or cannot be read.
            InvalidDimensionsError: If dimensions are invalid.
            InvalidCoordinatesError: If coordinates are invalid.
        """
        width: int | None = None
        height: int | None = None
        entry: Tuple[int, int] | None = None
        exit: Tuple[int, int] | None = None
        output_file: str | None = None
        algorithm: str = "recursive_backtracking"
        perfect: bool = True
        seed: int | None = None
        imperfect_percentage: float = 0.5
        from terminal_display import TerminalDisplay
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    try:
                        key, value = self.parse_line(line)
                    except ConfigError:
                        raise

                    if key == "width":
                        try:
                            width = int(value)
                        except ValueError as e:
                            raise InvalidDimensionsError(
                                "Width must be an integer"
                            ) from e

                    elif key == "height":
                        try:
                            height = int(value)
                        except ValueError as e:
                            raise InvalidDimensionsError(
                                "Height must be an integer"
                            ) from e

                    elif key == "entry":
                        try:
                            x, y = value.split(",")
                            entry = (int(x.strip()), int(y.strip()))
                        except (ValueError, IndexError) as e:
                            raise InvalidCoordinatesError(
                                "Entry must be in format: x,y"
                            ) from e

                    elif key == "exit":
                        try:
                            x, y = value.split(",")
                            exit = (int(x.strip()), int(y.strip()))
                        except (ValueError, IndexError) as e:
                            raise InvalidCoordinatesError(
                                "Exit must be in format: x,y"
                            ) from e

                    elif key == "output_file":
                        output_file = value

                    elif key == "algorithm":
                        algorithm = value

                    elif key == "perfect":
                        perfect = value.lower() in ("true", "1", "yes")

                    elif key == "imperfect_percentage":
                        try:
                            imperfect_percentage = float(value)
                        except ValueError:
                            imperfect_percentage = 0.3

                    elif key == "seed":
                        try:
                            seed = int(value)
                        except ValueError:
                            if value == "none" or value == "None":
                                seed = None
                            else:
                                seed = value
        except FileNotFoundError:
            # raise ConfigError(f"Config file '{filename}' not found") from e
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Config file '{filename}' not found")
        from terminal_display import TerminalDisplay

        if width is None:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Width not found in config file")
        if height is None:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Height not found in config file")
        if entry is None:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Entry not found in config file")
        if exit is None:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Exit not found in config file")
        if output_file is None:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Output file not found in config file")
        if width <= 0:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Width must be positive, got {width}")
        if height <= 0:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Height must be positive, got \
{height}")

        max_dimension: int = 23
        if width > max_dimension:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Width too large (max {max_dimension}), \
got {width}")
        if height > max_dimension:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Height too large (max {max_dimension}), \
got {height}")
        entry_x, entry_y = entry
        exit_x, exit_y = exit

        if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Entry {entry} is out of bounds (0-\
{width - 1}, 0-{height - 1})")
        if exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error(f"Exit {exit} is out of bounds\
 (0-{width - 1}, 0-{height - 1})")

        if entry == exit:
            temp_display = TerminalDisplay([[{}]], (0, 0), (0, 0))
            temp_display.show_error("Entry and exit cannot be the same")

        return {
            "width": width,
            "height": height,
            "entry": entry,
            "exit": exit,
            "output_file": output_file,
            "algorithm": algorithm,
            "perfect": perfect,
            "seed": seed,
            "imperfect_percentage": imperfect_percentage
        }
