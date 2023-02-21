import io
import logging
import subprocess

from PIL import Image


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

    def get_brightness_percentage(self):
        logging.debug("Device: getting brightness")
        ps = subprocess.run(
            f"ffmpeg -i {self.path} -vframes 1 -f image2pipe -".split(),
            capture_output=True,
        )
        im = Image.open(io.BytesIO(ps.stdout))
        im = im.convert("L")
        histogram = im.histogram()
        pixels = sum(histogram)
        br = scale = len(histogram)

        for i in range(0, scale):
            ratio = histogram[i] / pixels
            br += ratio * (-scale + i)

        return 1 if br == 255 else br / scale
