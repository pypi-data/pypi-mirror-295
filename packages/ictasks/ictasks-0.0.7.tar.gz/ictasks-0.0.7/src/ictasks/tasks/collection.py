"""
This module is for a collection of tasks
"""

from pathlib import Path
import os
from typing import Generator

from iccore.serialization import Serializable

from .task import Task
from .taskfarm_file import TaskfarmFile


class TaskCollection(Serializable):
    """
    This is a collection of tasks which can be 'run' over
    a collection of workers
    """

    def __init__(self, job_dir: Path, group_size: int = 1) -> None:
        self.job_dir = job_dir
        self.job_id = ""
        self.group_size = group_size

        self.items: list[Task] = []
        self.num_grouped_tasks: int = 0

    def add_task(self, task: Task):
        task.job_dir = self.job_dir
        task.job_id = self.job_id
        self.items.append(task)

    def add_tasks(self, tasks: list[Task]):
        for task in tasks:
            self.add_task(task)

    def get_task(self, task_id: str) -> Task:
        for task in self.items:
            if task.task_id == task_id:
                return task
        raise KeyError(f"Task {task_id} not found")

    def get_running_tasks(self) -> Generator:
        for task in self.items:
            if task.is_running():
                yield task

    def has_running_tasks(self) -> bool:
        for task in self.items:
            if task.is_running():
                return True
        return False

    def has_grouped_tasks(self) -> bool:
        return self.group_size > 1

    def serialize(self):
        return {
            "group_size": self.group_size,
            "num_grouped_tasks": self.num_grouped_tasks,
            "items": [t.serialize() for t in self.items],
        }

    def read_taskfile(self, path: Path):
        taskfile = TaskfarmFile(self.job_dir, self.group_size)
        self.num_grouped_tasks, tasks = taskfile.read(path)
        self.add_tasks(tasks)

    def load_from_job_dir(self):
        ids = set()
        for entry in self.job_dir.iterdir():
            if entry.is_dir() and entry.name.startswith("task_"):
                ids.add(entry.name[len("task_") :])

        for each_id in ids:
            task = Task(self.job_dir)
            task.task_id = each_id
            self.add_task(task)

        for item in self.items:
            item.read()

    def write_task_dirs(self):
        for task in self.items:
            os.makedirs(task.get_task_dir(), exist_ok=True)
            task.write()

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return len(self.items)
