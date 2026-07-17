
import urllib.request, time
for _ in range(3):
    s = time.time()
    urllib.request.urlopen('http://127.0.0.1:47300/api/ping')
    print(time.time() - s)
