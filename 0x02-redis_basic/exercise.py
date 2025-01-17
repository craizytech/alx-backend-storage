#!/usr/bin/env python3
"""This module is for performing operations on redis"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional


class Cache:
    """This class contains operations done on redis"""

    def __init__(self):
        """This is the constructor method of the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
