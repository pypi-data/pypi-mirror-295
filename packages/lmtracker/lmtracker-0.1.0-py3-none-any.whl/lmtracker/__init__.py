# lmtracker/lmtracker/__init__.py

# Import everything from track_mouse.py
from .track_mouse import *

# Optional: Define __all__ to control what gets exposed with wildcard imports
__all__ = [name for name in dir() if not name.startswith('_')]
