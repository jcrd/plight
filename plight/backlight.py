from pathlib import Path

from plight.ddcutil import ddcutil


class Backlight:
    def __init__(self, name, setter):
        self.name = name
        self.setter = setter
        self.path = f"/sys/class/backlight/{name}"
        with open(Path(self.path, "max_brightness")) as f:
            self.max_brightness = int(f.read())

    def get_brightness(self):
        with open(Path(self.path, "brightness")) as f:
            return int(f.read())

    def set_brightness(self, v, curve=True):
        self.setter(self.name, self.max_brightness * v if curve else v)


class DDCBacklight(ddcutil):
    def __init__(self):
        super().__init__()

    def get_brightness(self):
        v, _ = self.get()
        return v

    def set_brightness(self, v, curve=True):
        self.set(round(self.max_brightness * v) if curve else v)
