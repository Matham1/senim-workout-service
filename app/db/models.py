from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    exercise_type = Column(String, nullable=False)
    total_reps = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
