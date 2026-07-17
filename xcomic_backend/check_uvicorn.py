
import socket
import urllib.request

try:
    s = socket.socket()
    s.connect(('127.0.0.1', 47300))
    s.close()
    print('Port 47300 is OPEN')
except Exception as e:
    print('Port 47300 is CLOSED:', e)

try:
    req = urllib.request.Request('http://127.0.0.1:47300/api/ping')
    with urllib.request.urlopen(req, timeout=5) as r:
        print('Ping HTTP OK:', r.getcode(), r.read())
except Exception as e:
    print('Ping HTTP FAIL:', e)
