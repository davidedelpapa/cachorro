"""Provides the unit tests for the decorators."""
import unittest
from cachorro.decorators import cacheme


class TestCacheme(unittest.TestCase):
    """Unit tests for cacheme decorator."""

    def test_cacheme(self):
        """Basic unit tests for cacheme decorator."""
        self.assertEqual(cacheme(), "Hello, world!")


if __name__ == '__main__':
    unittest.main()
