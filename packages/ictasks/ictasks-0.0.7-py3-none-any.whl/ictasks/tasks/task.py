"""
This module describes a task, i.e. a small unit of work
"""

from pathlib import Path
import os
import time

from iccore.serialization import read_json, write_json, Serializable

from ictasks.stopping_condition import StoppingCondition

from .status import TaskStatus


class Task(Serializable):
    def __init__(
        self, task_id: str = "", launch_cmd: str = "", extra_paths: list | None = None
    ):
        self.launch_cmd = launch_cmd
        self.task_id = task_id
        self.job_id: str = ""
        self.job_dir: Path = Path(os.getcwd())
        self.inputs: dict = {}
        if extra_paths:
            self.extra_paths = extra_paths
        else:
            self.extra_paths = []
        self.status = TaskStatus()
        self.proc = None

    def check_status(self, stopping_condition: StoppingCondition | None):
        assert self.proc

        if self.proc.poll() is not None:
            self.status.set_is_finished(self.proc.poll())

        if stopping_condition:
            stopping_condition.eval(self.get_launch_file())

    def is_finished(self) -> bool:
        return self.status.is_finished()

    def is_running(self) -> bool:
        return self.status.is_running()

    def set_is_running(self, proc):
        self.proc = proc
        self.status.pid = proc.pid
        self.status.set_is_running()

    def set_inputs(self, inputs):
        self.inputs = dict(inputs)
        if "command" not in self.inputs:
            self.inputs["command"] = self.launch_cmd

    def get_task_dir(self) -> Path:
        return self.job_dir / f"task_{self.task_id}"

    def get_launch_file(self) -> Path:
        task_label = f"{self.status.host_id}-id{self.status.worker_id}-{self.job_id}"
        task_file_name = f"task-{task_label}.{self.task_id}"
        return self.job_dir / Path(task_file_name)

    def on_worker_assigned(self, host_id: str, worker_id: str):
        self.status.launch_time = time.time()
        self.status.host_id = host_id
        self.status.worker_id = worker_id

    def on_completed(self):
        self.status.walltime = time.time() - self.status.launch_time
        self.status.set_is_finished(self.proc.returncode)

    def serialize(self):
        return {
            "launch_cmd": self.launch_cmd,
            "id": self.task_id,
            "job_dir": str(self.job_dir),
            "extra_paths": self.extra_paths,
            "inputs": self.inputs,
            "status": self.status.serialize(),
        }

    def deserialize(self, content: dict):
        if "launch_cmd" in content:
            self.launch_cmd = content["launch_cmd"]
        if "id" in content:
            self.task_id = content["id"]
        if "job_dir" in content:
            self.job_dir = Path(content["job_dir"])
        if "inputs" in content:
            self.inputs = content["inputs"]
        if "extra_paths" in content:
            self.extra_paths = content["extra_paths"]
        if "status" in content:
            self.status = TaskStatus()
            self.status.deserialize(content["status"])

    def write(self, path: Path | None = None, filename: str = "task.json"):
        if not path:
            path = self.get_task_dir()

        write_json(self.serialize(), path / filename)

    def read(self, filename: str = "task.json"):
        content = read_json(self.get_task_dir() / filename)
        self.deserialize(content)
