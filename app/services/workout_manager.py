from app.services.redis_service import workout_service
from app.db.models import WorkoutSession
from app.db.base import get_async_session
from sqlalchemy import insert
import datetime

async def save_workout_session(user_id: str, exercise_type: str, session_id: str) -> int:
    # 1. Get total reps from Redis
    try:
        total_reps = await workout_service.get_total_reps(session_id)
    except Exception as e:
        raise Exception(f"Failed to get total reps from Redis: {e}")
    try:
        async for session in get_async_session():
            stmt = insert(WorkoutSession).values(
                user_id=user_id,
                exercise_type=exercise_type,
                total_reps=total_reps,
                created_at=datetime.datetime.now()
            ).returning(WorkoutSession.id)
            result = await session.execute(stmt)
            await session.commit()
            workout_id = result.scalar_one()
    except Exception as e:
        raise Exception(f"Failed to save workout session to DB: {e}")
    
    await workout_service.clear_session(session_id)
    
    return workout_id