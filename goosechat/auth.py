" authentication routines for GooseChat "
from threading import Lock
from enum import Enum
import hashlib
import base64
import os

PASSWD_PATH = os.environ("GOOSECHAT_PASSWD", 'goosechat.passwd')
PASSWD_LOCK = Lock()

if not os.path.exists(PASSWD_PATH):
    with open(PASSWD_PATH, 'x'): pass # create the file

class EnumPasswdUpdateStatus(Enum):
    FAIL = 0
    CHANGE = 1
    ADDUSR = 2

def get_passdb() -> dict[str, bytes]:
    with PASSWD_LOCK:
        r = {}
        with open(PASSWD_PATH, 'r', encoding='ascii') as passwd_file:
            d = passwd_file.read().split('\n')
        r1 = {}
        for line in d:
            splitline = line.split(':', 1)
            r1[splitline[0]] = splitline[1]
        for usr in r1:
            r[usr] = base64.b64decode(r1[usr])
    return r

def add_pass(usr: str, passwd: bytes) -> EnumPasswdUpdateStatus:
    with PASSWD_LOCK:
        if usr in get_passdb():
            ... # later
            return EnumPasswdUpdateStatus.CHANGE # meaning fail in this case
        try:
            with open(PASSWD_PATH, 'a', encoding='ascii') as passwd_file:
                passwd_file.write(':'.join(usr,
                                           base64.b64encode(passwd).decode()
                                       ))
        else:
            return EnumPasswdUpdateStatus.ADDUSR
        #except Exception as e:
        #    print(e); return EnumPasswdUpdateStatus.FAIL

def check_pass(usr: str, passwd: bytes) -> bool:
    with PASSWD_LOCK:
        passdb = get_passdb()
        if usr in passdb:
            if passdb[usr] == passwd:
                return True
    return False

def encodepass(passwd: str) -> bytes:
    " in future, this will hash the password, but anyway "
    return passwd.encode('ascii')
