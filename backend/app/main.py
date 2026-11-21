from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.services.redis import ping_redis, close_redis
from app.db.database import check_db_health, init_db
from app.config import app_config

from app.api.hardware import hardware_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_config.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    await init_db()
    
    try:
        yield
    finally:
        await close_redis()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hardware_router)

@app.get("/health")
async def health_check():
    redis_status: bool = await ping_redis()
    db_status: bool = await check_db_health()

    healthy = redis_status and db_status

    status_code = (
        status.HTTP_200_OK
        if healthy
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return JSONResponse (
        status_code=status_code,
        content={
            "status": "healthy" if healthy else "unhealthy",
            "redis": redis_status,
            "sqlite": db_status,
        },
    )