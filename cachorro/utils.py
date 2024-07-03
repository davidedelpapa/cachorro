"""Utilities for the library."""
import __main__
import os


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
