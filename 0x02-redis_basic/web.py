#!/usr/bin/env python3
"""This Module implements an expiring web cache and tracker"""

import redis
from typing import Callable
from functools import wraps
import requests

r = redis.Redis(decode_responses=True)


def cache_webpage(func: Callable) -> Callable:
    """tracks how many times a url has been accessed"""

    @wraps(func)
    def wrapper_function(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)
        cached_response = r.get(f"cached:{url}")
        if cached_response:
            return cached_response

        web_content = func(url)
        r.setex(f"cached:{url}", 10, web_content)

        return web_content

    return wrapper_function

@cache_webpage
def get_page(url: str) -> str:
    """Fetch the url content from the web"""
    response = requests.get(url)
    return response.text
