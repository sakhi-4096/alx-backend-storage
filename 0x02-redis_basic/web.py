#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps

# Initialize Redis connection
store = redis.Redis()


def count_url_access(method):
    """
    Decorator counting how many times a URL is accessed.

    Parameters:
    - method: The method to be decorated.
    Returns:
    A decorated wrapper function.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrap the decorated function and return the wrapper.

        Parameters:
        - url: The URL to be accessed.
        Returns:
        HTML content of the URL.
        """
        # Define keys for caching and counting
        cached_key = "cached:" + url
        count_key = "count:" + url

        # Check if the data is already cached
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # If not cached, retrieve HTML content using the decorated method
        html = method(url)

        # Increment the access count for the URL
        store.incr(count_key)

        # Cache the HTML content with a time-to-live (TTL) of 10 seconds
        store.set(cached_key, html)
        store.expire(cached_key, 10)

        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Returns HTML content of a URL.

    Parameters:
    - url: The URL to fetch HTML content from.
    Returns:
    HTML content of the URL.
    """
    # Perform a GET request to the specified URL
    res = requests.get(url)
    return res.text
