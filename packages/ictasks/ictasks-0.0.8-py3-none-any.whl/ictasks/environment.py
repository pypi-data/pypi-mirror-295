"""
An environment in which a set of tasks run
"""

import uuid
import logging

from iccore.serialization import Serializable
from icsystemutils.cluster.node import ComputeNode

from .scheduler.schedulers.slurm import SlurmJob
from .worker_collection import WorkerCollection
from .worker import Worker
from .utils.queue import Queue

logger = logging.getLogger(__name__)


class Environment(Serializable):

    """
    A base compute environment
    """

    def __init__(self, workers: WorkerCollection) -> None:
        self.job_id: str = ""
        self.workers = workers
        self.nodelist: list[ComputeNode] = []
        self.worker_queue = Queue()

    def setup_worker_queue(self):
        if not self.worker_queue.ids:
            for worker in self.workers:
                self.worker_queue.push(worker.worker_id)

    def has_free_worker(self) -> bool:
        return self.worker_queue.available()

    def get_next_worker(self) -> Worker:
        return self.workers[self.worker_queue.pop()]

    def on_worker_freed(self, worker_id: str):
        self.worker_queue.push(worker_id)

    def serialize(self):
        return {
            "job_id": self.job_id,
            "workers": self.workers,
            "nodelist": [n.serialize() for n in self.nodelist],
        }


class BasicEnvironment(Environment):
    """
    A basic compute environment with e.g. no job scheduler
    This usually corresponds to running locally
    """

    def __init__(
        self,
        workers: WorkerCollection = WorkerCollection(),
        job_id: str = "",
        nodelist: list[str] | None = None,
    ) -> None:
        super().__init__(workers)

        if not job_id:
            self.job_id = str(uuid.uuid4())
        else:
            self.job_id = job_id

        if not nodelist:
            self.nodelist = [ComputeNode("localhost")]
        else:
            self.nodelist = [ComputeNode(a) for a in nodelist]

        self.workers.load(self.nodelist)


class SlurmEnvironment(Environment):
    """
    A slurm compute environment
    """

    def __init__(self, workers: WorkerCollection = WorkerCollection()) -> None:
        super().__init__(workers)
        self.slurm_job = SlurmJob()
        self.nodelist = [ComputeNode(a) for a in self.slurm_job.nodes]
        self.workers.load(self.nodelist)

    @staticmethod
    def detect() -> bool:
        return bool(SlurmJob.get_id())


def autodetect_environment(workers: WorkerCollection) -> Environment:
    if SlurmEnvironment.detect():
        logger.info("Detected we are running in a 'slurm' environment")
        return SlurmEnvironment(workers)

    logger.info("No runtime environment detected - using 'basic' environment")
    return BasicEnvironment(workers)
