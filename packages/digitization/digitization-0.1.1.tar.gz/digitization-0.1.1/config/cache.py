# Importing necessary modules and packages
import warnings
from typing import (TYPE_CHECKING,Any,Callable,Dict,Optional,Sequence,Tuple,Type,Union,cast)
from langchain.schema import ChatGeneration, Generation
from langchain.cache import BaseCache, _hash, _dump_generations_to_json, _load_generations_from_json

RETURN_VAL_TYPE = Sequence[Generation]

class RedisCache(BaseCache):
    """Cache that uses Redis as a backend."""

    def __init__(self, redis_: Any):
        """Initialize by passing in Redis instance."""
        try:
            from redis import Redis
        except ImportError:
            raise ValueError(
                "Could not import redis python package. "
                "Please install it with `pip install redis`."
            )
        if not isinstance(redis_, Redis):
            raise ValueError("Please pass in Redis object.")
        self.redis = redis_

    def _key(self, prompt: str, llm_string: str) -> str:
        """Compute key from prompt and llm_string"""
        return _hash(prompt + llm_string)

    def lookup(self, prompt: str, llm_string: str) -> Optional[RETURN_VAL_TYPE]:
        """Look up based on prompt and llm_string."""
        generations = []
        # Read from a Redis HASH
        key = self._key(prompt, llm_string)
        results = self.redis.hgetall(key)
        if results:
            for _, text in results.items():
                generations.append(Generation(text=text))
            self.redis.expire(key, 300)
        return generations if generations else None

    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """Update cache based on prompt and llm_string."""
        for gen in return_val:
            if not isinstance(gen, Generation):
                raise ValueError(
                    "RedisCache only supports caching of normal LLM generations, "
                    f"got {type(gen)}"
                )
            if isinstance(gen, ChatGeneration):
                warnings.warn(
                    "NOTE: Generation has not been cached. RedisCache does not"
                    " support caching ChatModel outputs."
                )
                return
        # Write to a Redis HASH
        key = self._key(prompt, llm_string)
        self.redis.hset(
            key,
            mapping={
                str(idx): generation.text for idx, generation in enumerate(return_val)
            },
        )
        self.redis.expire(key, 900)

    def clear(self, **kwargs: Any) -> None:
        """Clear cache. If `asynchronous` is True, flush asynchronously."""
        asynchronous = kwargs.get("asynchronous", False)
        self.redis.flushdb(asynchronous=asynchronous, **kwargs)
