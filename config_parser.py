
class ConfigParser:

    RESET  = '\033[0m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = {}

    def parse(self):
        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    continue

                key, value = line.split('=', 1)
                value = value.split('#')[0]
                key = key.strip()
                value = value.strip()

                if key:
                    self.config[key] = value

        return self.config

    def get_int(self, key):
        try:
            return int(self.config[key])
        except KeyError:
            raise ValueError(f"Missing key in config: {key}")
        except ValueError:
            raise ValueError(f"Invalid integer for {key}: {self.config[key]}")

    def get_bool(self, key):
        try:
            value = self.config[key].lower()
        except KeyError:
            raise ValueError(f"Missing key in config: {key}")
        if value in ('true', '1', 'yes'):
            return True
        elif value in ('false', '0', 'no'):
            return False
        else:
            raise ValueError(f"Invalid boolean for {key}: {self.config[key]}")

    def get_coords(self, key):
        try:
            x, y = self.config[key].split(',')
            return (int(x.strip()), int(y.strip()))
        except KeyError:
            raise ValueError(f"Missing key in config: {key}")
        except Exception:
            raise ValueError(f"Invalid coordinates for {key}: {self.config[key]}")

    def get_str(self, key):
        return self.config.get(key, "")