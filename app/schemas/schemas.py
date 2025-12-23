from pydantic import BaseModel
from typing import Literal

class RepDetectionEvent(BaseModel):
    event: Literal["rep_detected"]
    type: str

class WorkoutStatus(BaseModel):
    event: Literal["rep_update"]
    status: str
    total_reps: int

class FinishWorkoutRequest(BaseModel):
    user_id: str
    exercise_type: str
    session_id: str