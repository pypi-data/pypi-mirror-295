import asyncio
from functools import wraps

from fastapi import HTTPException


def must_response_in(seconds: float):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=408, detail="fun timeout, please retry later"
                )

        return wrapper

    return decorator
