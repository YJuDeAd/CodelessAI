from pydantic import BaseModel

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