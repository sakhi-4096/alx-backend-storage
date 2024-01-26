#!/usr/bin/env python3
"""
Module declares a redis class and methods.
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Count how many times methods of Cache class are called.

    Parameters:
    - method: The method to be decorated.
    Returns:
    A decorated wrapper function.
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        Wrap the decorated function and return the wrapper.

        Parameters:
        - self: The Cache instance.
        - *args: Variable positional arguments.
        - **kwargs: Variable keyword arguments.
        Returns:
        The result of the decorated function.
        '''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Store the history of inputs and outputs for a particular function.

    Parameters:
    - method: The method to be decorated.
    Returns:
    A decorated wrapper function.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        Wrap the decorated function and return the wrapper.

        Parameters:
        - self: The Cache instance.
        - *args: Variable positional arguments.
        - **kwargs: Variable keyword arguments.
        Returns:
        The result of the decorated function.
        '''
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data
    return wrapper


def replay(fn: Callable):
    '''
    Display the history of calls of a particular function.

    Parameters:
    - fn: The function to display the history for.
    Returns:
    None
    '''
    r = redis.Redis()
    func_name = fn.__qualname__
    call_count = r.get(func_name)
    try:
        call_count = int(call_count.decode("utf-8"))
    except Exception:
        call_count = 0
    print("{} was called {} times:".format(func_name, call_count))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for input_data, output_data in zip(inputs, outputs):
        try:
            input_data = input_data.decode("utf-8")
        except Exception:
            input_data = ""
        try:
            output_data = output_data.decode("utf-8")
        except Exception:
            output_data = ""
        print("{}(*{}) -> {}".format(func_name, input_data, output_data))


class Cache:
    '''
    Declares a Cache redis class.

    Methods:
    - __init__: Initializes a new Cache instance.
    - store: Stores data in the cache and returns a key.
    - get: Retrieves data from the cache using a key.
    - get_str: Retrieves a string from the cache using a key.
    - get_int: Retrieves an integer from the cache using a key.
    '''
    def __init__(self):
        '''
        Upon init to store an instance and flush the database.

        Parameters:
        None
        Returns:
        None
        '''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Takes a data argument and returns a string key.

        Parameters:
        - data: The data to be stored in the cache.
        Returns:
        A string key representing the stored data.
        '''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''
        Retrieves data from the cache using a key and applies an optional
        conversion function.

        Parameters:
        - key: The key to retrieve data from.
        - fn: Optional conversion function to be applied to the retrieved data.
        Returns:
        The retrieved data, optionally converted by the provided function.
        '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''
        Retrieves a string from the cache using a key.

        Parameters:
        - key: The key to retrieve the string from.
        Returns:
        The retrieved string.
        '''
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''
        Retrieves an integer from the cache using a key.

        Parameters:
        - key: The key to retrieve the integer from.
        Returns:
        The retrieved integer.
        '''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
