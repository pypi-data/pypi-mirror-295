from icsystemutils.cpu import PhysicalProcessor
from icsystemutils.gpu import GpuProcessor


class ComputeNode:
    def __init__(self, address: str) -> None:
        self.address = address
        self.cpus: dict[int, PhysicalProcessor] = {}
        self.gpus: dict[int, GpuProcessor] = {}
