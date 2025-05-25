from os import system, fork

for _ in range(4): fork()

while 1: system('curl -X POST http://127.0.0.1:5000/chat/spam/ -H "Content-Type: application/x-www-form-urlencoded" '+
                '-d "msg=checkitout"')