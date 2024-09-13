"""
This module has stopping conditions for tasks
"""

from pathlib import Path
import sys
import os
import logging

logger = logging.getLogger(__name__)


class StoppingCondition:
    """
    This condition stops processing if a particular file
    is found with a predefined phrase.
    """

    def __init__(self, stopfile: Path | None = None, stopmagic: str = "") -> None:
        self.stopmagic = stopmagic
        self.stopfile = stopfile

    def check_magic(self, path: Path) -> bool:
        """
        Is the magic phrase found in the file?
        """
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if self.stopmagic in line:
                    return True
        return False

    def eval(self, path: Path):
        """
        Stop processing if the stop condition is hit
        """
        if not self.stopfile:
            return

        stopfile_path = path / self.stopfile

        if os.path.exists(stopfile_path) and self.stopmagic == "":
            logger.info("Exit because stop-file %s is present.", stopfile_path)
            sys.exit(1)

        if os.path.exists(stopfile_path) and self.check_magic(stopfile_path):
            logger.info(
                "Exit because file %s contains magic %s", stopfile_path, self.stopmagic
            )
            sys.exit(1)
