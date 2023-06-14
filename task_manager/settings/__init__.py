from .base import *

try:
    from .development import *
    live = False
except ImportError:
    live = True

if live:
    from .production import *
