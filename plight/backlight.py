from pathlib import Path


class Backlight:
    def __init__(self, name):
        self.name = name
        self.path = f"/sys/class/backlight/{name}"
        with open(Path(self.path, "max_brightness")) as f:
            self.max_brightness = int(f.read())

    def get_brightness(self):
        with open(Path(self.path, "brightness")) as f:
            return int(f.read())
