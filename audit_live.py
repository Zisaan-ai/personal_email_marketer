"""Full website audit - Test EVERY endpoint on live server xcomic.xyz"""
import requests
import json
import time
import urllib3
urllib3.disable_warnings()

BASE = "https://xcomic.xyz/api"
RESULTS = []

def test(name, method, endpoint, **kwargs):
    """Test an endpoint and record result"""
    try:
        url = f"{BASE}{endpoint}"
        start = time.time()
        if method == 'GET':
            r = requests.get(url, headers=headers, timeout=15, **kwargs)
        elif method == 'POST':
            r = requests.post(url, headers=headers, timeout=15, **kwargs)
        elif method == 'DELETE':
            r = requests.delete(url, headers=headers, timeout=15, **kwargs)
        elif method == 'PUT':
            r = requests.put(url, headers=headers, timeout=15, **kwargs)
        elapsed = round((time.time() - start) * 1000)
        
        status = "OK" if r.status_code in [200, 201] else f"FAIL({r.status_code})"
        detail = ""
        try:
            data = r.json()
            if isinstance(data, dict) and 'detail' in data:
                detail = str(data['detail'])[:80]
            elif isinstance(data, list):
                detail = f"returned {len(data)} items"
            elif isinstance(data, dict):
                detail = str({k: str(v)[:30] for k, v in list(data.items())[:3]})
        except:
            detail = r.text[:80]
        
        result = {"name": name, "status": status, "time_ms": elapsed, "detail": detail}
        RESULTS.append(result)
        icon = "[OK]" if "OK" in status else "[FAIL]"
        print(f"  {icon} {name} ({elapsed}ms) - {detail[:60]}")
        return r
    except Exception as e:
        result = {"name": name, "status": f"ERROR", "time_ms": 0, "detail": str(e)[:80]}
        RESULTS.append(result)
        print(f"  [ERR] {name} - {str(e)[:60]}")
        return None

# ============================================================
# 1. LOGIN
# ============================================================
print("=" * 70)
print("1. AUTHENTICATION")
print("=" * 70)

r = requests.post(f"{BASE}/auth/token", data={
    "username": "zmonemrahman@gmail.com",
    "password": "76008972"
}, timeout=15)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print(f"  [OK] Login successful (admin={r.json().get('is_admin')})")

# Test bad login
r2 = requests.post(f"{BASE}/auth/token", data={"username": "bad@email.com", "password": "wrong"}, timeout=15)
icon = "[OK]" if r2.status_code == 401 else "[FAIL]"
print(f"  {icon} Bad login returns {r2.status_code} (expected 401)")
RESULTS.append({"name": "Bad Login Check", "status": "OK" if r2.status_code == 401 else "FAIL", "time_ms": 0, "detail": f"Returns {r2.status_code}"})

# ============================================================
# 2. CORE PAGES
# ============================================================
print("\n" + "=" * 70)
print("2. FRONTEND PAGES")
print("=" * 70)

for page in ['/', '/assets/app.js', '/assets/style.css', '/assets/sending_accounts.js', '/assets/templates.js', '/assets/deliverability_v2.js', '/assets/ai_features.js']:
    try:
        start = time.time()
        r = requests.get(f"https://xcomic.xyz{page}", timeout=15)
        elapsed = round((time.time() - start) * 1000)
        size_kb = round(len(r.text) / 1024, 1)
        status = "OK" if r.status_code == 200 else f"FAIL({r.status_code})"
        icon = "[OK]" if r.status_code == 200 else "[FAIL]"
        print(f"  {icon} {page} ({elapsed}ms, {size_kb}KB)")
        RESULTS.append({"name": f"Page {page}", "status": status, "time_ms": elapsed, "detail": f"{size_kb}KB"})
    except Exception as e:
        print(f"  [ERR] {page} - {e}")
        RESULTS.append({"name": f"Page {page}", "status": "ERROR", "time_ms": 0, "detail": str(e)[:80]})

# ============================================================
# 3. SERVER HEALTH
# ============================================================
print("\n" + "=" * 70)
print("3. SERVER HEALTH")
print("=" * 70)

test("Ping", "GET", "/ping")
test("Test DB", "GET", "/test-db")

# ============================================================
# 4. CAMPAIGNS
# ============================================================
print("\n" + "=" * 70)
print("4. CAMPAIGNS")
print("=" * 70)

r = test("List Campaigns", "GET", "/campaigns")
campaigns = []
if r and r.status_code == 200:
    campaigns = r.json()
    for c in campaigns[:3]:
        print(f"       - {c['subject'][:35]} | status={c['status']} | type={c['type']}")

# Test create draft
test("Create Draft (Cold Mail)", "POST", "/campaigns/send", json={
    "subject": "Audit Test Draft", "body": "<div>test</div>", "type": "cold_mail",
    "leads": [], "is_draft": True,
    "sending_days": json.dumps(["Mon","Tue","Wed"]), "start_hour": 9, "end_hour": 18, "timezone": "Asia/Dhaka"
})

# Test create VB draft
test("Create Draft (Newsletter)", "POST", "/campaigns/send", json={
    "subject": "Audit VB Draft", "body": "<div>test newsletter</div>", "type": "newsletter",
    "leads": [], "is_draft": True,
    "sending_days": json.dumps(["Mon","Fri"]), "start_hour": 10, "end_hour": 17, "timezone": "UTC"
})

# Refresh campaigns
r = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
campaigns = r.json() if r.status_code == 200 else []

# Find the audit drafts
audit_drafts = [c for c in campaigns if 'Audit' in c.get('subject', '')]
for ad in audit_drafts:
    # Test schedule save
    test(f"Save Schedule ({ad['type']})", "POST", f"/campaigns/{ad['id']}/save-schedule", json={
        "sending_days": json.dumps(["Sat","Sun"]), "start_hour": 14, "end_hour": 22, "timezone": "Asia/Dhaka"
    })
    
    # Verify schedule persisted
    r2 = requests.get(f"{BASE}/campaigns", headers=headers, timeout=15)
    if r2.status_code == 200:
        c2 = next((c for c in r2.json() if c['id'] == ad['id']), None)
        if c2:
            saved_ok = c2.get('sending_days') == json.dumps(["Sat","Sun"])
            icon = "[OK]" if saved_ok else "[FAIL]"
            print(f"  {icon} Schedule Persist Check ({ad['type']}) - days={c2.get('sending_days')}")
            RESULTS.append({"name": f"Schedule Persist ({ad['type']})", "status": "OK" if saved_ok else "FAIL", "time_ms": 0, "detail": f"days={c2.get('sending_days')}"})

    # Test get leads
    test(f"Get Leads ({ad['type']})", "GET", f"/campaigns/{ad['id']}/leads")
    
    # Test pause
    test(f"Pause Campaign ({ad['type']})", "POST", f"/campaigns/{ad['id']}/pause")
    
    # Test resume
    test(f"Resume Campaign ({ad['type']})", "POST", f"/campaigns/{ad['id']}/resume")
    
    # Clean up
    test(f"Delete Campaign ({ad['type']})", "DELETE", f"/campaigns/{ad['id']}")

# Test launch with exhausted limits
test("Launch with Full Limits", "POST", "/campaigns/send", json={
    "subject": "Limit Check", "body": "<div>test</div>", "type": "cold_mail",
    "leads": [{"email": "test@test.com", "name": "Test", "company": ""}],
    "is_draft": False,
    "sending_days": json.dumps(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),
    "start_hour": 0, "end_hour": 24, "timezone": "UTC"
})

# ============================================================
# 5. SENDING ACCOUNTS
# ============================================================
print("\n" + "=" * 70)
print("5. SENDING ACCOUNTS")
print("=" * 70)

r = test("List Sending Accounts", "GET", "/sending-accounts")
if r and r.status_code == 200:
    accs = r.json()
    for a in accs:
        print(f"       - {a['email']} | active={a['is_active']} | sent={a.get('sent_today',0)}/{a.get('daily_limit','?')}")
        
        # Test account health
        test(f"Account Health ({a['email'][:20]})", "GET", f"/account-health/{a['id']}")
        
        # Test account stats
        test(f"Account Stats ({a['email'][:20]})", "GET", f"/account-stats/{a['id']}")

# Test all domain health
test("All Domains Health", "GET", "/domain-health-all")

# Test all accounts health
test("All Accounts Health", "GET", "/account-health-all")

# ============================================================
# 6. AI FEATURES
# ============================================================
print("\n" + "=" * 70)
print("6. AI FEATURES")
print("=" * 70)

test("AI Chat", "POST", "/ai/chat", json={"message": "Hello, what can you do?"})
test("AI Generate Email", "POST", "/ai/generate", json={"prompt": "Write a cold email for SaaS product", "tone": "professional"})
test("AI Optimize Subject", "POST", "/ai/optimize-subject", json={"subject": "Check out our product"})
test("AI Generate Icebreakers", "POST", "/ai/generate-icebreakers", json={"leads_csv": "Email,Name,Company\njohn@example.com,John,Acme Corp"})

# ============================================================
# 7. PREFLIGHT & DELIVERABILITY
# ============================================================
print("\n" + "=" * 70)
print("7. PREFLIGHT & DELIVERABILITY")
print("=" * 70)

test("Preflight Check", "POST", "/preflight", json={"subject": "Test Subject", "body": "Hello this is a test email with good content and no spam words"})
test("Spam Score Check", "POST", "/spam-check", json={"subject": "FREE MONEY NOW!!!", "content": "Click here to claim your prize! Buy now! Limited offer!"})

# ============================================================
# 8. LEADS VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("8. LEADS VALIDATION")
print("=" * 70)

test("Validate Leads", "POST", "/validate-leads", json={"emails": ["test@gmail.com", "fake@nonexistentdomain12345.com"]})
test("Clean Inactive Leads", "POST", "/clean-inactive-leads")

# ============================================================
# 9. SETTINGS
# ============================================================
print("\n" + "=" * 70)
print("9. SETTINGS")
print("=" * 70)

test("Get Settings", "GET", "/settings")

# ============================================================
# 10. BOUNCES, UNSUBSCRIBES, REPLIES
# ============================================================
print("\n" + "=" * 70)
print("10. BOUNCES, UNSUBSCRIBES, REPLIES")
print("=" * 70)

test("Get Bounces", "GET", "/bounces")
test("Get Unsubscribes", "GET", "/unsubscribes")
test("Get Replies", "GET", "/replies")

# ============================================================
# 11. WEBHOOKS
# ============================================================
print("\n" + "=" * 70)
print("11. WEBHOOKS")
print("=" * 70)

test("Get Webhook", "GET", "/webhook")

# ============================================================
# 12. ADMIN
# ============================================================
print("\n" + "=" * 70)
print("12. ADMIN")
print("=" * 70)

test("List All Users (Admin)", "GET", "/admin/users")

# ============================================================
# 13. GALLERY
# ============================================================
print("\n" + "=" * 70)
print("13. GALLERY")
print("=" * 70)

test("Get Gallery", "GET", "/gallery")

# ============================================================
# 14. PERFORMANCE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("14. PERFORMANCE ANALYSIS")
print("=" * 70)

slow_endpoints = [r for r in RESULTS if r.get('time_ms', 0) > 2000]
failed_endpoints = [r for r in RESULTS if 'FAIL' in r.get('status', '') or 'ERROR' in r.get('status', '')]

print(f"\n  Total endpoints tested: {len(RESULTS)}")
print(f"  Passed: {len([r for r in RESULTS if 'OK' in r.get('status', '')])}")
print(f"  Failed: {len(failed_endpoints)}")
print(f"  Slow (>2s): {len(slow_endpoints)}")

if failed_endpoints:
    print(f"\n  FAILED ENDPOINTS:")
    for f in failed_endpoints:
        print(f"    - {f['name']}: {f['status']} - {f['detail']}")

if slow_endpoints:
    print(f"\n  SLOW ENDPOINTS (>2s):")
    for s in slow_endpoints:
        print(f"    - {s['name']}: {s['time_ms']}ms")

# Sort by time
by_time = sorted(RESULTS, key=lambda x: x.get('time_ms', 0), reverse=True)
print(f"\n  TOP 5 SLOWEST:")
for r in by_time[:5]:
    print(f"    - {r['name']}: {r['time_ms']}ms")

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)

# Save results
with open('audit_results.json', 'w') as f:
    json.dump(RESULTS, f, indent=2)
print("Results saved to audit_results.json")
