import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://xcomic.xyz'

# Step 1: Login
print('[1] Logging in...')
form_data = urllib.parse.urlencode({
    'username': 'zmonemrahman@gmail.com',
    'password': '76008972'
}).encode()

token = None
try:
    req = urllib.request.Request(
        BASE + '/api/auth/token',
        data=form_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        token = data.get('access_token')
        print('[OK] Token acquired:', token[:40] if token else 'NONE')
except urllib.error.HTTPError as e:
    print('[FAIL] HTTP', e.code, e.read()[:200].decode())
except Exception as e:
    print('[FAIL] Login:', e)

if not token:
    print('Cannot continue without token.')
    exit(1)

# Step 2: Get accounts
print()
print('[2] Fetching sending accounts...')
try:
    req2 = urllib.request.Request(
        BASE + '/api/sending-accounts',
        headers={'Authorization': 'Bearer ' + token}
    )
    with urllib.request.urlopen(req2, timeout=15) as r:
        accounts = json.loads(r.read())
        warmup_list = [a for a in accounts if a.get('warmup_enabled')]
        print('    Total accounts :', len(accounts))
        print('    Warmup-enabled :', len(warmup_list))
        print()
        for a in accounts:
            status = 'WARMUP=ON' if a.get('warmup_enabled') else 'warmup=off'
            em = a.get('email', '?')
            hs = a.get('health_score', 0)
            wt = a.get('warmup_total_sent', 'N/A')
            wd = a.get('warmup_sent_today', 0)
            wl = a.get('warmup_daily_limit', 5)
            print(f'    {em} | health={hs}% | {status} | warmup_total={wt} | today={wd}/{wl}')
except Exception as e:
    print('[FAIL] Accounts:', e)

# Step 3: Trigger warmup manually via run-warmup endpoint
print()
print('[3] Triggering manual warmup cycle...')
try:
    req3 = urllib.request.Request(
        BASE + '/api/run-warmup',
        data=b'{}',
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    with urllib.request.urlopen(req3, timeout=60) as r:
        result = json.loads(r.read())
        print('[OK] Warmup result:', result)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'[HTTP {e.code}]', body[:300])
except Exception as e:
    print('[FAIL] Warmup trigger:', e)

# Step 4: Check accounts again after warmup
print()
print('[4] Checking accounts AFTER warmup...')
try:
    req4 = urllib.request.Request(
        BASE + '/api/sending-accounts',
        headers={'Authorization': 'Bearer ' + token}
    )
    with urllib.request.urlopen(req4, timeout=15) as r:
        accounts2 = json.loads(r.read())
        for a in accounts2:
            if a.get('warmup_enabled'):
                em = a.get('email', '?')
                hs = a.get('health_score', 0)
                wt = a.get('warmup_total_sent', 'N/A')
                wd = a.get('warmup_sent_today', 0)
                wl = a.get('warmup_daily_limit', 5)
                print(f'    {em} | health={hs}% | warmup_total={wt} | today={wd}/{wl}')
except Exception as e:
    print('[FAIL]', e)

print()
print('=== DONE ===')
