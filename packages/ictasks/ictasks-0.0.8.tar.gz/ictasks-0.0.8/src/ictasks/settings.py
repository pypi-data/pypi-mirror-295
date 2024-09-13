"""
This module has taskfarm settings
"""

import sys
import logging

from icsystemutils.cpu.cpu_info import CpuInfo
from .utils.environment import env_read


logger = logging.getLogger(__name__)


class Setting:
    """
    This is a single setting value, including things like a default,
    type and description
    """

    def __init__(self, name, default, key, description, setting_type) -> None:
        self.name = name
        self.default = default
        self.key = key
        self.setting_type = setting_type
        self.description = description
        self.value = default

    def read_from_env(self):
        self.value = env_read(self.key, self.default, self.setting_type)


TASKFARM_DEFAULT_SETTINGS = [
    Setting(
        "sleep",
        0.5,
        "TASKFARM_SLEEP",
        "How long to sleep between task end checks",
        float,
    ),
    Setting(
        "launcher",
        "mpirun",
        "TASKFARM_MPI_LAUNCHER",
        "Base launch command for tasks",
        str,
    ),
    Setting(
        "stopfile",
        "abandon",
        "TASKFARM_STOPFILE",
        "Stop the run if this is present and empty or has stopmagic",
        str,
    ),
    Setting(
        "stopmagic",
        "",
        "TASKFARM_STOPMAGIC",
        "Stop the run if this is present in the stopfile",
        str,
    ),
    Setting("group_size", 1, "TASKFARM_GROUP", "Group tasks into this size", int),
    Setting(
        "keep",
        "",
        "TASKFARM_KEEP",
        "Whether to keep old tasks in the list",
        bool,
    ),
    Setting(
        "use_smt",
        None,
        "TASKFARM_SMT",
        "If set use simulataneous multithreading ",
        None,
    ),
    Setting(
        "silent",
        None,
        "TASKFARM_SILENT",
        "If set don't produce informational logging ",
        None,
    ),
    Setting("ppn", None, "TASKFARM_PPN", "Number of processes per node", int),
    Setting("cores_per_task", 1, "TASKFARM_MPI", "Number of cores per task", int),
]


class TaskfarmSettings:
    def __init__(self) -> None:
        """
        This class holds and reads settings for taskfarm
        functionality
        """

        self.log_level = "info"
        self.threads_per_core = 1
        self.cores_per_task = 1

        self.cpu_info = CpuInfo()
        self.processes_per_node = self.get_threads_per_node()

        self.settings = {}
        for setting in TASKFARM_DEFAULT_SETTINGS:
            self.settings[setting.name] = setting

    def read_from_environment(self):
        for name, setting in self.settings.items():
            setting.read_from_env()
            self.settings[name] = setting

        if self.get("silent"):
            self.log_level = "error"

        if self.get("use_smt"):
            self.threads_per_core = self.cpu_info.threads_per_core

        if self.get("ppn"):
            self.processes_per_node = self.get("ppn")
        else:
            self.processes_per_node = self.get_threads_per_node()

        if self.get("cores_per_task") > 1:
            ppn = self.processes_per_node
            self.cores_per_task = self.get_cores_per_node() / ppn

        self.validate()

    def get_threads_per_node(self):
        return self.get_cores_per_node() * self.threads_per_core

    def get(self, name):
        if name in self.settings:
            return self.settings[name].value
        return None

    def set(self, name, value):
        if name in self.settings:
            self.settings[name].value = value

    def get_cores_per_node(self):
        return self.cpu_info.cores_per_node

    def validate(self):
        msg_prefix = "Error: $TASKFARM_PPN must"

        cores_per_node = self.get_cores_per_node()
        threads_per_node = self.get_threads_per_node()

        more_procs_than_threads = self.processes_per_node > threads_per_node
        more_procs_than_cores = self.processes_per_node > cores_per_node
        if self.threads_per_core > 1 and more_procs_than_threads:
            logger.error(
                "%s not exceed %d ppn when $TASKFARM_SMT is set.",
                msg_prefix,
                threads_per_node,
            )
            sys.exit(1)
        elif self.threads_per_core == 1 and more_procs_than_cores:
            logger.error("%s not exceed %d ppn.", msg_prefix, cores_per_node)
            sys.exit(1)
        elif self.processes_per_node < 1:
            logger.error("%s request one or more processes per node.", msg_prefix)
            sys.exit(1)
