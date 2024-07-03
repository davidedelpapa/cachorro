"""Provides the main decorators for the cachorro library."""
import os
import pickle
import logging
from functools import wraps
from .utils import get_cache_filepath, _ensure_folder_exists


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def cacheme(func):
    """Cacheme decorator.

    A decorator function that caches the return values of a function.
    It checks if there is a saved state in a file, and if so, it returns it.
    If there is no saved state, it executes the function,
    saves the result to a file, and returns it.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        filepath = get_cache_filepath(func.__name__)
        _ensure_folder_exists(os.path.dirname(filepath))

        # Attempt to load a saved state
        if os.path.exists(filepath):
            try:
                with open(filepath, 'rb') as file:
                    return pickle.load(file)
            except Exception as e:
                log_msg = f"Error loading saved state from {filepath}: {e}\n"
                log_msg += "DEFAULT ACTION: probably corrupted pickle file, "
                log_msg += "DELETED"

                log.critical(log_msg)
                os.remove(filepath)  # Remove corrupted pickle file

        # If no saved state, execute the function and save the result
        try:
            result = func(*args, **kwargs)
            with open(filepath, 'wb') as file:
                pickle.dump(result, file)
            return result
        except Exception as e:
            log_msg = f"Error executing function {func.__name__}: {e}\n"
            log_msg += "DEFAULT ACTION: pickle file not created."
            log.critical(log_msg)

            # Ensure no corrupt state is saved
            if os.path.exists(filepath):
                os.remove(filepath)
            raise

    return wrapper
