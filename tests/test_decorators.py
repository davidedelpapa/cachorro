"""Provides the unit tests for the decorators."""
import unittest
import os
import shutil
from time import sleep
from cachorro import cacheme

TEST_SAVED_DIR = 'saved_states'


class TestCacheme(unittest.TestCase):
    """Unit tests for cacheme decorator."""

    @classmethod
    def setUpClass(cls):
        """Set up any necessary initial conditions for the tests."""
        os.makedirs(TEST_SAVED_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are run."""
        shutil.rmtree(TEST_SAVED_DIR)

    def setUp(self):
        """Set up any necessary initial conditions for each test."""
        self.initial_vector = [1, 2, 3]

    def tearDown(self):
        """Clean up after each test if needed."""
        pass

    def test_cacheme(self):
        """Basic unit tests for cacheme decorator."""
        @cacheme
        def test_func(arr):
            """Dummy function to test the library."""
            sleep(1)
            return [x * 2 for x in arr]

        result_1 = test_func(self.initial_vector)
        result_2 = test_func(self.initial_vector)

        self.assertEqual(result_1, [2, 4, 6])
        self.assertEqual(result_1, result_2)

    def test_cacheme_error(self):
        """Unit tests for cacheme decorator with errors."""
        @cacheme
        def test_func_err(arr):
            """Dummy function to test the library."""
            sleep(1)
            return [x / 0 for x in arr]  # Division by zero

        with self.assertRaises(Exception):
            test_func_err(self.initial_vector)


if __name__ == '__main__':
    unittest.main()
