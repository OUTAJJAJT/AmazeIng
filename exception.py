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
    
    @staticmethod
    def parse_line(line: str) -> tuple[str, str]:
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
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            raise ConfigError("Invalid line format: expected '=' or ':'")

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
        exit_coord: Tuple[int, int] | None = None
        output_file: str | None = None
        algorithm: str = "recursive_backtracking"

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
                            exit_coord = (int(x.strip()), int(y.strip()))
                        except (ValueError, IndexError) as e:
                            raise InvalidCoordinatesError(
                                "Exit must be in format: x,y"
                            ) from e

                    elif key == "output_file":
                        output_file = value

                    elif key == "algorithm":
                        algorithm = value

        except FileNotFoundError as e:
            raise ConfigError(f"Config file '{filename}' not found") from e

        # Validate all required fields are present
        if width is None:
            raise InvalidDimensionsError("Width not found in config file")
        if height is None:
            raise InvalidDimensionsError("Height not found in config file")
        if entry is None:
            raise InvalidCoordinatesError("Entry not found in config file")
        if exit_coord is None:
            raise InvalidCoordinatesError("Exit not found in config file")
        if output_file is None:
            raise InvalidDimensionsError("Output file not found in config file"
                                         )
        # Validate dimensions are positive
        if width <= 0:
            raise InvalidDimensionsError(f"Width must be positive, got {width}"
                                         )
        if height <= 0:
            raise InvalidDimensionsError(f"Height must be positive, got\
{height}")

        max_dimension: int = 1000
        if width > max_dimension:
            raise InvalidDimensionsError(
                f"Width too large (max {max_dimension}), got {width}"
            )
        if height > max_dimension:
            raise InvalidDimensionsError(
                f"Height too large (max {max_dimension}), got {height}"
            )
        entry_x, entry_y = entry
        exit_x, exit_y = exit_coord

        if entry_x < 0 or entry_x >= width or entry_y < 0 or entry_y >= height:
            raise InvalidCoordinatesError(f"Entry {entry} is out of bounds (0-\
{width - 1}, 0-{height - 1})")
        if exit_x < 0 or exit_x >= width or exit_y < 0 or exit_y >= height:
            raise InvalidCoordinatesError(f"Exit {exit_coord} is out of bounds\
 (0-{width - 1}, 0-{height - 1})")

        if entry == exit_coord:
            raise InvalidCoordinatesError("Entry and exit cannot be the same")

        return {
            "width": width,
            "height": height,
            "entry": entry,
            "exit": exit_coord,
            "output_file": output_file,
            "algorithm": algorithm,
        }


if __name__ == "__main__":
    parser: ConfigParsing = ConfigParsing()

    try:
        config: Dict[str, Any] = parser.parse("config.txt")
        print("Configuration loaded successfully!")
        print(f"Width: {config['width']}")
        print(f"Height: {config['height']}")
        print(f"Entry: {config['entry']}")
        print(f"Exit: {config['exit']}")
        print(f"Output file: {config['output_file']}")
        print(f"Algorithm: {config['algorithm']}")
    except MazeError as e:
        print(f"Error: {e}")
