from fastapi import APIRouter, HTTPException, Depends
from app.routers.websocket import router as ws_router
from app.services.workout_manager import save_workout_session
from app.db.base import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import WorkoutSession

router = APIRouter()
router.include_router(ws_router)

CONSTANT_USER_ID = "1"
DEFAULT_EXERCISE_TYPE = "squat"

@router.get("/")
async def root():
    return {"message": "Workout Tracker Service is Running"}

@router.post("/workout/finish")
async def finish_workout():
    from app.core.session_state import session_id #(this is not best practice at all, but for demo purposes)
    try:
        result = await save_workout_session(
            user_id=CONSTANT_USER_ID,
            exercise_type=DEFAULT_EXERCISE_TYPE,
            session_id=session_id # we are using actual session_id from websocket.py
        )
        return {"status": "success", "workout_id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workout/sessions")
async def get_workout_sessions(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(
            WorkoutSession.__table__.select()
        )
        sessions = result.fetchall()
        return [
            {
                "id": s.id,
                "user_id": s.user_id,
                "exercise_type": s.exercise_type,
                "total_reps": s.total_reps,
                "created_at": s.created_at.isoformat() if s.created_at else None
            }
            for s in sessions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))