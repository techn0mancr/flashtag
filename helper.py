# Standard library imports
from random import randrange

def shuffle(lst):
    """
    Fisher-Yates shuffle with Durstenfeld's optimisations,
    sourced from https://en.m.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle.

    Parameters
    ----------
    lst : List[Any]
        _description_
    """
    n = len(lst)
    for i in range(n - 2):
        j = randrange(i, n)
        lst[i], lst[j] = lst[j], lst[i]