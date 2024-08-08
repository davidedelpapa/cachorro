"""Provides the main decorators and pseudo-decortors for the cachorro library."""
import ast
import os
import pickle
import sys
import logging
from functools import wraps, partial
from .utils import get_cache_filepath, _ensure_folder_exists


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def cacheme(func=None, *, force_rerun=False):
    """Cacheme decorator.

    A decorator function that caches the return values of a function.
    It checks if there is a saved state in a file, and if so, it returns it.
    If there is no saved state, it executes the function,
    saves the result to a file, and returns it.

    Args:
        force_rerun (bool, optional): If True, the function will be executed,
            even if a cache exists, and re-cached. Defaults to False.
    """ # noqa D417
    if func is None:
        return partial(cacheme, force_rerun=force_rerun)

    @wraps(func)
    def wrapper(*args, **kwargs):
        filepath = get_cache_filepath(func.__name__)
        _ensure_folder_exists(os.path.dirname(filepath))

        # Attempt to load a saved state
        if not force_rerun and os.path.exists(filepath):
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


class Cached:
    """Cached class.

    The `Cached` class is used for caching function results.
    - __init__(self, func): Initializes the Cached instance by storing the function and cache file path.
    - __call__(self, *args, **kwargs): Checks if the cache file exists, loads and returns
        the cached result if available, otherwise executes the function, saves the result to the cache file,
        and returns it.
    - load(cache_file): Loads and returns the cached result from a specified cache file.
    - save(cache_file, result): Saves the given result to the specified cache file.
    """
    def __init__(self, func):
        """Initialize a new instance of the class.

        Args:
            func (function): The function to be cached.

        Returns:
            None
        """
        self.func = func
        self.cache_file = get_cache_filepath(func.__name__)
        _ensure_folder_exists(os.path.dirname(self.cache_file))

    def __call__(self, *args, **kwargs):
        """Execute the decorated function and cache its result in a file.

        Args:
            *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns:
            The result of the decorated function.

        Raises:
            None.

        Notes:
            - If a cache file exists, the function retrieves the cached result from the file.
            - If no cache file exists, the function executes the decorated function and caches
              its result in a file.
        """
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                # print(f"Using cached result from {self.cache_file}")
                return pickle.load(f)

        result = self.func(*args, **kwargs)
        with open(self.cache_file, 'wb') as f:
            pickle.dump(result, f)
            # print(f"Cached result to {self.cache_file}")
        return result

    @staticmethod
    def load(cache_file):
        """Load the cached result from the specified cache file.

        Args:
            cache_file (str): The path to the cache file.

        Returns:
            The cached result if the cache file exists and can be loaded, otherwise None.
        """
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                print(f"Using cached result from {cache_file}")
                return pickle.load(f)
        return None

    @staticmethod
    def save(cache_file, result):
        """Save the given result to the specified cache file.

        Args:
            cache_file (str): The path to the cache file.
            result (Any): The result to be saved.

        Returns:
            None

        Raises:
            None

        Notes:
            - The result is serialized using pickle and written to the cache file in binary mode.
            - The cache file is opened in write binary mode ('wb') and closed automatically using a context manager.
        """
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
            # print(f"Cached result to {cache_file}")


class CacheTransformer(ast.NodeTransformer):
    """CacheTransformer class.

    This class, `CacheTransformer`, is a subclass of `ast.NodeTransformer` from the `ast` module in Python.
    It's designed to transform Abstract Syntax Trees (ASTs) in Python.

    Here's a succinct explanation of what each method does:

    1. `__init__(self, cache_dir)`: This is the constructor method. It initializes the `CacheTransformer`
        instance with a `cache_dir` parameter, which is the directory where cache files will be stored.

    2. `visit_Assign(self, node)`: This method is called for each `ast.Assign` node in the AST.
        It checks if the assignment is a call to a function named `cacheme` and if the target
        of the assignment is a simple variable. If these conditions are met, it creates an AST that
        checks if a cached value exists, loads it if it does, or calls the function and saves the result
        if it doesn't. The cached value is stored in a file named after the variable.

    In summary, this class is used to transform Python code to automatically cache the results of function calls.
    """
    def __init__(self, cache_dir):
        """Initialize a new instance of the class.

        Args:
            cache_dir (str): The directory where cache files will be stored.

        Returns:
            None
        """
        self.cache_dir = cache_dir

    def visit_Assign(self, node):
        """Visit an assignment node in the abstract syntax tree (AST) and transform it.

        Visit an assignment node in the abstract syntax tree (AST) and transform it if the assignment
        is a call to a function named 'cacheme' and the target of the assignment is a simple variable.
        If these conditions are met, the function creates an AST that checks if a cached value exists,
        loads it if it does, or calls the function and saves the result if it doesn't. The cached
        value is stored in a file named after the variable.

        Args:
            node (ast.Assign): The assignment node to be visited.

        Returns:
            Union[ast.Assign, List[Union[ast.Assign, ast.If]]]: If the conditions for transformation
            are met, a list of AST nodes representing the transformed code is returned. Otherwise,
            the original assignment node is returned.
        """
        if (isinstance(node.value, ast.Call) and
                isinstance(node.targets[0], ast.Name) and
                hasattr(node.value.func, 'id') and
                node.value.func.id == 'cacheme'):

            var_name = node.targets[0].id
            func_name = node.value.args[0].id
            cache_file = os.path.join(self.cache_dir, f"{var_name}_cache.pkl")

            check_cache = ast.parse(f"{var_name} = Cached.load('{cache_file}')").body[0]
            call_func = ast.Assign(
                targets=[node.targets[0]],
                value=ast.Call(func=ast.Name(id=func_name, ctx=ast.Load()), args=[], keywords=[])
            )
            save_cache = ast.parse(f"Cached.save('{cache_file}', {var_name})").body[0]

            return [check_cache,
                    ast.If(
                        test=ast.Compare(
                            left=ast.Name(id=var_name, ctx=ast.Load()),
                            ops=[ast.Is()],
                            comparators=[ast.Constant(value=None)]
                        ),
                        body=[call_func, save_cache],
                        orelse=[]
                    )]
        return node


def transform_and_execute(script_path):
    """Transform and execute a script located at the given path.

    Args:
        script_path (str): The path to the script to be transformed and executed.

    Returns:
        None
    """
    with open(script_path, "r") as source:
        tree = ast.parse(source.read())

    transformer = CacheTransformer(Cached.cache_dir)
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    exec(compile(new_tree, filename=script_path, mode="exec"))


def initialize_caching(cache_dir='./cache'):
    """Initialize caching for a script located at the given path.

    Args:
        cache_dir (str): The directory where the cache files will be stored. Defaults to './cache'.

    Returns:
        None

    Raises:
        FileNotFoundError: If the script file specified by `sys.argv[0]` does not exist.

    This function takes the path to a script file as input and transforms and executes the script
    by adding caching functionality. The cache files are stored in the specified `cache_dir`.

    The function first obtains the absolute path of the script file using `sys.argv[0]`. It then
    calls the `transform_and_execute` function to transform and execute the script.

    Note:
        The `sys.argv[0]` argument is used to obtain the path to the script file. Make sure that
        the script file is provided as the first argument when running the script.

    Example:
        >>> initialize_caching('/path/to/script.py')
        None
    """
    script_path = os.path.abspath(sys.argv[0])
    transform_and_execute(script_path)
