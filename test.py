#!/usr/bin/env -S python3 -m pytest
from goosechat import entry

def test_entry_load_dump():
    e = entry.Entry(739294728402847481.4828472,
                    'reallyAmazingUsername2014',
                    'I am a person with a really amazing username. I have a / in my message!')
    assert entry.Entry.load(e.dump()) == e, "load/dump doesn't produce the same result"