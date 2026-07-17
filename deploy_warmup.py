import ftplib
import sys
import time
import io

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
REMOTE_DIR = "/xcomic_backend"

sys.stdout.reconfigure(encoding='utf-8')

def ftp_connect():
    for pasv in [True, False]:
        try:
            ftp = ftplib.FTP(timeout=30)
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASS)
            ftp.set_pasv(pasv)
            ftp.cwd(REMOTE_DIR)
            print(f"[OK] FTP connected (passive={pasv})")
            return ftp
        except Exception as e:
            print(f"   passive={pasv} failed: {e}")
    raise Exception("All FTP modes failed!")

def upload(ftp, local, remote):
    with open(local, "rb") as f:
        ftp.storbinary(f"STOR {remote}", f)
    print(f"[OK] Uploaded: {remote}")

print("=" * 50)
print("  WARMUP DEPLOY + TEST")
print("=" * 50)

# Step 1: Upload
print("\n[1] Uploading files...")
ftp = ftp_connect()
upload(ftp, r"xcomic_backend\warmup_service.py", "warmup_service.py")
upload(ftp, r"xcomic_backend\health_monitor.py", "health_monitor.py")
upload(ftp, r"xcomic_backend\database.py", "database.py")
upload(ftp, r"xcomic_backend\main.py", "main.py")

# Step 2: Restart
print("\n[2] Restarting server (touch restart.txt)...")
ftp.storbinary("STOR restart.txt", io.BytesIO(str(time.time()).encode()))
print("[OK] restart.txt updated")
ftp.quit()

print("\n[3] Waiting 6s for server to restart...")
time.sleep(6)

# Step 3: API Test
import urllib.request
import json

BASE_URL = "https://xcomic.xyz/api"

print("\n[4] Logging in...")
try:
    req = urllib.request.Request(
        BASE_URL + "/login",
        data=json.dumps({"email": "mzisan367@gmail.com", "password": "admin123"}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
        token = data.get("access_token")
        print(f"[OK] Token: {token[:30]}..." if token else f"[FAIL] {data}")
except Exception as e:
    token = None
    print(f"[FAIL] Login: {e}")

# Step 4: Check accounts
if token:
    print("\n[5] Checking warmup accounts...")
    try:
        req2 = urllib.request.Request(
            BASE_URL + "/sending-accounts",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req2, timeout=20) as r:
            accounts = json.loads(r.read())
            warmup_accs = [a for a in accounts if a.get("warmup_enabled")]
            print(f"    Total accounts  : {len(accounts)}")
            print(f"    Warmup-enabled  : {len(warmup_accs)}")
            for a in warmup_accs:
                print(f"    -> {a['email']} | health={a.get('health_score',0)}% | total_warmup={a.get('warmup_total_sent',0)} | today={a.get('warmup_sent_today',0)}/{a.get('warmup_daily_limit',5)}")
    except Exception as e:
        print(f"[FAIL] {e}")

# Step 5: Trigger warmup
if token:
    print("\n[6] Triggering manual warmup cycle...")
    try:
        req3 = urllib.request.Request(
            BASE_URL + "/run-warmup",
            data=b"{}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req3, timeout=45) as r:
            result = json.loads(r.read())
            print(f"[OK] Warmup result: {result}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"    HTTP {e.code}: {body[:300]}")
    except Exception as e:
        print(f"[FAIL] {e}")

print("\n" + "=" * 50)
print("  DONE")
print("=" * 50)
