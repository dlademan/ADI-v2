

class QueueItem:

    def __init__(self, asset_id: int, process: int, status: bool, pos: int):

        self.asset_id = asset_id
        self.process = process
        self.status = status
        self.pos = pos

    def __lt__(self, other):
        return self.pos < other.pos
