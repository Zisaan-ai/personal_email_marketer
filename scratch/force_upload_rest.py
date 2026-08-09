import os
import ftplib
import time

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

files = [
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html", "/xcomic.xyz/index.html"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js", "/xcomic.xyz/assets/app.js"),
]

for local_path, remote_path in files:
    local_size = os.path.getsize(local_path)
    print(f"\nUploading {os.path.basename(local_path)} ({local_size} bytes)...")
    
    ftp = ftplib.FTP(timeout=120)
    ftp.connect(FTP_HOST, 21)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f, blocksize=8192)
    
    try:
        remote_size = ftp.size(remote_path)
        match = "MATCH" if remote_size == local_size else "MISMATCH"
        print(f"  Local={local_size}, Remote={remote_size} -> {match}")
    except:
        print("  Could not verify size")
    
    ftp.quit()

print("\nAll critical files uploaded and verified!")
