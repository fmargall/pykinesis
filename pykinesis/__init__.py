# High level convenience class
from .kcube_solenoid import KCubeSolenoid

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pykinesis")
except PackageNotFoundError:
    __version__ = "?.?.?"