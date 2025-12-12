"""Lightweight decorators for common utilities.

This module contains small helpers used across examples and utilities.
"""

from typing import Any, Callable


def memoize_recursive(func: Callable) -> Callable:
    """
    Simple memoization decorator for recursive functions.

    Note: For Python 3.9+ prefer using `functools.cache` or
    `functools.lru_cache(maxsize=None)`.

    Example:
        @memoize_recursive
        def fib(n):
            if n < 2:
                return n
            return fib(n-1) + fib(n-2)
    """
    memo: dict[tuple[Any, ...], Any] = {}

    def wrapper(*args: Any) -> Any:
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]

    wrapper.cache = memo
    wrapper.clear_cache = memo.clear
    return wrapper
