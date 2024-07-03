"""Utilities for the library."""
import __main__
import os
import pickle
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
        log.info(f"Cache cleared for {program_name}: {func_name}")
    else:
        log.info(f"No cache found for {program_name}: {func_name}")


def load_cache(func_name, program_name=None):
    """Load a specific funcion's cached result.

    This function loads a cached result from a file.
    It first checks if the `program_name` is provided, and if not,
    it infers it from the main file name. It then loads the cached result.
    If the loading fails, removes the cache file, and returns None

    Args:
        func_name (str): The name of the function to load the cache for.
        program_name (str, optional): The name of the program.
            If not provided, it will be inferred from the main file name.

    Returns:
        The cached result if found and successfully loaded,
            or None if the cache file does not exist or fails to load.

    Raises:
        None

    Example:
        >>> load_cache('my_function', program_name='my_program')
        Loading saved state for my_program: my_function
        <cached_result>
    """
    if program_name is None:
        program_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    filepath = get_cache_filepath(func_name, program_name)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as file:
                complete_name = f"{program_name}: {func_name}"
                log.info(f"Loading saved state for {complete_name}")
                return pickle.load(file)
        except Exception as e:
            log.critical(f"Failed to load saved state for {func_name}: {e}")
            os.remove(filepath)  # remove faulty pickle file
            return None
    else:
        log.info(f"No cache found for {func_name}")
        return None
