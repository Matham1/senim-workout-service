from pydantic import BaseModel
from typing import Literal

# Incoming message from CV model (Simplified)
class RepDetectionEvent(BaseModel):
    event: Literal["rep_detected"]
    type: str

# Outgoing: Feedback on Reps
class WorkoutStatus(BaseModel):
    event: Literal["rep_update"]
    status: str
    total_reps: int

# Outgoing: New Session Established (Server -> Client)
class SessionStartEvent(BaseModel):
    event: Literal["session_start"]
    session_id: str
    message: str

class FinishWorkoutRequest(BaseModel):
    user_id: str
    exercise_type: str
    session_id: str