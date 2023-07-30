# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="DmxOscServer",
    version="1.0.0",
    description="A Python Lib to create a DMX compatible OSC server with handlers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Miniontoby/DmxOscServer",
    author="Miniontoby",
    keywords="dmx, osc, server",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["python-osc"],
    project_urls={
        "Bug Reports": "https://github.com/Miniontoby/DmxOscServer/issues",
        "Source": "https://github.com/Miniontoby/DmxOscServer",
    },
)
