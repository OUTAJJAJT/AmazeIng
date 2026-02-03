"""Configuration file parser for maze generator."""


class ConfigParser:
    """Parse configuration files for maze generation."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.config = {}

    def parse(self):
        try:
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise ValueError(f"Invalid line: {line}")

                    key, value = line.split('=', 1)
                    self.config[key.strip()] = value.strip()

            return self.config

        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.filepath}")

    def get_int(self, key: str) -> int:
        try:
            return int(self.config[key])
        except ValueError:
            raise ValueError(
                f"Invalid integer for {key}: {self.config[key]}"
            )
        except KeyError:
            raise KeyError(f"Missing key: {key}")

    def get_bool(self, key: str) -> bool:
        value = self.config[key].lower()
        if value in ('true', '1', 'yes'):
            return True
        elif value in ('false', '0', 'no'):
            return False
        else:
            raise ValueError(
                f"Invalid boolean for {key}: {self.config[key]}"
            )

    def get_coords(self, key: str):
        try:
            x, y = self.config[key].split(',')
            return (int(x.strip()), int(y.strip()))
        except Exception:
            raise ValueError(
                f"Invalid coordinates for {key}: {self.config[key]}"
            )

    def get_str(self, key: str, default: str = "") -> str:
        return self.config.get(key, default)
