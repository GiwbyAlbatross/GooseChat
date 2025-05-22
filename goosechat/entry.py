import time

class Entry:
    seperator: str='/'
    timestamp: float
    user: str
    msg: str
    def dump(self) -> str:
        return self.seperator.join(
            [
                str(self.timestamp),
                self.user,
                self.msg
             ]
        )
    @classmethod
    def load(cls, d: str):
        return cls(*(d.split(cls.seperator, 2)))
    def __init__(self, timestamp: str|float, user: str, msg: str):
        if isinstance(timestamp, str): self.timestamp = float(timestamp)
        else: self.timestamp = timestamp
        self.user = user
        self.msg  = msg
