import requests
import time

print("Waiting 15 seconds for passenger restart...")
time.sleep(15)

url = "https://xcomic.xyz/"
print(f"Requesting {url}...")
try:
    r = requests.get(url, timeout=15)
    print(f"Status: {r.status_code}")
    print("=== Response Content ===")
    print(r.text)
    print("========================")
except Exception as e:
    print(f"Request failed: {e}")
