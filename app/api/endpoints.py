from fastapi import APIRouter, HTTPException
from app.api.websocket import router as ws_router
from app.services.workout_manager import save_workout_session

router = APIRouter()
router.include_router(ws_router)

CONSTANT_USER_ID = "1"
DEFAULT_EXERCISE_TYPE = "squat"

@router.get("/")
async def root():
    return {"message": "Workout Tracker Service is Running"}

@router.post("/workout/finish")
async def finish_workout():
    try:
        # For single user, assume session_id is user_id (or a constant)
        session_id = CONSTANT_USER_ID
        result = await save_workout_session(
            user_id=CONSTANT_USER_ID,
            exercise_type=DEFAULT_EXERCISE_TYPE,
            session_id=session_id
        )
        return {"status": "success", "workout_id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))