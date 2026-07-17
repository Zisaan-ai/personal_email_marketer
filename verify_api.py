import time
import requests
import json

print("Waiting 15 seconds for Passenger to reload...")
time.sleep(15)

endpoints = [
    '/api/ping',
    '/api/test-db',
    '/api/debug-accounts'
]

for ep in endpoints:
    url = f"https://xcomic.xyz{ep}"
    print(f"\nTesting {url}...")
    start_time = time.time()
    try:
        r = requests.get(url, timeout=20)
        elapsed = time.time() - start_time
        print(f"Status: {r.status_code} (took {elapsed:.2f} seconds)")
        if r.status_code == 200:
            print("Response:", r.text[:300])
        else:
            print("Response:", r.text[:300])
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Failed after {elapsed:.2f} seconds: {e}")
