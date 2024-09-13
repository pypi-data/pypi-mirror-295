from iccore.serialization import Serializable
from icsystemutils.cluster.node import ComputeNode


class CoreRange(Serializable):
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def serialize(self):
        return {"start": self.start, "end": self.end}

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"


class WorkerHost(Serializable):
    def __init__(self, host_id: int, node: ComputeNode) -> None:
        self.host_id = host_id
        self.node = node

    def serialize(self):
        return {"id": self.host_id, "node": self.node.serialize()}


class Worker(Serializable):
    def __init__(self, worker_id, host: WorkerHost, cores: CoreRange) -> None:
        self.worker_id = worker_id
        self.host = host
        self.cores = cores

    def serialize(self):
        return {
            "id": self.worker_id,
            "host": self.host.serialize(),
            "cores": self.cores.serialize(),
        }

    def get_host_address(self) -> str:
        return self.host.node.address
