from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.redis_service import workout_service
from app.schemas.schemas import RepDetectionEvent, WorkoutStatus
import json
import logging
import uuid

router = APIRouter()
logger = logging.getLogger("uvicorn")

@router.websocket("/ws/workout")
async def workout_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Assign a unique session ID for this connection
    current_session_id = str(uuid.uuid4())
    # update global session_id (this is not best practice at all, but for demo purposes)
    import app.core.session_state
    app.core.session_state.session_id = current_session_id
    last_known_reps = 0
    
    logger.info(f"New connection. Assigned Session ID: {current_session_id}")
    
    while True:            
        try:
            data = await websocket.receive_text()
            payload = json.loads(data)
            event_data = RepDetectionEvent(**payload)

            if event_data.event == "rep_detected":
                # If Redis is empty but we previously had reps, it's a new session
                redis_reps = await workout_service.get_total_reps(current_session_id) #
                
                if redis_reps == 0 and last_known_reps > 0:
                    current_session_id = str(uuid.uuid4())
                    last_known_reps = 0

                # Process the rep using the current session ID
                current_reps = await workout_service.process_rep(current_session_id) #
                
                if current_reps:
                    last_known_reps = current_reps
                    response = WorkoutStatus(
                        event="rep_update",
                        status="success",
                        total_reps=current_reps
                    )
                    await websocket.send_text(response.model_dump_json())
                    logger.info(f"Rep counted. Total Reps: {current_reps} for Session {current_session_id}")
                else:
                    logger.info(f"Rep ignored (Debounce active)")
        except json.JSONDecodeError:
                await websocket.send_json({"status": "error", "message": "Invalid JSON"})
        except WebSocketDisconnect:
            logger.info(f"Connection closed for Session {current_session_id}")
            break
        except Exception as e:
            logger.error(f"Error processing message: {e}")