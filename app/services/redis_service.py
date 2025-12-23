import redis.asyncio as redis
from app.core.config import settings

class WorkoutRedisService:
    def __init__(self):
        # Initialize Async Redis Client
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def close(self):
        await self.redis.close()

    async def process_rep(self, session_id: str) -> int | None:
        """
        Atomically checks for debounce and increments counter.
        Returns total_reps if successful, or None if debounced (ignored).
        """
        lock_key = f"lock:session:{session_id}"
        count_key = f"session:{session_id}:count"

        # Anti-Cheat
        # we set key value NX (Not Exists) and EX (Expire seconds)
        # returns True if key was set (lock acquired), False if key exists (locked)
        is_allowed = await self.redis.set(lock_key, "locked", nx=True, ex=1)

        if not is_allowed:
            # Logic: Lock exists, 1 second has not passed since last rep.
            return None

        # Increment the rep count only if lock was acquired
        new_count = await self.redis.incr(count_key)
        
        return new_count

    async def get_total_reps(self, session_id: str) -> int:
        count = await self.redis.get(f"session:{session_id}:count")
        return int(count) if count else 0

    async def clear_session(self, session_id: str):
        keys = [f"session:{session_id}:count", f"lock:session:{session_id}"]
        await self.redis.delete(*keys)

workout_service = WorkoutRedisService()