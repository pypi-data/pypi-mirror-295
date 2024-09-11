from setuptools import setup

from os import environ

MAJOR_VERSION = 0
MINOR_VERSION = 0
BUILD_VERSION = environ.get("BUILD_VERSION", "DEV")

__version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}.{BUILD_VERSION}"

setup(version=__version__)