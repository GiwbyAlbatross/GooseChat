# pylint: disable=invalid-name,missing-module-docstring
from __future__ import annotations
from . import ChatNotFoundError
from typing import Optional
from threading import Lock
import time
import os

ENTRIES_FILE = os.environ.get('GOOSECHAT_ENTRIES_FILE', './chatlog.txt')
ENTRYFILELOCK= Lock()
try: os.mkdir('chats')
except OSError: pass

def _cleancrlf(s: str) -> str:
    r = ""
    for i, c in enumerate(s):
        if c == '\n' and s[i-1] == '\r':
            r += "<br/>"
        elif c != '\r':
            r += c
    return r

class Entry:
    "class representing an entry in the chat log"
    seperator: str='/'
    timestamp: float
    legit: bool
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
        ) + ('^' if self.legit else '~')
    @classmethod
    def load(cls, d: str):
        "create an Entry from a string generated from Entry.dump"
        try:
            d1 = d[:-1]
            d2 = d[-1]
        except IndexError as e:
            print(f"IndexError: with values d: {d!r}, d1: {d1!r}")
            raise e
        if d2 not in {'~', '^'}:
            d1 += d2
        #print("d1:", d1, "d2:",d2)
        timestamp, usr, msg = d1.split(cls.seperator, 2)
        return cls(timestamp, usr, msg, legit=(d2=='^'))
    def __init__(self, timestamp: str|float, user: str, msg: str, legit=False):
        if isinstance(timestamp, str):
            self.timestamp = float(timestamp)
        else:
            self.timestamp = timestamp
        self.legit = legit
        self.user = user
        self.msg  = msg
    def __repr__(self) -> str:
        return f"Entry(timestamp={self.timestamp!r}, user={self.user!r}, msg={self.msg!r}, legit={self.legit!r})"
    def __eq__(self, other) -> bool:
        return self.timestamp == other.timestamp and \
            self.user == other.user and self.msg == other.msg\
            and self.legit == other.legit

def add_msg(msg: str, user: str='guest', timestamp: Optional[float]=None, legit: Optional[bool]=None, chat_id='default'):
    "add a message into the global chat log"
    if chat_id != 'default': entryfile = os.path.join('chats', chat_id+'.txt')
    else: entryfile = ENTRIES_FILE
    if timestamp is None:
        timestamp = time.time()
    entry = Entry(timestamp, user, _cleancrlf(msg), legit)
    with ENTRYFILELOCK:
        with open(entryfile, 'a', encoding='utf-8') as f:
            f.write(entry.dump())
def add_entry(entry: Entry, chat_id='default') -> None:
    "add an Entry into the global chat log"
    if chat_id != 'default': entryfile = os.path.join('chats', chat_id+'.txt')
    else: entryfile = ENTRIES_FILE
    with ENTRYFILELOCK:
        with open(entryfile, 'a', encoding='utf-8') as f:
            f.write(entry.dump())
    return

def get_entries(chat_id: str='default') -> list[Entry]:
    "get all entries in the global chat log"
    if chat_id != 'default': entryfile = os.path.join('chats', chat_id+'.txt')
    else: entryfile = ENTRIES_FILE
    r: list[Entry] = []
    with ENTRYFILELOCK:
        try:
            with open(entryfile, encoding='utf-8') as f:
                d = f.read().strip('\n').split('\n')
        except FileNotFoundError as e:
            raise ChatNotFoundError(entryfile)
    for line in d:
        #if line == '': continue # old solution, idk if it works or not
        try: r.append(Entry.load(line))
        except IndexError: pass # skip malformed entries entirely
    return r
