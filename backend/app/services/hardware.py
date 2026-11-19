from pydantic import BaseModel
from app.config import app_config
import psutil

class GPUInfo(BaseModel):
    index: int
    name: str
    vram_total_mb: float
    vram_free_mb: float
    vram_used_mb: float
    utilization_percentage: float
    temperature_c: int | None

class SystemInfo(BaseModel):
    cpu_cores_physical: int | None
    cpu_cores_logical: int
    cpu_utilization_percentage: float
    ram_total_gb: float
    ram_available_gb: float
    disk_total_gb: float
    disk_available_gb: float

class HardwareInfo(BaseModel):
    gpu_available: bool
    driver_version: str | None
    gpus: list[GPUInfo]
    system: SystemInfo


to_gb = 1024**3

def system_info_extractor() -> SystemInfo:
    # CPU Info
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    cpu_utilization = psutil.cpu_percent(interval=0.5)

    # Ram Info
    total_ram = round((psutil.virtual_memory().total / to_gb), 2)
    available_ram = round((psutil.virtual_memory().available / to_gb), 2)

    # Disk Info
    total_disk = round((psutil.disk_usage(str(app_config.STORAGE_DIR)).total / to_gb), 2)
    available_disk = round((psutil.disk_usage(str(app_config.STORAGE_DIR)).free / to_gb), 2)

    return SystemInfo(
        cpu_cores_physical=physical_cores,
        cpu_cores_logical=logical_cores,
        cpu_utilization_percentage=cpu_utilization,
        ram_total_gb=total_ram,
        ram_available_gb=available_ram,
        disk_total_gb=total_disk,
        disk_available_gb=available_disk
    )