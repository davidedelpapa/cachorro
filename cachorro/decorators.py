"""Provides the main decorators for the cachorro library."""
import os
import pickle
from functools import wraps


def cacheme(func):
    """Cacheme decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Construct the filename based on the function name
        program_name = os.path.splitext(os.path.basename(__file__))[0]
        folder = 'saved_states'
        filename = f"{program_name}_{func.__name__}.pkl"
        filepath = os.path.join(folder, filename)

        # Ensure the folder exists
        os.makedirs(folder, exist_ok=True)

        # Attempt to load the saved state
        if os.path.exists(filepath):
            with open(filepath, 'rb') as file:
                return pickle.load(file)

        # If no saved state, execute the function and save the result
        result = func(*args, **kwargs)
        with open(filepath, 'wb') as file:
            pickle.dump(result, file)

        return result
    return wrapper
