import json
import redis.asyncio as aioredis
from typing import Dict
from jose import JWTError
from pydantic import ValidationError
from fastapi import (
    FastAPI,
    Depends,
    status,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from app.core.config import settings
from app.api.router import router
from app.models.user import User
from app.services.user import UserService


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/",
)
app.include_router(router, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def test():
    return {"message": "pong!"}


@app.delete(
    "/reset_database",
    summary="Delete All Data",
    status_code=status.HTTP_200_OK,
)
async def reset_database(
    _: User = Depends(UserService.authenticate_current_user),
) -> Dict:
    try:
        return {"message": "Database cleared successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/tasks_status/{task_id}")
def task_status(task_id: str, _: User = Depends(UserService.authenticate_current_user)):
    try:
        response = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": response.status,
            "task_result": response.result,
        }
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.websocket("/websocket_task_status/{task_id}")
async def websocket_task_status(websocket: WebSocket, task_id: str):
    redis = aioredis.from_url(settings.CELERY_BROKER_URL)
    try:
        await websocket.accept()
        token_message = await websocket.receive_text()
        await UserService.authenticate_current_user(token_message)
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"task_updates:{task_id}")
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message:
                task_status = json.loads(message["data"])
                await websocket.send_json(task_status)

                if task_status.get("status") in ["SUCCESS", "FAILURE"]:
                    break

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except (JWTError, ValidationError):
        await websocket.close()
    finally:
        await pubsub.unsubscribe(f"task_updates:{task_id}")
        await pubsub.close()
