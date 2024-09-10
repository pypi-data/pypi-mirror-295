# -*- coding: utf-8 -*-
__all__ = ["ContextLock"]
__credits__ = ["QuacktorAI", "ruecat"]

from asyncio import Lock


class ContextLock:
    """ Lock an object when modifying shared memory resources across several asynchronous calls.
        Can be called in an `async with` statement thanks to `__aenter__` and `__aexit__` definitions
    """

    def __init__(self):
        self.lock = Lock()

    async def __aenter__(self):
        await self.lock.acquire()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.lock.release()
