" authentication routines for GooseChat "
from dataclasses import dataclass
from threading import Lock, Thread
from enum import Enum
import secrets
import hashlib
import base64
import time
import os

PASSWD_PATH = os.environ.get("GOOSECHAT_PASSWD", 'goosechat.shadow.passwd')
PASSWD_LOCK = Lock()

if not os.path.exists(PASSWD_PATH):
    with open(PASSWD_PATH, 'x'): pass # create the file

class EnumPasswdUpdateStatus(Enum):
    FAIL = 0
    CHANGE = 1
    ADDUSR = 2
@dataclass
class AuthCodeEntry:
    user: str
    code: bytes
    expiry: float
class AuthCodeManager:
    db: dict[str, AuthCodeEntry]
    db_lock: Lock
    def __init__(self):
        self.db = {}
        self.db_lock = Lock()
    def is_valid(self, usr: str, authcode: bytes) -> bool:
        with self.db_lock:
            if usr not in self.db:
                return False
            code_entry = self.db[usr]
        return secrets.compare_digest(code_entry.code, authcode)
        #raise NotImplementedError
    def get_code(self, usr: str) -> bytes:
        with self.db_lock:
            if usr in self.db:
                code_entry = self.db[usr]
                code_entry.expiry += 60*15
        code_entry = AuthCodeEntry(usr, self._generate_code(), time.time()+3600)
        with self.db_lock: self.db[usr] = code_entry
        return code_entry.code
    def _generate_code(self):
        return secrets.token_bytes(48)
    def _expiry_thread(self):
        while 1:
            time.sleep(60)
            print("Checking for expired authcodes")
            with self.db_lock:
                for usr, entry in self.db.items():
                    if entry.expiry > time.time():
                        print("Deleting authcode:", repr(entry))
                        del self.db[usr]

def get_passdb() -> dict[str, bytes]:
    r: dict[str, bytes]={}
    with PASSWD_LOCK:
        with open(PASSWD_PATH, 'r', encoding='ascii') as passwd_file:
            d = passwd_file.read()
        if d == '': return {}
        else: d = d.split('\n')
        r1: dict[str, str] = {}
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
    passdb = get_passdb()
    if usr in passdb:
        if secrets.compare_digest(passdb[usr], passwd):
            r = True
    return r

def encodepass(passwd: str) -> bytes:
    " this will hash the password "
    #return passwd.encode('ascii')
    return hashlib.sha3_384(passwd.encode('utf-16')).digest()

authcodemanager = AuthCodeManager()

def start_entry_timeout_thread() -> Thread:
    "starts the thread which looks after expiring authcodes"
    r = Thread(target=authcodemanager._expiry_thread, name="authcodemanager_expiry-thread")
    r.start()
    return r

def is_legit(cookies) -> bool:
    " is this the correct cookie set to be legit. Will be different when we have proper auth going on "
    #return _parsebool(cookies.get('legit', 'false'))
    username = cookies.get('username', 'guest')
    if username == 'guest': return False
    cookie_authcode = base64.b64decode(cookies.get('goosechat-authcode',
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
    return authcodemanager.is_valid(username, cookie_authcode)
