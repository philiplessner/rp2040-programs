import functools
import time
from typing import Callable, Any
import aiohttp
from aiohttp import ClientSession


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total:.4f} second(s)")
        return wrapped
    return wrapper


@async_timed()
async def fetch_status(session: ClientSession,
                       url: str) -> int:
    timeout = aiohttp.ClientTimeout(total=4.0)
    async with session.get(url, timeout=timeout) as result:
        return result.status
