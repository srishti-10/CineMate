import os
import redis
import json
from typing import Optional, Any

# Get Redis connection details from environment variables or use defaults
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Function to get a Redis client
# Use this function wherever you need to interact with Redis

def get_redis_client():
    """
    Returns a Redis client instance connected to the specified host and port.
    """
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
    
    def set_cache(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        Set a value in cache with expiration time (default 1 hour).
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self.redis_client.setex(key, expire, value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        """
        try:
            value = self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except:
                    return value
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """
        Delete a key from cache.
        """
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def cache_movie_data(self, movie_id: str, movie_data: dict, expire: int = 1800) -> bool:
        """
        Cache movie data for 30 minutes.
        """
        key = f"movie:{movie_id}"
        return self.set_cache(key, movie_data, expire)
    
    def get_cached_movie(self, movie_id: str) -> Optional[dict]:
        """
        Get cached movie data.
        """
        key = f"movie:{movie_id}"
        return self.get_cache(key)
    
    def cache_popular_movies(self, movies: list, expire: int = 3600) -> bool:
        """
        Cache popular movies list for 1 hour.
        """
        key = "popular_movies"
        return self.set_cache(key, movies, expire)
    
    def get_cached_popular_movies(self) -> Optional[list]:
        """
        Get cached popular movies.
        """
        key = "popular_movies"
        return self.get_cache(key)
    
    def cache_user_session(self, user_id: str, session_data: dict, expire: int = 7200) -> bool:
        """
        Cache user session data for 2 hours.
        """
        key = f"session:{user_id}"
        return self.set_cache(key, session_data, expire)
    
    def get_user_session(self, user_id: str) -> Optional[dict]:
        """
        Get cached user session.
        """
        key = f"session:{user_id}"
        return self.get_cache(key)
    
    def cache_search_results(self, query: str, results: list, expire: int = 1800) -> bool:
        """
        Cache search results for 30 minutes.
        """
        key = f"search:{query.lower()}"
        return self.set_cache(key, results, expire)
    
    def get_cached_search(self, query: str) -> Optional[list]:
        """
        Get cached search results.
        """
        key = f"search:{query.lower()}"
        return self.get_cache(key)

# Global Redis cache instance
redis_cache = RedisCache() 