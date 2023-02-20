import logging
import os
import sys
from pathlib import Path

import tomllib
from gi.repository import GLib

from plight.backlight import Backlight
from plight.device import Device
from plight.logind import Logind

WAKEUP_DELAY = 1 * 1000

default_config = {
    "update_interval": 5,
    "brightness_curve": [0.001, 0.005, 0.01, 0.1, 0.2, 0.5, 0.6, 0.8, 0.9, 1.0],
    "device_name": "video0",
    "backlight_name": "intel_backlight",
}


class Updater:
    def __init__(self, config):
        self.source = None
        self.dev = Device(config["device_name"])
        self.bl = Backlight(config["backlight_name"])
        self.logind = Logind(self.on_start)
        self.brightness_curve = config["brightness_curve"]
        self.update_interval = config["update_interval"]

        self.on_start()

    def wakeup_update(self):
        self.dev.wakeup()
        self.update()

    def on_start(self):
        if self.source:
            GLib.source_remove(self.source)
        GLib.timeout_add(WAKEUP_DELAY, self.wakeup_update)

    def update(self):
        per = self.dev.get_brightness_percentage()
        idx = max(round(per * len(self.brightness_curve)) - 1, 0)
        cv = self.brightness_curve[idx]
        logging.debug(f"Updater: setting backlight {cv} (ambient {per})")
        self.logind.set_brightness(self.bl.name, self.bl.max_brightness * cv)

        self.source = GLib.timeout_add(self.update_interval * 60 * 1000, self.update)

    def run(self):
        logging.debug("Updater: running")
        GLib.MainLoop().run()


def process_config(default, data):
    if "curve" in data:
        for f in data["curve"]:
            if not (f > 0.0 and f <= 1.0):
                logging.warning(
                    f"config: curve value {f} is out of range; 0.0 < x <= 1.0"
                )
                sys.exit(2)

    return default | data


def main():
    if os.getenv("PLIGHT_DEBUG"):
        logging.basicConfig(level=logging.DEBUG)

    config = default_config
    p = Path(GLib.get_user_config_dir(), "plight", "plight.conf")

    if p.exists():
        with open(p) as f:
            config = process_config(config, tomllib.load(f))

    Updater(config).run()


if __name__ == "__main__":
    main()
