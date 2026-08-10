import os
import ftplib
import hashlib
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ROOT_DIR = r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer"

files_to_compare = [
    (os.path.join(ROOT_DIR, "xcomic_backend", "main.py"), "/xcomic_backend/main.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "database.py"), "/xcomic_backend/database.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "bulk_campaign_sender.py"), "/xcomic_backend/bulk_campaign_sender.py"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "index.html"), "/xcomic.xyz/index.html"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "app.js"), "/xcomic.xyz/assets/app.js"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "style.css"), "/xcomic.xyz/assets/style.css"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "support_patch.js"), "/xcomic.xyz/assets/support_patch.js"),
]

def get_hash(data):
    return hashlib.md5(data.replace(b"\r\n", b"\n")).hexdigest()

print("--- Connecting to FTP to compare live server files with Git repo ---\n")

ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

all_match = True

for local_path, remote_path in files_to_compare:
    rel_name = os.path.relpath(local_path, ROOT_DIR)
    with open(local_path, "rb") as f:
        local_bytes = f.read()
    
    # Download remote file
    remote_bytes = bytearray()
    try:
        ftp.retrbinary(f"RETR {remote_path}", remote_bytes.extend)
    except Exception as e:
        print(f"FAILED to download {remote_path}: {e}")
        all_match = False
        continue

    remote_bytes = bytes(remote_bytes)
    
    local_size = len(local_bytes)
    remote_size = len(remote_bytes)
    
    local_md5 = get_hash(local_bytes)
    remote_md5 = get_hash(remote_bytes)
    
    match = (local_md5 == remote_md5)
    status = "[MATCH] 100% IDENTICAL" if match else "[MISMATCH]"
    
    print(f"File: {rel_name}")
    print(f"  Local Git:   {local_size} bytes | MD5: {local_md5}")
    print(f"  Live Server: {remote_size} bytes | MD5: {remote_md5}")
    print(f"  Status: {status}\n")
    
    if not match:
        all_match = False

ftp.quit()

if all_match:
    print("==========================================")
    print("PERFECT MATCH! All live server files are 100% identical to Git repo!")
    print("==========================================")
else:
    print("==========================================")
    print("WARNING: Some live server files do not match Git repo!")
    print("==========================================")
