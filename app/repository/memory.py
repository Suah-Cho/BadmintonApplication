from abc import ABC, abstractmethod


class BaseCacheRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> dict | str | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: str | dict):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass

    @abstractmethod
    async def scan(self, pattern: str) -> list:
        pass


# class RedisRepository(BaseCacheRepository):
#     def __init__(self, redis_url: str):
#         self.redis = aioredis.from_url(redis_url, decode_responses=True)

#     async def get(self, key: str):
#         return await self.redis.get(key)

#     async def set(self, key: str, value: str):
#         await self.redis.set(key, value)

#     async def delete(self, key: str):
#         await self.redis.delete(key)

#     async def scan(self, pattern: str) -> list:
#         cursor = "0"
#         keys = []
#         while cursor != 0:
#             cursor, partial_keys = await self.redis.scan(cursor=cursor, match=pattern)
#             keys.extend(partial_keys)
#         return keys


class InMemoryCacheRepository(BaseCacheRepository):
    def __init__(self):
        self.store = {}

    async def get(self, key: str) -> dict | str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str | dict):
        self.store[key] = value

    async def delete(self, key: str):
        if key in self.store:
            del self.store[key]

    async def scan(self, pattern: str) -> list:
        import fnmatch

        return [key for key in self.store.keys() if fnmatch.fnmatch(key, pattern)]


# if config.USE_REDIS:
#     repository: BaseCacheRepository = RedisRepository(
#         redis_url="redis://localhost:6379/0"
#     )
# else:
#     repository: BaseCacheRepository = InMemoryCacheRepository()

repository: BaseCacheRepository = InMemoryCacheRepository()


def get_cache_repository() -> BaseCacheRepository:
    return repository
