import json


class ProcessorThread:
    """Class representing a logical thread on a processor core

    Attributes:
        id (int): An identifier for the thread

    Args:
        id (int): An identifier for the thread
    """

    def __init__(self, id: int) -> None:
        self.id = id

    def serialize(self) -> dict:
        return {"id": self.id}

    def __str__(self) -> str:
        return json.dumps(self.serialize())


class ProcessorCore:
    """Class representing a core on a processor

    Attributes:
        id (int): An identifier for the core
        threads (:obj:`dict`): A collection of threads on the core

    Args:
        id (int): An identifier for the core
    """

    def __init__(self, id: int) -> None:
        self.id = id
        self.threads: dict[int, ProcessorThread] = {}

    def add_thread(self, id: int):
        """Add a thread to the collection with the specified id

        Args:
            id (str): An identifier for the thread
        """
        self.threads[id] = ProcessorThread(id)

    def get_num_threads(self) -> int:
        return len(self.threads)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "threads": [t.serialize() for t in self.threads.values()],
        }

    def __str__(self) -> str:
        return json.dumps(self.serialize())


class PhysicalProcessor:
    """Class representing a real (physical) processor

    Attributes:
        id (int): An identifier for the processor
        core (:obj:`dict`): A collection of processor cores
        model (str): The manufacture's brand string
        cache_size (:obj:`int`): Size of the memory cache
        siblings (:obj:`int`): Counter indicating use of simultaneous multithreading

    Args:
        id (int): An identifier for the processor
    """

    def __init__(self, id: int) -> None:
        self.id = id
        self.cores: dict[int, ProcessorCore] = {}
        self.model = ""
        self.cache_size = 0
        self.siblings = 1

    def add_core(self, id: int):
        """Add a core to the collection with the specified id

        Args:
            id (str): An identifier for the core
        """
        self.cores[id] = ProcessorCore(id)

    def get_num_cores(self) -> int:
        return len(self.cores)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "cores": [c.serialize() for c in self.cores.values()],
            "model": self.model,
            "cache_size": self.cache_size,
            "siblings": self.siblings,
        }

    def __str__(self) -> str:
        return json.dumps(self.serialize())
