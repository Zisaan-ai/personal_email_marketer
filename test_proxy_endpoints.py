import requests

endpoints = [
    "/api/test-db",
    "/api/sending-accounts"
]

for ep in endpoints:
    url = f"https://xcomic.xyz{ep}"
    print(f"Sending GET request to {url}...")
    try:
        r = requests.get(url, timeout=15)
        print(f"Status Code: {r.status_code}")
        print("Response Content:")
        print(r.text)
    except Exception as e:
        print(f"HTTP Request failed: {e}")
    print("-" * 50)
