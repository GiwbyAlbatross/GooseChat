from typing import Optional
import time
import os

ENTRIES_FILE = os.environ.get('GOOSECHAT_ENTRIES_FILE', './chatlog.txt')

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

def add_msg(msg: str, user: str='guest', timestamp: Optional[float]=None):
    if timestamp is None:
        timestamp = time.time()
    entry = Entry(timestamp, user, msg)
    with open(ENTRIES_FILE, 'a') as f:
        f.write(entry.dump())
def add_entry(entry: Entry):
    with open(ENTRIES_FILE, 'a') as f:
        f.write(entry.dump())