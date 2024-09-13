"""
This is a collection of workers representing processes or threads
that a task can run on
"""

import sys
import logging
from pathlib import Path

from iccore.serialization import Serializable
from icsystemutils.cluster.node import ComputeNode

from .worker import Worker, WorkerHost, CoreRange

logger = logging.getLogger(__name__)


class WorkerCollection(Serializable):
    def __init__(self, cores_per_node: int = 1, proc_per_node: int = 1) -> None:
        self.cores_per_node = cores_per_node
        self.proc_per_node = proc_per_node
        self.items: list[Worker] = []

    def serialize(self):
        return {
            "cores_per_node": self.cores_per_node,
            "proc_per_node": self.proc_per_node,
            "items": [w.serialize() for w in self.items],
        }

    def read(self, path: Path):
        logger.info("Reading nodefile at: %s, path")
        try:
            with open(path, "r", encoding="utf-8") as f:
                nodes = [ComputeNode(n) for n in f.read().splitlines()]
                self.load(nodes)
        finally:
            logger.error("Error opening node file %s. Exiting.", path)
            sys.exit(2)

    def load(self, nodes: list[ComputeNode]):
        logger.info("Setting up workers")
        for idx, node in enumerate(nodes):
            if not self._node_is_registered(node):
                self._add_worker(WorkerHost(idx, node))
        logger.info("Set up %d workers", len(self.items))

    def _add_worker(self, host: WorkerHost):
        cores_per_task = int(self.cores_per_node / self.proc_per_node)
        for proc_id in range(self.proc_per_node):
            worker_id = host.host_id + proc_id % self.cores_per_node
            core_list = self._get_core_range(proc_id, cores_per_task)
            self.items.append(Worker(worker_id, host, core_list))

    def _get_core_range(self, proc_id: int, cores_per_task: int) -> CoreRange:
        start = proc_id % self.cores_per_node * cores_per_task
        end = start + cores_per_task - 1
        return CoreRange(start, end)

    def _node_is_registered(self, node: ComputeNode) -> bool:
        for worker in self.items:
            if worker.host.node.address == node.address:
                return True
        return False

    def __getitem__(self, arg):
        return self.items[arg]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()
