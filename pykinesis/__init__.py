from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pykinesis")
except PackageNotFoundError:
    __version__ = "?.?.?"