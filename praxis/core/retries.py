import time
from typing import Callable


def retry(
    fn: Callable,
    *,
    retries: int = 2,
    backoff: float = 0.5,
    retry_on: tuple[type[Exception], ...] = (Exception,),
):
    last_exc = None

    for attempt in range(retries + 1):
        try:
            return fn()
        except retry_on as exc:
            last_exc = exc
            if attempt == retries:
                break
            time.sleep(backoff * (attempt + 1))

    raise last_exc
