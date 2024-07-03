"""Provides the default imports for the cachorro library."""
from .decorators import cacheme
from .utils import get_cache_filepath


VERSION = "0.0.1"
__all__ = ['cacheme', 'get_cache_filepath', 'VERSION']
