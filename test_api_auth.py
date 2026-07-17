import urllib.request
import json

try:
    req = urllib.request.Request('https://xcomic.xyz/api/settings', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    print("API SETTINGS:", res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"API HTTP ERROR: {e.code} - {e.reason}")
except Exception as e:
    print("API ERROR:", e)
