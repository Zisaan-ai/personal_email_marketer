import requests
import time
import json

def test_api():
    # 1. Login
    session = requests.Session()
    print("Logging in...")
    res = session.post("https://xcomic.xyz/api/auth/token", data={
        "username": "mzisan367@gmail.com",
        "password": "password"
    })
    print("Login response:", res.status_code, res.text)
    if res.status_code != 200:
        return
    token = res.json()["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    
    # 2. Create campaign
    print("Sending campaign...")
    start_time = time.time()
    payload = {
        "name": "API Test Campaign",
        "subject": "Test Subject API",
        "body": "Test Body API",
        "accounts": ["test"],  # Assuming we can just pass anything if it's draft or not validated strongly
        "leads": [
            {"email": "test1@example.com"},
            {"email": "test2@example.com"},
            {"email": "test3@example.com"},
        ],
        "is_draft": False
    }
    res = session.post("https://xcomic.xyz/api/campaigns/send", json=payload)
    end_time = time.time()
    
    print("Campaign response:", res.status_code, res.text)
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    test_api()
