import os
import ftplib
import time

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

local_path = r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\style.css"
remote_path = "/xcomic.xyz/assets/style.css"

local_size = os.path.getsize(local_path)
print(f"Local file size: {local_size} bytes")

# Upload with verification
for attempt in range(1, 4):
    print(f"\nAttempt {attempt}: Uploading style.css ({local_size} bytes)...")
    try:
        ftp = ftplib.FTP(timeout=120)
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.set_pasv(True)
        
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f, blocksize=8192)
        
        # Verify remote size
        try:
            remote_size = ftp.size(remote_path)
            print(f"Remote file size after upload: {remote_size} bytes")
            if remote_size == local_size:
                print("SUCCESS: File sizes match!")
                ftp.quit()
                break
            else:
                print(f"MISMATCH: Local={local_size}, Remote={remote_size}")
        except:
            print("Could not verify remote size via FTP SIZE command")
        
        ftp.quit()
    except Exception as e:
        print(f"Upload error: {e}")
    time.sleep(3)

print("\nDone. Now verifying via HTTP...")

import urllib.request
try:
    req = urllib.request.Request("https://xcomic.xyz/assets/style.css?nocache=" + str(time.time()))
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()
        print(f"HTTP downloaded size: {len(content)} bytes")
        text = content.decode('utf-8', errors='ignore')
        print(f"Contains UNBEATABLE: {'UNBEATABLE' in text}")
        print(f"Contains min-width 769: {'min-width: 769px' in text}")
        print(f"Last 200 chars: {text[-200:]}")
except Exception as e:
    print(f"HTTP verify error: {e}")
