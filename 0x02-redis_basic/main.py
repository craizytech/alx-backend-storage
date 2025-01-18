#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache
from exercise import replay

cache = Cache()

s1 = cache.store("foo")
s2 = cache.store("bar")
s3 = cache.store(42)

replay(cache.store)
