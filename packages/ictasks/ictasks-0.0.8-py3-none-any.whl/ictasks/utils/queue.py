class Queue:
    def __init__(self) -> None:
        self.ids: list = []

    def pop(self):
        first_id = self.ids[0]
        del self.ids[0]
        return first_id

    def available(self):
        return len(self.ids) != 0

    def push(self, next_id):
        self.ids.append(next_id)
