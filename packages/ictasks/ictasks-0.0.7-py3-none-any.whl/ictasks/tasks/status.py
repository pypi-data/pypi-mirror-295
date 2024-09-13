from pathlib import Path

from iccore.serialization import Serializable


def write_file(content, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


class TaskStatus(Serializable):
    def __init__(self) -> None:
        self.state = "created"
        self.return_code: int = 0
        self.walltime: float = 0.0
        self.launch_time: float = 0.0
        self.worker_id: str = ""
        self.host_id: str = ""
        self.pid: int = 0
        self.stdout: list[str] = []
        self.stdout_filename = "task_stdout.txt"
        self.stderr: str = ""

    def is_finished(self) -> bool:
        return self.state == "finished"

    def set_is_finished(self, return_code: int):
        self.state = "finished"
        self.return_code = return_code

    def set_is_running(self):
        self.state = "running"

    def is_running(self) -> bool:
        return self.state == "running"

    def serialize(self) -> dict:
        return {"pid": self.pid,
                "state": self.state,
                "return_code": self.return_code,
                "walltime": self.walltime}

    def read_stdout(self, work_dir: Path, task_id: str):
        with open(
            work_dir / task_id / self.stdout_filename, "r", encoding="utf-8"
        ) as f:
            self.stdout = f.readlines()

    def write_return_code(self, path: Path) -> None:
        write_file(self.return_code, path / "task_return_code.dat")

    def deserialize(self, content: dict) -> None:
        if "return_code" in content:
            self.return_code = content["return_code"]

        if "walltime" in content:
            self.walltime = content["walltime"]

        if "state" in content:
            self.state = content["state"]

        if "pid" in content:
            self.state = content["pid"]
