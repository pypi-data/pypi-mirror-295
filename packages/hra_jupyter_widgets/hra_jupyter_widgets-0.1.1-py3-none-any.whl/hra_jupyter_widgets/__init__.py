import importlib.metadata

from .widgets import *

try:
    __version__ = importlib.metadata.version("hra_jupyter_widgets")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
