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
        Exception if the cache file fails to load,
        after deleting the corrupted file.

    Example:
        >>> load_cache('my_function', program_name='my_program')
        Loading saved state for my_program: my_function
        <cached_result>
    """
    if program_name is None:
        program_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    complete_name = f"{program_name}: {func_name}"
    filepath = get_cache_filepath(func_name, program_name)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as file:
                log.info(f"Loading saved state for {complete_name}")
                return pickle.load(file)
        except Exception as e:
            log_msg = f"Error loading saved state for {complete_name}: {e}\n"
            log.critical(log_msg)
            os.remove(filepath)  # remove faulty pickle file
            raise
    else:
        log.info(f"No cache found for {func_name}")
        return None


def save_cache(data, func_name, program_name=None):
    """Saves to the cache file for the specified function.

    It substitutes the @cacheme decorator at times when it can't be used.
    For example, if the fuction is defined in a third party module,
    however we want to cache a result anyway.

    Args:
        data (Any): The data to be saved.
        func_name (str): The name of the function for which to save the cache.
        program_name (str, optional): The name of the program. If not provided,
            it will be derived from the current file name.

    Raises:
        Exception: If there is an error while saving the cache file.

    Example:
        >>> save_cache('data', 'my_function', 'my_program')
        Saving state for my_program: my_function
    """
    if program_name is None:
        program_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    complete_name = f"{program_name}: {func_name}"
    filepath = get_cache_filepath(func_name, program_name)
    _ensure_folder_exists(os.path.dirname(filepath))
    try:
        with open(filepath, 'wb') as file:
            log.info(f"Saving state for {complete_name}")
            pickle.dump(data, file)
    except Exception as e:
        log.critical(f"Failed to save state for {complete_name}: {e}")
        raise
