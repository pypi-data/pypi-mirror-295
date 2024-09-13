"""
This module has functionality for reading taskfarm files
"""

from pathlib import Path
import logging
import re

from .task import Task


logger = logging.getLogger(__name__)


class TaskfarmFile:
    def __init__(self, work_dir: Path, group_size: int = 1):
        self.work_dir = work_dir
        self.group_size = group_size

    def append_workdir(self, line: str) -> str:
        if line[-1] != ";":
            line += ";"
        return line + " cd " + str(self.work_dir)

    def process_line(self, line: str) -> str:
        if self.has_grouped_tasks():
            return self.append_workdir(line)
        return line

    def extract_paths(self, line: str):
        np = re.search(r"^cd (\w+)", line)
        if np is None:
            np = re.search(r"^pushd (\w+)", line)
        if np is None:
            return ""
        return np.groups()[0]

    def has_grouped_tasks(self) -> bool:
        return self.group_size != 1

    def load(self, content: str):
        logger.info("Setting up tasks")
        template_lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped:
                template_lines.append(self.process_line(stripped))

        lines = [
            template_lines[i].replace("%TASKFARM_TASKNUM%", str(i))
            for i in range(len(template_lines))
        ]

        num_grouped_tasks = 0
        tasks = []
        if self.has_grouped_tasks():
            num_grouped_tasks = len(lines)
            num_groups = num_grouped_tasks // self.group_size + 1
            gs = self.group_size
            commands = filter(
                None,
                [" && ".join(lines[i * gs : (i + 1) * gs]) for i in range(num_groups)],
            )
            for idx, cmd in enumerate(commands):
                tasks.append(Task(str(idx), cmd))
        else:
            for idx, cmd in enumerate(lines):
                tasks.append(Task(str(idx), cmd, self.extract_paths(cmd)))

        logger.info("Set up %d tasks", len(tasks))
        return num_grouped_tasks, tasks

    def read(self, path: Path):
        logger.info("Reading tasks from: %s", path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return self.load(f.read())
        except Exception as e:
            msg = f"Error opening task file {path} with {e}."
            logger.error(msg)
            raise e
