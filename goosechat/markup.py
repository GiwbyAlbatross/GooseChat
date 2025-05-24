"manipulating HTML and so on, for GooseChat"
from __future__ import annotations
from .entry import Entry
from os import PathLike

def readfrom(filename: PathLike | str|bytes, **kwargs) -> str:
    with open(filename, 'r', **kwargs) as file:
        return file.read()

def render_basic_template(title, content):
    with open('static/base.template.html') as f:
        return f.read().format(title=title, content=content)

def render_entry(entry: Entry) -> str:
    msg_template = readfrom('static/msg.template.html')
    return msg_template.format(username=entry.user, msg=entry.msg, timestamp=entry.timestamp)

def render_chat(entries: list[Entry]) -> str:
    chat_template = readfrom('static/chat_page.template.html')
    msgs: list[str] = []
    for entry in entries:
        msgs.append(render_entry(entry))
    chat_template.format(chat='<br/>'.join(msgs), chat_from='<pre>chat form goes here </pre>')
    return chat_template
