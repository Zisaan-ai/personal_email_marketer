import urllib.request
import json
import time

time.sleep(3) # Wait for passenger restart

try:
    req = urllib.request.Request('https://xcomic.xyz/api/ping', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    print("API PING:", res.read().decode('utf-8'))
except Exception as e:
    print("API PING ERROR:", e)
