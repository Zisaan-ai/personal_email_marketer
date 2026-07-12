"""Fix stuck campaigns on live server"""
import requests
import json
import urllib3
urllib3.disable_warnings()

BASE = "https://xcomic.xyz/api"

# Login
r = requests.post(f"{BASE}/auth/token", data={
    "username": "zmonemrahman@gmail.com",
    "password": "76008972"
}, timeout=15)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print("Logged in OK")

# Get all campaigns
r = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
camps = r.json()

# Find stuck processing campaigns
stuck = [c for c in camps if c['status'] == 'processing']
print(f"\nFound {len(stuck)} stuck 'processing' campaigns:")
for c in stuck:
    print(f"  - ID={c['id']} | subject={c['subject'][:40]} | type={c['type']}")

# Also find debug test campaigns to clean up
debug_camps = [c for c in camps if 'Debug Test' in c.get('subject', '') or 'Launch Test' in c.get('subject', '')]
print(f"\nFound {len(debug_camps)} debug test campaigns to delete:")
for c in debug_camps:
    print(f"  - ID={c['id']} | subject={c['subject']}")
    r = requests.delete(f"{BASE}/campaigns/{c['id']}", headers=headers, timeout=15)
    print(f"    Deleted: {r.status_code}")

# For stuck campaigns, pause them first
for c in stuck:
    print(f"\nPausing stuck campaign {c['id']}...")
    r = requests.post(f"{BASE}/campaigns/{c['id']}/pause", headers=headers, timeout=15)
    print(f"  Pause result: {r.status_code} - {r.text[:100]}")

print("\nDone! Stuck campaigns have been paused.")
print("After deploying the fix, they won't get stuck anymore.")
