# pylint: disable=invalid-name,missing-module-docstring
from __future__ import annotations
from typing import Optional
from threading import Lock
import time
import os

ENTRIES_FILE = os.environ.get('GOOSECHAT_ENTRIES_FILE', './chatlog.txt')
ENTRYFILELOCK= Lock()

class Entry:
    "class representing an entry in the chat log"
    seperator: str='/'
    timestamp: float
    user: str
    msg: str
    def dump(self) -> str:
        "dump this Entry into a string to put in a chat log file"
        return '\n'+self.seperator.join(
            [
                str(self.timestamp),
                self.user,
                self.msg
             ]
        )
    @classmethod
    def load(cls, d: str):
        "create an Entry from a string generated from Entry.dump"
        return cls(*(d.split(cls.seperator, 2)))
    def __init__(self, timestamp: str|float, user: str, msg: str):
        if isinstance(timestamp, str):
            self.timestamp = float(timestamp)
        else:
            self.timestamp = timestamp
        self.user = user
        self.msg  = msg
    def __repr__(self) -> str:
        return f"Entry(timestamp={self.timestamp!r}, user={self.user!r}, msg={self.msg!r})"
    def __eq__(self, other) -> bool:
        return self.timestamp == other.timestamp and \
            self.user == other.user and self.msg == other.msg

def add_msg(msg: str, user: str='guest', timestamp: Optional[float]=None):
    "add a message into the global chat log"
    if timestamp is None:
        timestamp = time.time()
    entry = Entry(timestamp, user, msg)
    with ENTRYFILELOCK:
        with open(ENTRIES_FILE, 'a', encoding='utf-8') as f:
            f.write(entry.dump())
def add_entry(entry: Entry) -> None:
    "add an Entry into the global chat log"
    with ENTRYFILELOCK:
        with open(ENTRIES_FILE, 'a', encoding='utf-8') as f:
            f.write(entry.dump())
    return

def get_entries(chat_id: str='default') -> list[Entry]:
    "get all entries in the global chat log"
    if chat_id != 'default': entryfile = chat_id+'txt'
    else: entryfile = ENTRIES_FILE
    r: list[Entry] = []
    with ENTRYFILELOCK:
        with open(entryfile, encoding='utf-8') as f:
            d = f.read().split('\n')
    for line in d:
        r.append(Entry.load(line))
    return r
