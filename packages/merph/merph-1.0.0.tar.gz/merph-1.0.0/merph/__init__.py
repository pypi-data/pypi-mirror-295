
from importlib.metadata import version as _version

from .main import (Merph, load_Aubry, load_IVESPA, load_Mastin, load_Sparks,
                   read_csv, read_excel)
from .notebooks import launch_jupyter_example

__version__ = _version("merph")

__all__ = [
    'Merph',
    'read_excel',
    'read_csv',
    'load_IVESPA',
    'load_Aubry',
    'load_Mastin',
    'load_Sparks',
    'launch_jupyter_example',
]
