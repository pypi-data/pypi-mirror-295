import time

import asyncio
from requests.exceptions import HTTPError, ConnectionError, Timeout
from functools import wraps


def synchronized(lock):
    """Decorator to lock critical sections."""
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)
        return inner_wrapper
    return wrapper

def log_exceptions(logger):
    """Decorator to log exceptions."""
    def wrapper(f):
        @wraps(f)
        async def async_inner_wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in {f.__name__}: {str(e)}", exc_info=True)
                raise

        @wraps(f)
        def sync_inner_wrapper(*args, **kwargs):
            try:
                if asyncio.iscoroutinefunction(f):
                    return async_inner_wrapper(*args, **kwargs)
                else:
                    return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception occurred in {f.__name__}: {str(e)}", exc_info=True)
                raise

        return sync_inner_wrapper
    return wrapper

def retry_on_failure(max_retries, delay):
    """Decorator to retry on failure."""
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return f(*args, **kwargs)
                except (HTTPError, ConnectionError, Timeout) as e:
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        return inner_wrapper
    return wrapper
