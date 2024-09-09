
# utils/caching.py
from functools import lru_cache, wraps
import time

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache

# Usage example:
# @timed_lru_cache(seconds=60)
# def get_user_info(user_id):
#     # Fetch user info from API
#     pass
