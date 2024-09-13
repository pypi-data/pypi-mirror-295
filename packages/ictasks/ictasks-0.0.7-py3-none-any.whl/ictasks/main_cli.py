"""
Main entry point for ictasks
"""

import os
from pathlib import Path
import sys
import signal
import argparse
import logging

from iccore import logging_utils
from iccore.serialization import read_yaml

from ictasks.session import Session
from ictasks.environment import Environment, SlurmEnvironment, BasicEnvironment
from ictasks.settings import TaskfarmSettings
from ictasks.worker_collection import WorkerCollection
from ictasks.tasks import (
    Task,
    TaskCollection,
    TaskLauncher,
    SubprocessTaskLauncher,
    MpiTaskLauncher,
)

logger = logging.getLogger(__name__)


def on_sig_int(*_):
    """
    Signal handler for SIGINT
    """

    logger.info("Session interrupted by SIGINT. Please check for orphaned processes.")
    sys.exit(1)


def taskfarm(args):

    logging_utils.setup_default_logger()

    signal.signal(signal.SIGINT, on_sig_int)

    settings = TaskfarmSettings()
    config_environment = {}
    config_tasks = {}
    if args.config.resolve().exists():
        config = read_yaml(args.config.resolve())
        if "environment" in config:
            config_environment = config["environment"]
            config_tasks = config["tasks"]

    cores_per_node = settings.get_cores_per_node()
    processes_per_node = settings.processes_per_node
    if "workers" in config_environment:
        if "cores_per_node" in config_environment["workers"]:
            cores_per_node = config_environment["workers"]["cores_per_node"]
            processes_per_node = cores_per_node
    workers = WorkerCollection(cores_per_node, processes_per_node)

    logger.info("Setting up runtime environment")
    if args.env == "slurm":
        logger.info("Running in slurm environment")
        env: Environment = SlurmEnvironment(workers)
        launcher: TaskLauncher = MpiTaskLauncher(
            settings.get("launcher"), settings.cores_per_task
        )
    elif args.env == "basic":
        logger.info("Running in basic environment")
        env = BasicEnvironment(workers, args.job_id, args.nodelist.split(","))
        launcher = SubprocessTaskLauncher()
    elif SlurmEnvironment.detect():
        logger.info("Detected slurm environment")
        env = SlurmEnvironment(workers)
        launcher = MpiTaskLauncher(settings.get("launcher"), settings.cores_per_task)
        launcher: TaskLauncher = MpiTaskLauncher(
            settings.get("launcher"), settings.cores_per_task
        )
    else:
        logger.info(
            "No environment given and Slurm not detected. "
            "Defaulting to basic runtime environment"
        )
        env = BasicEnvironment(workers, args.job_id, args.nodelist.split(","))
        launcher = SubprocessTaskLauncher()

    logger.info("Setting up tasks")
    tasks = TaskCollection(args.work_dir.resolve(), settings.get("group_size"))
    if config_tasks:
        tasks_from_config = []
        for each_task in config_tasks["items"]:
            tasks_from_config.append(Task(each_task["id"], each_task["launch_cmd"]))
        tasks.add_tasks(tasks_from_config)
    else:
        tasks.read_taskfile(args.tasklist.resolve())

    session = Session(tasks, env, launcher, settings.get("sleep"))
    logger.info("Starting session run")
    session.run()
    logger.info("Finished session run")


def main_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    taskfarm_parser = subparsers.add_parser("taskfarm")

    taskfarm_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory to run the session in",
    )
    taskfarm_parser.add_argument("--tasklist", type=Path, help="Path to tasklist file")
    taskfarm_parser.add_argument("--config", type=Path, help="Path to a config file")
    taskfarm_parser.add_argument(
        "--nodelist", type=str, default="", help="List of system nodes to use"
    )
    taskfarm_parser.add_argument(
        "--job_id", type=str, default="", help="Identifier for this job"
    )
    taskfarm_parser.add_argument(
        "--env",
        type=str,
        default=" ",
        help="Environment to run the session in, 'slurm' or 'basic'",
    )

    taskfarm_parser.set_defaults(func=taskfarm)
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main_cli()
