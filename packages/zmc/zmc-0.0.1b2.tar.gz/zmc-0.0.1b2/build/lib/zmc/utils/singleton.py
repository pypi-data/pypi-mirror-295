"""singleton decorator utils module."""

import functools


def singleton(cls):
    """Make a class a Singleton class.

    The __new__ and __init__ functions will only be called the first time the
    class is instantiated. All other times, the first instance will be returned
    without making any calls to the class itself.
    """

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if wrapper_singleton.instance is None:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton
