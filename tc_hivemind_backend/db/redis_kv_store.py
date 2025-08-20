import json
from typing import Any, Dict

from llama_index.core.storage.kvstore.types import DEFAULT_COLLECTION
from llama_index.storage.kvstore.redis import RedisKVStore


class CustomRedisKVStore(RedisKVStore):
    """
    A Redis KV store that is compatible with redis-py clients configured with
    decode_responses=True. Overrides get_all/aget_all to avoid calling decode()
    on str keys/values.
    """

    def get_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
        collection_kv_dict: Dict[str, dict] = {}
        for key, val_str in self._redis_client.hscan_iter(name=collection):
            # Handle both bytes and str for key and value
            if isinstance(key, bytes):
                key = key.decode()
            if isinstance(val_str, bytes):
                val_str = val_str.decode()

            value_obj = json.loads(val_str) if val_str is not None else None
            if value_obj is not None:
                # Ensure dict type
                value_dict = value_obj if isinstance(value_obj, dict) else dict(value_obj)
                collection_kv_dict[key] = value_dict
        return collection_kv_dict

    async def aget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, dict]:
        collection_kv_dict: Dict[str, dict] = {}
        async for key, val_str in self._async_redis_client.hscan_iter(name=collection):
            if isinstance(key, bytes):
                key = key.decode()
            if isinstance(val_str, bytes):
                val_str = val_str.decode()

            value_obj = json.loads(val_str) if val_str is not None else None
            if value_obj is not None:
                value_dict = value_obj if isinstance(value_obj, dict) else dict(value_obj)
                collection_kv_dict[key] = value_dict
        return collection_kv_dict

    @classmethod
    def from_redis_client(cls, redis_client: Any) -> "CustomRedisKVStore":
        # Keep parity with upstream API for convenience
        return cls(redis_client=redis_client)


