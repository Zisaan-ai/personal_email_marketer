import urllib.request
import urllib.error
import json
import time

URL = "https://xcomic.xyz"
# Or if it requires API prefix
API_URL = URL + "/api"

def login():
    req = urllib.request.Request(API_URL + "/auth/token", method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    body = "username=zmonemrahman@gmail.com&password=76008972"
    with urllib.request.urlopen(req, data=body.encode(), timeout=5) as res:
        data = json.loads(res.read())
        return data["access_token"]

def measure(name, endpoint, token):
    req = urllib.request.Request(API_URL + endpoint)
    req.add_header("Authorization", "Bearer " + token)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            res.read()
            status = res.status
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception as e:
        status = str(e)
    end = time.time()
    print(f"{name:25} | {status} | {(end - start) * 1000:.2f} ms")

try:
    print("Logging in...")
    token = login()
    print("Testing endpoints...")
    measure("Campaigns", "/campaigns", token)
    measure("Bounces", "/bounces", token)
    measure("Replies", "/replies", token)
    measure("Account Health", "/account-health-all", token)
    measure("Domain Health", "/domain-health-all", token)
    measure("Sending Accounts", "/sending-accounts", token)
except Exception as e:
    print("Error:", e)
