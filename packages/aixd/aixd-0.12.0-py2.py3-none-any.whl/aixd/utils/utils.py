import os
from typing import Any, Callable, Dict, List

import numpy as np


def apply_list(ls: list, func: Callable[[Any], list]) -> list:
    """
    Applies a function to all elements in the list. Works with nested lists.

    Parameters
    ----------
    ls : Iterable
        The input list.
    func : Callable
        The function to be applied to each element in the list.

    Returns
    -------
    Iterable
        A new list with the same structure as the input list, where the function has been applied to all elements.

    Examples
    --------
    >>> def square(x):
    ...     return x ** 2
    ...
    >>> numbers = [1, 2, [3, 4, [5, 6]]]
    >>> apply_list(numbers, square)
    [1, 4, [9, 16, [25, 36]]]

    """
    if isinstance(ls, list):
        return [apply_list(elem, func) for elem in ls]
    else:
        return func(ls)


def apply_dict(d: Dict, func: Callable) -> Dict:
    """
    Recursively applies a given function to all values in a nested dictionary.

    Parameters
    ----------
    d: Dict
        The input dictionary.
    func: Callable
        The function to be applied to each value in the dictionary.

    Returns
    -------
    Dict
        A new dictionary with the same structure as the input dictionary, where the function
        has been applied to all values.

    Notes
    -----
    - This function is designed to work with nested dictionaries, where the values themselves
      can also be dictionaries or other types.
    - If the input dictionary (or any nested dictionary) contains non-dictionary values,
      the function `func` is applied to those values directly.

    Examples
    --------
    >>> def square(x):
    ...     return x ** 2
    ...
    >>> d = {'a': 2, 'b': {'x': 3, 'y': 4}, 'c': 5}
    >>> apply_dict(d,square)
    {'a': 4, 'b': {'x': 9, 'y': 16}, 'c': 25}

    """
    if isinstance(d, dict):
        return {key: apply_dict(value, func) for key, value in d.items()}
    else:
        return func(d)


def flatten_list(ls: list) -> list:
    """
    Flattens a nested list to a single list.

    Parameters
    ----------
    ls : Iterable
        An n-dimensional nested list.

    Returns
    -------
    Iterable
        A single list containing all elements from the input n-dimensional nested list.

    Examples
    --------
    >>> numbers = [1, 2, [3, 4, [5, 6]]]
    >>> flatten_list(numbers)
    [1, 2, 3, 4, 5, 6]
    """

    if isinstance(ls, list):
        return [elem for sublist in ls for elem in flatten_list(sublist)]
    else:
        return [ls]


def flatten_dict(d: Dict, with_keys: bool = False) -> List:
    """
    Flattens a nested dictionary to a list.

    Parameters
    ----------
    d : Dict
        The input dictionary to be flattened.
    with_keys : bool, optional (default=False)
        Specifies whether to include keys in the flattened list.
        If True, each entry in the list will be a tuple of (key, value).
        If False, only the values will be included in the list.

    Returns
    -------
    List
        A list containing either the values or key-value tuples from the input dictionary.
        The order of elements in the list follows a depth-first traversal of the input dictionary.

    Examples
    --------
    >>> d = {'a': 1, 'b': {'x': 2, 'y': 3}, 'c': 4}
    >>> flatten_dict(d)
    [1, 2, 3, 4]

    >>> flatten_dict(d, with_keys=True)
    [('a', 1), ('x', 2), ('y', 3), ('c', 4)]
    """
    flattened_list = []
    for key, value in d.items():
        if isinstance(value, dict):
            flattened_list.extend(flatten_dict(value, with_keys))
        else:
            flattened_list.append((key, value) if with_keys else value)
    return flattened_list


def list_unique(ls: list) -> list:
    """
    Returns the unique elements of a list, preserving the order of the original list.

    Parameters
    ----------
    ls : list
        The input list.

    Returns
    -------
    list
        A new list containing the unique elements of the input list, preserving the order of the original list.

    Examples
    --------
    >>> list_unique([1, 2, 3, 1, 2, 4, 5, 3])
    [1, 2, 3, 4, 5]
    """

    hashmap = {}
    unique_list = []
    for elem in ls:
        if elem not in hashmap:
            hashmap[elem] = True
            unique_list.append(elem)
    return unique_list


def float_ceil(a, digits=0):
    """
    Returns the smallest float with the given number of digits after the decimal point that is greater than or equal to the input.

    Parameters
    ----------
    a : float
        The input float.
    digits : int, optional (default=0)
        The number of digits after the decimal point.

    Returns
    -------
    float
        The smallest float with the given number of digits after the decimal point that is greater than or equal to the input.

    Examples
    --------
    >>> float(float_ceil(1.2345, 2))
    1.24
    >>> float(float_ceil(1.2345, 3))
    1.235
    >>> float(float_ceil(1.2345, 4))
    1.2345
    """
    return np.true_divide(np.ceil(a * 10**digits), 10**digits)


def float_floor(a, digits=0):
    """
    Returns the largest float with the given number of digits after the decimal point that is less than or equal to the input.

    Parameters
    ----------
    a : float
        The input float.
    digits : int, optional (default=0)
        The number of digits after the decimal point.

    Returns
    -------
    float
        The largest float with the given number of digits after the decimal point that is less than or equal to the input.

    Examples
    --------
    >>> float(float_floor(1.2345, 2))
    1.23
    >>> float(float_floor(1.2345, 3))
    1.234
    >>> float(float_floor(1.2345, 4))
    1.2345
    """
    return np.true_divide(np.floor(a * 10**digits), 10**digits)


def dirname(path: str) -> str:
    """
    Returns the directory name of a path. This is the same as os.path.dirname, but it also normalizes the path. In particular, it removes trailing slashes.

    Parameters
    ----------
    path : str
        The path to a file or directory.

    Returns
    -------
    str
        The directory name of the path.

    Examples
    --------
    >>> dirname("aixd/data/constants.py") # doctest: +SKIP
    'aixd/data'
    >>> dirname("aixd/data/") # doctest: +SKIP
    'aixd/data'

    """
    return os.path.normpath(os.path.dirname(path))


def basename(path: str) -> str:
    """
    Returns the base name of a path. This is the same as os.path.basename, but it normalizes the path first. In particular, it removes trailing slashes.

    Parameters
    ----------
    path : str
        The path to a file or directory.

    Returns
    -------
    str
        The base name of the path.

    Examples
    --------
    >>> basename("aixd/data/constants.py")
    'constants.py'
    >>> basename("aixd/data/")
    'data'
    >>> basename(dirname("aixd/data/constants.py"))
    'data'

    """
    return os.path.basename(os.path.normpath(path))
