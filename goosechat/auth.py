" authentication routines for GooseChat "
from threading import Lock
from enum import Enum
import secrets
import hashlib
import base64
import os

PASSWD_PATH = os.environ.get("GOOSECHAT_PASSWD", 'goosechat.shadow.passwd')
PASSWD_LOCK = Lock()

def _parsebool(s: str) -> bool:
    s = s.lower()
    if s == 'true':
        return True
    return False

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
            d = passwd_file.read()
        if d == '': return {}
        else: d = d.split('\n')
        r1 = {}
        for line in d:
            splitline = line.split(':', 1)
            r1[splitline[0]] = splitline[1]
        for usr in r1:
            r[usr] = base64.b64decode(r1[usr])
    return r

def add_pass(usr: str, passwd: bytes) -> EnumPasswdUpdateStatus:
    if usr in get_passdb():
        ... # later
        return EnumPasswdUpdateStatus.CHANGE # meaning fail in this case
    with PASSWD_LOCK:
        try:
            with open(PASSWD_PATH, 'a', encoding='ascii') as passwd_file:
                passwd_file.write('\n' + (':'.join([usr,
                                           base64.b64encode(passwd).decode()]
                                       )))
        except Exception as e: raise e
        else:
            return EnumPasswdUpdateStatus.ADDUSR
    #except Exception as e:
    #    print(e); return EnumPasswdUpdateStatus.FAIL

def check_pass(usr: str, passwd: bytes) -> bool:
    r = False
    #with PASSWD_LOCK:
    if 1:
        passdb = get_passdb()
        if usr in passdb:
            if passdb[usr] == passwd:
                r = True
    return r

def encodepass(passwd: str) -> bytes:
    " in future, this will hash the password, but anyway "
    #return passwd.encode('ascii')
    return hashlib.sha3_384(passwd.encode('utf-16')).digest()

def is_legit(cookies) -> bool:
    " is this the correct cookie set to be legit. Will be different when we have proper auth going on "
    return _parsebool(cookies.get('legit', 'false'))
