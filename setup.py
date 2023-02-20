from pathlib import Path

from setuptools import setup


def read(name):
    return open(Path(Path(__file__).parent, name)).read()


setup(
    name="plight",
    version="0.1.0",
    packages=["plight"],
    install_requires=["pygobject", "Pillow"],
    entry_points={
        "console_scripts": [
            "plight = plight.__main__:main",
        ],
    },
    description="Set laptop backlight based on webcam ambient light detection",
    # long_description=read("README.md"),
    # long_description_content_type="text/markdown",
    url="https://github.com/jcrd/plight",
    license="MIT",
    author="James Reed",
    author_email="james@twiddlingbits.net",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
