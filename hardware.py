"""Hardware detection helpers for CPU, RAM, and GPU capabilities."""

from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import Dict, Any

import psutil

try:
    import torch
except Exception:  # pragma: no cover - torch might be unavailable.
    torch = None


@dataclass
class HardwareInfo:
    """Structured runtime hardware information."""

    os_name: str
    cpu_name: str
    cpu_cores_logical: int
    cpu_cores_physical: int
    ram_total_gb: float
    ram_available_gb: float
    has_gpu: bool
    gpu_name: str
    gpu_vram_gb: float



def _detect_gpu() -> tuple[bool, str, float]:
    """Detect GPU availability and VRAM using PyTorch when available."""
    if torch is None:
        return False, "N/A", 0.0

    try:
        if torch.cuda.is_available():
            device_idx = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(device_idx)
            vram = torch.cuda.get_device_properties(device_idx).total_memory / (1024**3)
            return True, gpu_name, round(vram, 2)
    except Exception:
        return False, "N/A", 0.0

    return False, "N/A", 0.0



def detect_hardware() -> HardwareInfo:
    """Collect high-level system hardware information."""
    vm = psutil.virtual_memory()
    has_gpu, gpu_name, gpu_vram = _detect_gpu()

    return HardwareInfo(
        os_name=f"{platform.system()} {platform.release()}",
        cpu_name=platform.processor() or "Unknown CPU",
        cpu_cores_logical=psutil.cpu_count(logical=True) or 1,
        cpu_cores_physical=psutil.cpu_count(logical=False) or 1,
        ram_total_gb=round(vm.total / (1024**3), 2),
        ram_available_gb=round(vm.available / (1024**3), 2),
        has_gpu=has_gpu,
        gpu_name=gpu_name,
        gpu_vram_gb=gpu_vram,
    )



def hardware_as_dict() -> Dict[str, Any]:
    """Expose hardware info as a serializable dictionary."""
    return detect_hardware().__dict__
