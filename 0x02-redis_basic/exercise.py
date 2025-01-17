#!/usr/bin/env python3
"""This module is for performing operations on redis"""

import redis
from uuid import uuid4
from typing import Union


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
