#!/usr/bin/env python3
"""This Module implements an expiring web cache and tracker"""

import redis
from typing import Callable
from functools import wraps
import requests

r = redis.Redis(decode_responses=True)


def call_counts(func: Callable) -> Callable:
    """tracks how many times a url has been accessed"""
    @wraps(func)
    def wrapper_function(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)

        if not r.ttl(count_key):
            r.setex(count_key, 10)

        return func(url)

    return wrapper_function


@call_counts
def get_page(url: str) -> str:
    """Fetch the url content from the web"""
    response = requests.get(url)
    return response.text
