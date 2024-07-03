"""Utilities for the library."""
import __main__
import os
import logging


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get_cache_filepath(func_name, program_name=None):
    """Generate the file path for the cache file.

    Generate the file path for the cache file based on the function name
    and the program name.
    Args:
        func_name (str): The name of the function.
        program_name (str, optional): The name of the program.
            If not provided, it will be derived from the current file name.

    Returns:
        str: The file path for the cache file.
    """
    if program_name is None:
        program_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    folder = 'saved_states'
    filename = f"{program_name}_{func_name}.pkl"
    filepath = os.path.join(folder, filename)

    return filepath


def _ensure_folder_exists(folder):
    """Ensure that a folder exists."""
    os.makedirs(folder, exist_ok=True)


def clear_cache(func_name, program_name=None):
    """Clears the cache for a specific function.

    Args:
        func_name (str): The name of the function for which to clearthe cache.
        program_name (str, optional): The name of the program.
            If not provided, it will be derived from the current file name.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> clear_cache('my_function')
        Cache cleared for my_script.py: my_function
        >>> clear_cache('my_function', 'my_program')
        Cache cleared for my_program.py: my_function
    """
    if program_name is None:
        program_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    filepath = get_cache_filepath(func_name, program_name)
    if os.path.exists(filepath):
        os.remove(filepath)
        log.info(f"Cache cleared for {__main__.__file__}: {func_name}")
    else:
        log.info(f"No cache found for {__main__.__file__}: {func_name}")
