import json
from typing import Any


class JsonCache:
    def __init__(self, redis_url: str | None = None, ttl_seconds: int = 3600) -> None:
        self.redis_url = redis_url
        self.ttl_seconds = ttl_seconds
        self._memory: dict[str, str] = {}

    async def get(self, key: str) -> Any | None:
        raw = self._memory.get(key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: Any) -> None:
        self._memory[key] = json.dumps(value)

    async def invalidate(self, prefix: str) -> None:
        for key in [key for key in self._memory if key.startswith(prefix)]:
            self._memory.pop(key, None)


class RedisJsonCache(JsonCache):
    def __init__(self, redis_url: str, ttl_seconds: int = 3600) -> None:
        super().__init__(redis_url=redis_url, ttl_seconds=ttl_seconds)
        self._client = None

    async def _redis(self):
        if self._client is None:
            from redis.asyncio import from_url

            self._client = from_url(self.redis_url)
        return self._client

    async def get(self, key: str) -> Any | None:
        client = await self._redis()
        raw = await client.get(key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: Any) -> None:
        client = await self._redis()
        await client.set(key, json.dumps(value), ex=self.ttl_seconds)

    async def invalidate(self, prefix: str) -> None:
        client = await self._redis()
        async for key in client.scan_iter(f"{prefix}*"):
            await client.delete(key)

