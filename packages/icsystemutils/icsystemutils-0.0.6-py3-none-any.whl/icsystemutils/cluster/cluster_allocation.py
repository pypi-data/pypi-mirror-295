from .node import ComputeNode


class ClusterAllocation:
    def __init__(self) -> None:
        self.nodes: list[ComputeNode] = []
