import urllib.request
import json
import time

try:
    req = urllib.request.Request('https://xcomic.xyz/api/settings', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    print("API SETTINGS:", res.read().decode('utf-8'))
except Exception as e:
    print("API SETTINGS ERROR:", e)
