#!/usr/bin/python3
"""This Module implements an expiring web cache and tracker"""

import redis
from typing import Callable
from functools import wraps
import requests

r = redis.Redis(decode_responses=True)


def load_from_cache(func: Callable) -> Callable:
    """
    retrieves the web page from the cache if it does not exit at
    the cache then it gets it from the web page itself
    """
    @wraps(func)
    def wrapper_function(url: str) -> str:
        cached_webpage = r.get(url)
        if cached_webpage:
            return cached_webpage

        web_content = func(url)
        r.setex(url, 10, web_content)
        return web_content

    return wrapper_function


def call_counts(func: Callable) -> Callable:
    """tracks how many times a url has been accessed"""
    @wraps(func)
    def wrapper_function(url: str) -> str:
        r.incr(f"count:{url}")
        return func(url)

    return wrapper_function


@load_from_cache
@call_counts
def get_page(url: str) -> str:
    """Fetch the url content from the web"""
    response = requests.get(url)
    return response.text
