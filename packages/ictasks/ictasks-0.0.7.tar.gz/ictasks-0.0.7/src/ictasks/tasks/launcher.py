"""
This module has a class for launching tasks
"""

import logging
import time
from subprocess import Popen
import os

from ictasks.worker import Worker
from .task import Task

logger = logging.getLogger()


class TaskLauncher:
    """
    This class is responsible for launching tasks. The launching
    is done by derived classes.
    """

    def __init__(
        self,
        stop_on_error: bool = True,
    ) -> None:
        self.stop_on_error = stop_on_error
        self.create_task_dirs = True

    def launch(self, task: Task, worker: Worker) -> None:

        """
        Launch the task in derived classes
        """
        raise NotImplementedError()


class SubprocessTaskLauncher(TaskLauncher):

    """
    This class runs tasks as a Python subprocess
    """

    def __init__(self, stop_on_error: bool = True):
        super().__init__(stop_on_error)

        self.stdout_filename = "task_stdout.txt"
        self.stderr_filename = "task_stderr.txt"

    def launch(self, task: Task, worker: Worker):

        task_dir = task.get_task_dir()
        stdout_f = open(task_dir / self.stdout_filename, "w", encoding="utf-8")
        stderr_f = open(task_dir / self.stderr_filename, "w", encoding="utf-8")

        task.status.launch_time = time.time()
        proc = Popen(
            task.launch_cmd,
            shell=True,
            env=os.environ.copy(),
            cwd=task_dir,
            stdout=stdout_f,
            stderr=stderr_f,
        )
        stdout_f.close()
        stderr_f.close()
        task.set_is_running(proc)
        logger.info("Task pid is %d", task.status.pid)


class ShellTaskLauncher(TaskLauncher):

    """
    This launcher creates a file with the task's command line args
    and runs it as a shell script.
    """

    def __init__(
        self,
        stop_on_error: bool = True,
    ) -> None:
        super().__init__(stop_on_error)

        self.runtime_env: str = ""
        self.env_exclude_params = ["PROFILEREAD", "BASH_FUNC_module()"]
        self.create_task_dirs = False

        self.initialize_environment()

    def initialize_environment(self):
        for param in os.environ:
            if param not in self.env_exclude_params:
                export_cmd = f"export {param}='{os.environ[param]}'; "
                self.runtime_env = self.runtime_env + export_cmd

    def write_launch_file(self, task: Task):
        task_cmd = task.launch_cmd
        wrapped_cmd = f"{self.runtime_env} cd {os.getcwd()} && {task_cmd}"

        os.makedirs(task.get_launch_file().parent, exist_ok=True)
        with open(task.get_launch_file(), "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n")
            f.write(wrapped_cmd)
        os.chmod(task.get_launch_file(), 0o0755)

    def launch_with_args(self, task: Task, args):
        #        task.full_cmd = ""
        #        for arg in args:
        #            task.full_cmd += arg + " "
        logger.info("Launch args %s", args)

        task.status.launch_time = time.time()
        proc = Popen(args)  # type: ignore
        task.set_is_running(proc)
        logger.info("Task pid is %d", task.status.pid)

    def launch(self, task: Task, worker: Worker):
        self.write_launch_file(task)

        args = [str(task.get_launch_file())]
        self.launch_with_args(task, args)


class MpiTaskLauncher(ShellTaskLauncher):

    """
    This class launches a task via an mpi wrapper and launch
    commands in a shell script.
    """

    def __init__(
        self, launch_wrapper: str, cores_per_task: int = 1, stop_on_error: bool = True
    ):
        super().__init__(stop_on_error)
        self.launch_wrapper = launch_wrapper
        self.cores_per_task = cores_per_task

    def launch(self, task: Task, worker: Worker):
        self.write_launch_file(task)

        args = [
            self.launch_wrapper,
            "-env",
            "I_MPI_PIN_PROCESSOR_LIST",
            str(worker.cores),
            "-n",
            str(self.cores_per_task),
            "-host",
            worker.get_host_address(),
            str(task.get_launch_file()),
        ]

        self.launch_with_args(task, args)
