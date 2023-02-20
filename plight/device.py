import io
import logging
import subprocess

from PIL import Image, ImageStat


def clamp(v, bot, top):
    return max(min(v, top), bot)


class Device:
    max_brightness = 255

    def __init__(self, name):
        self.path = f"/dev/{name}"

    def wakeup(self, frames=10):
        logging.debug("Device: waking up")
        subprocess.run(
            f"ffmpeg -i {self.path} -vframes {frames} -f image2pipe -".split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def get_brightness(self):
        logging.debug("Device: getting brightness")
        ps = subprocess.run(
            f"ffmpeg -i {self.path} -vframes 1 -f image2pipe -".split(),
            capture_output=True,
        )
        im = Image.open(io.BytesIO(ps.stdout))
        im = im.convert("L")
        return ImageStat.Stat(im).rms[0]

    def get_brightness_percentage(self):
        return clamp(self.get_brightness() / Device.max_brightness, 0.0, 1.0)
