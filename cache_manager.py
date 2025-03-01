# cache_manager.py
import asyncio
import time
from typing import Any, Optional

class CacheEntry:
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expiry = time.monotonic() + ttl

    def is_expired(self) -> bool:
        return time.monotonic() > self.expiry

class Cache:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            entry = self._cache.get(key)
            if entry and not entry.is_expired():
                return entry.value
            if key in self._cache:
                del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl: int):
        async with self._lock:
            self._cache[key] = CacheEntry(value, ttl)

    async def clear(self):
        async with self._lock:
            self._cache.clear()
