from pydantic import BaseModel
from app.config import app_config
import psutil
import pynvml

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
to_mb = 1024**2

def system_info_extractor() -> SystemInfo:
    # CPU Info
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    cpu_utilization = psutil.cpu_percent(interval=0.5)

    # Ram Info
    ram = psutil.virtual_memory()
    total_ram = round((ram.total / to_gb), 2)
    available_ram = round((ram.available / to_gb), 2)

    # Disk Info
    disk = psutil.disk_usage(str(app_config.STORAGE_DIR))
    total_disk = round((disk.total / to_gb), 2)
    available_disk = round((disk.free / to_gb), 2)

    return SystemInfo(
        cpu_cores_physical=physical_cores,
        cpu_cores_logical=logical_cores,
        cpu_utilization_percentage=cpu_utilization,
        ram_total_gb=total_ram,
        ram_available_gb=available_ram,
        disk_total_gb=total_disk,
        disk_available_gb=available_disk
    )

def gpu_info_extractor() -> tuple[bool, str | None, list[GPUInfo]]:
    try:
        pynvml.nvmlInit()
        try:
            driver_version = pynvml.nvmlSystemGetDriverVersion()
            gpus: list[GPUInfo] = []
            for i in range(pynvml.nvmlDeviceGetCount()):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                vram = pynvml.nvmlDeviceGetMemoryInfo(handle)
                total_vram = round((vram.total / to_mb), 2)
                free_vram = round((vram.free / to_mb), 2)
                used_vram = round((vram.used / to_mb), 2)
                gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
                
                try:
                    gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                except pynvml.NVMLError:
                    gpu_temp = None
                
                gpu = GPUInfo(
                    index=i,
                    name=name,
                    vram_total_mb=total_vram,
                    vram_free_mb=free_vram,
                    vram_used_mb=used_vram,
                    utilization_percentage=gpu_utilization,
                    temperature_c=gpu_temp
                )
                
                gpus.append(gpu)
            return (True, driver_version, gpus)
        finally:
            pynvml.nvmlShutdown()
    except pynvml.NVMLError:
        return (False, None, [])