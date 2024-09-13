import os


class SlurmJob:
    def __init__(self, nodelist: str | None = None) -> None:
        self.id: str | None = None
        self.nodelist_raw = nodelist
        self.nodes: list[str] = []
        self._parse_nodelist()

    def load_from_env(self):
        self.id = SlurmJob.get_id()
        self.nodelist_raw = SlurmJob.get_nodelist()
        self._parse_nodelist()

    def _parse_nodelist(self):
        if not self.nodelist_raw:
            return

        entries = []
        in_brackets = False
        working = ""
        for c in self.nodelist_raw:
            if c == "[":
                in_brackets = True
                working += c
            elif c == "]":
                in_brackets = False
                working += c
            elif c == "," and not in_brackets:
                entries.append(working)
                working = ""
            else:
                working += c
        if working:
            entries.append(working)

        for entry in entries:
            if "[" in entry and "]" in entry:
                self.nodes.extend(self._parse_brackets(entry))
            else:
                self.nodes.append(entry)

    def _parse_brackets(self, content: str):
        first_idx = content.index("[")
        last_idx = content.index("]")

        prefix = content[:first_idx]
        bracket_internals = content[first_idx + 1 : last_idx]

        entries = []
        bracket_entries = bracket_internals.split(",")
        for bracket_entry in bracket_entries:
            if "-" in bracket_entry:
                start, end = bracket_entry.split("-")
                for idx in range(int(start), int(end) + 1):
                    entries.append(prefix + str(idx))
            else:
                entries.append(prefix + bracket_entry)
        return entries

    @staticmethod
    def get_id() -> str | None:
        return os.environ.get("SLURM_JOB_ID")

    @staticmethod
    def get_nodelist() -> str | None:
        return os.environ.get("SLURM_JOB_NODELIST")
