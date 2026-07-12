"""Debug live server - test login, campaign send, and schedule"""
import requests
import json
import urllib3
urllib3.disable_warnings()

BASE = "https://xcomic.xyz/api"

# 1. Login
print("=" * 60)
print("1. TESTING LOGIN")
print("=" * 60)
try:
    r = requests.post(f"{BASE}/auth/token", data={
        "username": "zmonemrahman@gmail.com",
        "password": "76008972"
    }, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    
    if r.status_code == 200:
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print(f"\nToken obtained: {token[:20]}...")
    else:
        print("LOGIN FAILED - stopping")
        exit(1)
except Exception as e:
    print(f"Login error: {e}")
    exit(1)

# 2. Check sending accounts
print("\n" + "=" * 60)
print("2. CHECKING SENDING ACCOUNTS")
print("=" * 60)
try:
    r = requests.get(f"{BASE}/sending-accounts", headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        accs = r.json()
        print(f"Total accounts: {len(accs)}")
        for a in accs:
            print(f"  - {a.get('email', '?')} | active={a.get('is_active')} | sent_today={a.get('sent_today', 0)} | daily_limit={a.get('daily_limit', '?')}")
    else:
        print(f"Response: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

# 3. Get existing campaigns
print("\n" + "=" * 60)
print("3. CHECKING EXISTING CAMPAIGNS")
print("=" * 60)
try:
    r = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        camps = r.json()
        print(f"Total campaigns: {len(camps)}")
        for c in camps[:5]:
            print(f"  - ID={c.get('id','?')} | subject={c.get('subject','?')[:30]} | status={c.get('status','?')} | type={c.get('type','?')}")
            print(f"    schedule: days={c.get('sending_days')} start={c.get('start_hour')} end={c.get('end_hour')} tz={c.get('timezone')}")
    else:
        print(f"Response: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")

# 4. Test campaign SEND (cold_mail) - as draft first to be safe
print("\n" + "=" * 60)
print("4. TESTING CAMPAIGN SEND (COLD MAIL - DRAFT)")
print("=" * 60)
payload = {
    "subject": "Debug Test Campaign",
    "body": "<div>This is a debug test</div>",
    "type": "cold_mail",
    "leads": [{"email": "test@example.com", "name": "Test User", "company": "TestCo"}],
    "is_ab_test": False,
    "delay_min": 30,
    "delay_max": 90,
    "is_draft": True,
    "sending_days": json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri"]),
    "start_hour": 9,
    "end_hour": 18,
    "timezone": "Asia/Dhaka"
}

try:
    r = requests.post(f"{BASE}/campaigns/send", headers=headers, json=payload, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    
    if r.status_code == 200:
        data = r.json()
        campaign_id = data.get("campaign_id")
        print(f"\nDraft campaign created with ID: {campaign_id}")
        
        # Now check if schedule was saved
        r2 = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
        if r2.status_code == 200:
            camps = r2.json()
            for c in camps:
                if str(c.get("id")) == str(campaign_id):
                    print(f"\nVerifying saved campaign:")
                    print(f"  subject: {c.get('subject')}")
                    print(f"  status: {c.get('status')}")
                    print(f"  sending_days: {c.get('sending_days')}")
                    print(f"  start_hour: {c.get('start_hour')}")
                    print(f"  end_hour: {c.get('end_hour')}")
                    print(f"  timezone: {c.get('timezone')}")
                    break
    elif r.status_code == 422:
        print(f"\nVALIDATION ERROR - This is likely the bug!")
        print(f"Full error: {r.text}")
except Exception as e:
    print(f"Error: {e}")

# 5. Test actual campaign LAUNCH (not draft)
print("\n" + "=" * 60)
print("5. TESTING CAMPAIGN LAUNCH (NON-DRAFT)")
print("=" * 60)
launch_payload = {
    "subject": "Launch Test Campaign",
    "body": "<div>Launch test body</div>",
    "type": "cold_mail",
    "leads": [{"email": "debugtest@example.com", "name": "Debug", "company": ""}],
    "is_ab_test": False,
    "delay_min": 30,
    "delay_max": 90,
    "is_draft": False,
    "sending_days": json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]),
    "start_hour": 0,
    "end_hour": 24,
    "timezone": "Asia/Dhaka"
}

try:
    r = requests.post(f"{BASE}/campaigns/send", headers=headers, json=launch_payload, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    if r.status_code == 422:
        print(f"\nVALIDATION ERROR DETAILS:")
        print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

# 6. Test save-schedule endpoint
print("\n" + "=" * 60)
print("6. TESTING SAVE SCHEDULE ENDPOINT")
print("=" * 60)
try:
    r = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
    if r.status_code == 200:
        camps = r.json()
        if camps:
            test_id = camps[0]["id"]
            sched_payload = {
                "sending_days": json.dumps(["Mon", "Wed", "Fri"]),
                "start_hour": 10,
                "end_hour": 17,
                "timezone": "Asia/Dhaka"
            }
            r2 = requests.post(f"{BASE}/campaigns/{test_id}/save-schedule", headers=headers, json=sched_payload, timeout=15)
            print(f"Status: {r2.status_code}")
            print(f"Response: {r2.text[:500]}")
            if r2.status_code == 422:
                print(f"\nVALIDATION ERROR DETAILS:")
                print(json.dumps(r2.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

# 7. Test preflight endpoint  
print("\n" + "=" * 60)
print("7. TESTING PREFLIGHT ENDPOINT")
print("=" * 60)
try:
    r = requests.post(f"{BASE}/preflight", headers=headers, json={"subject": "Test", "body": "Hello world"}, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# 8. Server ping
print("\n" + "=" * 60)
print("8. SERVER PING")
print("=" * 60)
try:
    r = requests.get(f"{BASE}/ping", timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
