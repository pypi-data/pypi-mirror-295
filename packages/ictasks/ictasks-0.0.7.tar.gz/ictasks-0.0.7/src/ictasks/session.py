"""
This module is for a single batch job or session
"""

import time
import logging

from .environment import Environment, BasicEnvironment
from .tasks import TaskCollection, TaskLauncher, SubprocessTaskLauncher
from .stopping_condition import StoppingCondition

logger = logging.getLogger(__name__)


class Session:
    """This class represents a single batch job or session

    Attributes:
        job_id (str): Idenitifier for the job or session
        nodelist (:obj:`list`): List of compute nodes available to run on
        tasks_path (:obj:`Path`): Path to a list of tasks to run
    """

    def __init__(
        self,
        tasks: TaskCollection,
        environment: Environment = BasicEnvironment(),
        launcher: TaskLauncher = SubprocessTaskLauncher(),
        sleep_duration: float = 1.0,
    ) -> None:

        self.env = environment
        self.tasks: TaskCollection = tasks
        self.launcher = launcher
        self.stopping_condition = StoppingCondition()

        self.sleep = sleep_duration

    def run(self):
        """
        Run the session by iterating over all
        tasks an assigning them to waiting workers.
        """
        self._log_launch_info()

        self.env.setup_worker_queue()

        if self.launcher.create_task_dirs:
            self.tasks.write_task_dirs()

        for i, task in enumerate(self.tasks):
            if not self.env.has_free_worker():
                self._wait_for_workers()

            iteration = f"{i+1}/{len(self.tasks)}"
            logger.info("Launching %s, task %s", iteration, task.task_id)
            worker = self.env.get_next_worker()
            task.on_worker_assigned(worker.host.host_id, worker.worker_id)

            self.launcher.launch(task, worker)

        logger.info("All tasks launched. Waiting on tasks to finish.")
        while self.tasks.has_running_tasks():
            self._wait_for_workers()
        logger.info("All tasks finished.")

    def _log_launch_info(self):
        has_grouped_tasks = self.tasks.has_grouped_tasks()
        num_workers = len(self.env.workers)
        assert num_workers > 0
        num_tasks = len(self.tasks)

        ppn = self.env.workers.proc_per_node
        logger.info("Started with %d workers (%d per node).", num_workers, ppn)
        if has_grouped_tasks:
            grouped_tasks = self.tasks.num_grouped_tasks
            logger.info(
                "Has %d tasks, grouped as %d metatasks.",
                num_tasks,
                grouped_tasks,
            )
        else:
            logger.info("Has %d tasks.", num_tasks)

        if num_tasks % num_workers != 0:
            logger.warning(
                "Number of %d tasks should be multiple of %d workers.",
                num_tasks,
                num_workers,
            )
        if num_tasks / num_workers > 20:
            msg = f"""There are {num_tasks} tasks for {num_workers} workers.
                This tool is not ideal for high-throughput workloads.
                You can aggregate tasks using export TASKFARM_GROUP=xxx
                with xxx how many consecutive tasks to group in a metatask"""
            logger.warning(msg)

    def _wait_for_workers(self):
        while True:
            has_finished_tasks = False
            should_exit = False
            exit_info = {}

            for task in self.tasks.get_running_tasks():
                task.check_status(self.stopping_condition)
                if task.is_finished():
                    logger.info("Task %s is finished", task.task_id)
                    task.on_completed()
                    should_exit = task.status.return_code != 0
                    exit_info["return_code"] = task.status.return_code
                    exit_info["cmd"] = task.launch_cmd
                    has_finished_tasks = True

                    if self.launcher.create_task_dirs:
                        task.write()
                    self.env.on_worker_freed(task.status.worker_id)

            if has_finished_tasks:
                break

            time.sleep(self.sleep)

        if should_exit:
            logger.error(
                "'%s' killed by sig %d", exit_info["cmd"], exit_info["return_code"]
            )
