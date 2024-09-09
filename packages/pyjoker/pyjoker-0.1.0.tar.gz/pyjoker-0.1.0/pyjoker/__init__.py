# pyjoker/__init__.py

from .jokes import get_joke
from .categories import JokeCategories

__all__ = ["get_joke", "JokeCategories"]
