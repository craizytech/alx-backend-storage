#!/usr/bin/env python3
"""This module is for performing operations on redis"""

import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """
    counts how many times the method of the Cache class
    has been called
    """
    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_function


def call_history(method: Callable) -> Callable:
    """
    stores the history of inputs and outputs for a particular function
    """

    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        input_key = method.__qualname__ + ':inputs'
        output_key = method.__qualname__ + ':outputs'

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)
        return result

    return wrapper_function


def replay(func: Callable[..., Any]) -> None:
    """Displays the history of calls of a particular function"""
    r = redis.Redis()
    func_name = func.__qualname__
    func_redis_inputs = r.lrange(f"{func_name}:inputs", 0, -1)
    func_redis_outputs = r.lrange(f"{func_name}:outputs", 0, -1)

    func_inputs = [input.decode('utf-8') for input in func_redis_inputs]
    func_outputs = [output.decode('utf-8') for output in func_redis_outputs]

    times_called = len(func_inputs)
    print(f"{func_name} was called {times_called} times:")

    for input, output in zip(func_inputs, func_outputs):
        print(f"{func_name}(*{input}) -> {output}")


class Cache:
    """This class contains operations done on redis"""

    def __init__(self):
        """This is the constructor method of the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method stores the data passed into it in redis.

        Args:
            data: data to be stored

        Returns:
            uuid (string): the Id of the stored object
        """
        data_id = str(uuid4())
        self._redis.set(data_id, data)

        return data_id

    def get(
            self,
            key: str,
            fn: Optional[Callable[[bytes], Union[str, int]]] = None
            ) -> Union[bytes, str, int, None]:
        """
        This method retrieves data from the redis db

        Args:
            key (str): this is the key of the string to be retrieved

        Returns:
            bytestring of the returned data
        """
        data = self._redis.get(key)

        if data is None:
            return None

        return fn(data) if fn else data

    def get_str(self, data: bytes) -> str:
        """Converts bytes to string"""

        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """Converts bytes to integer"""

        return int(data.decode('utf-8'))
