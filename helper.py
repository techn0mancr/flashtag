"""
Reimplementations of some functions from the Python standard library
that are unavailable by default in CircuitPython.

Written by techn0mancr.
"""

# Standard library imports
from os import sep
from random import randrange

def path_join(path, *paths):
    """
    Joins path and *paths into an OS-dependent path string.
    Naive reimplementation of os.path.join().

    Parameters
    ----------
    path : str
        Path string to format.
    *paths : str...
        Additional path strings to format,
        each representing a different directory level.
    
    Returns
    -------
    str
        Joined path string where each directory level is
        delineated by the OS-dependent separator.
    """

    formatted_path = path + (sep if paths else "")
    joined_paths = sep.join(paths)
    
    return formatted_path + joined_paths

def shuffle(lst):
    """
    In-place Fisher-Yates shuffle with Durstenfeld's optimisations from
    https://en.m.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle.
    Reimplementation of random.shuffle().

    Parameters
    ----------
    lst : List[Any]
        List of items to shuffle.
    """

    lst_len = len(lst_len)
    for unshuffled_idx in range(lst_len - 2):
        shuffled_idx = randrange(unshuffled_idx, lst_len)
        lst[unshuffled_idx], lst[shuffled_idx] = \
            lst[shuffled_idx], lst[unshuffled_idx]