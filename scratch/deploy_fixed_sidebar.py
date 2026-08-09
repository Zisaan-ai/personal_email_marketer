import os
import ftplib
import time
import urllib.request

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

files = [
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\style.css", "/xcomic.xyz/assets/style.css"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html", "/xcomic.xyz/index.html"),
]

for local_path, remote_path in files:
    local_size = os.path.getsize(local_path)
    fname = os.path.basename(local_path)
    print(f"\n--- Uploading {fname} ({local_size} bytes) ---")
    
    for attempt in range(1, 4):
        try:
            ftp = ftplib.FTP(timeout=120)
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASS)
            ftp.set_pasv(True)
            
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_path}", f, blocksize=8192)
            
            remote_size = ftp.size(remote_path)
            ftp.quit()
            
            if remote_size == local_size:
                print(f"  SUCCESS: {fname} Local={local_size} Remote={remote_size} MATCH!")
                break
            else:
                print(f"  MISMATCH attempt {attempt}: Local={local_size} Remote={remote_size}")
        except Exception as e:
            print(f"  Error attempt {attempt}: {e}")
        time.sleep(2)

# HTTP verification
print("\n--- HTTP Verification ---")
for url_path, keyword in [
    ("assets/style.css", "position: fixed"),
    ("index.html", "position: fixed"),
]:
    url = f"https://xcomic.xyz/{url_path}?bust={time.time()}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            found = keyword in text
            print(f"  {url_path}: '{keyword}' found = {found} ({len(text)} bytes)")
    except Exception as e:
        print(f"  {url_path}: HTTP error: {e}")

print("\nDone!")
