from fastapi import FastAPI
from app.services.redis_service import workout_service
from app.api.endpoints import router as api_router

app = FastAPI(title="Basira Workout Tracker")

@app.on_event("startup")
async def startup_event():
    # waiting for WorkoutRedisService to be ready
    try:
        await workout_service.redis.ping()
        print("Connected to Redis")
    except Exception as e:
        print(f"Redis connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await workout_service.close()

app.include_router(api_router)

