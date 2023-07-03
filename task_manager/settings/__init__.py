from .base import *
import os

if os.getenv('ACTION_MODE'):
    try:
        from .development import *
    except ImportError:
        from .production import *
else:
    from .production import *
