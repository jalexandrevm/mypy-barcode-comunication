from configparser import ConfigParser
from pathlib import Path

DEFAULT_SECTION = "app"
DEFAULTS = {
    "app_name": "Printer Code Direct Sending",
    "default_printer": "",
    "log_file": "app.log",
    "encoding": "utf-8",
    "window_width": "900",
    "window_height": "600",
    "window_x": "100",
    "window_y": "100",
}


class AppConfig:
    def __init__(self, path: str = "app.ini"):
        self.path = Path(path)
        self.parser = ConfigParser()
        self._load()

    def _load(self):
        if not self.path.exists():
            self._create_default_file()

        self.parser.read(self.path, encoding="utf-8")
        if not self.parser.has_section(DEFAULT_SECTION):
            self.parser.add_section(DEFAULT_SECTION)

        for key, value in DEFAULTS.items():
            if not self.parser.has_option(DEFAULT_SECTION, key):
                self.parser.set(DEFAULT_SECTION, key, value)

        self.save()

    def _create_default_file(self):
        self.parser[DEFAULT_SECTION] = DEFAULTS
        self.save()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as config_file:
            self.parser.write(config_file)

    def get(self, key: str) -> str:
        return self.parser.get(DEFAULT_SECTION, key, fallback=DEFAULTS.get(key, ""))

    def set(self, key: str, value: str):
        self.parser.set(DEFAULT_SECTION, key, str(value))
        self.save()

    def get_int(self, key: str, fallback: int) -> int:
        try:
            return self.parser.getint(DEFAULT_SECTION, key)
        except (ValueError, TypeError):
            return fallback
