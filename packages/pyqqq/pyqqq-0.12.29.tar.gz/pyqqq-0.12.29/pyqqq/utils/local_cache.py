import os
import functools

from diskcache import Cache


class DiskCacheManager:
    def __init__(self, cache_name):
        parent_dir = os.getenv("CACHE_DIR") or "cache/"
        dir_str = os.path.join(parent_dir, cache_name)
        self.cache = Cache(dir_str)
        self.use_cache = os.getenv("STRATEGY_NAME") is None

    def memoize(self, expire=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.use_cache:
                    return func(*args, **kwargs)
                if expire is None:
                    return self.cache.memoize()(func)(*args, **kwargs)
                else:
                    return self.cache.memoize(expire=expire)(func)(*args, **kwargs)
            return wrapper
        return decorator
