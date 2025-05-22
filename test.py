from goosechat import entry

e = entry.Entry(3.14159265, 'user4836', 'I exist now')

print(e)
print(e.dump())
print(entry.Entry.load(e.dump()))

assert entry.Entry.load(e.dump()) == e, "load/dump doesn't produce the same result"