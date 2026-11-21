from fastapi import APIRouter
import asyncio

from app.services.hardware import hardware_info_extractor, HardwareInfo

hardware_router = APIRouter(prefix="/api/hardware", tags=["Hardware"])

@hardware_router.get("/specs", response_model=HardwareInfo)
async def specs_extractor():
    return await asyncio.to_thread(hardware_info_extractor)