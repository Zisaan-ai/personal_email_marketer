import os
import ftplib
import time

FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

files = [
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js", "/xcomic.xyz/assets/app.js"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic_backend\main.py", "/xcomic_backend/main.py"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic_backend\ai_core.py", "/xcomic_backend/ai_core.py"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html", "/xcomic.xyz/index.html"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\style.css", "/xcomic.xyz/assets/style.css"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\support_patch.js", "/xcomic.xyz/assets/support_patch.js"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\ai_features.js", "/xcomic.xyz/assets/ai_features.js"),
]

for local_path, remote_path in files:
    local_size = os.path.getsize(local_path)
    fname = os.path.basename(local_path)
    
    ftp = ftplib.FTP(timeout=120)
    ftp.connect(FTP_HOST, 21)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f, blocksize=8192)
    
    try:
        remote_size = ftp.size(remote_path)
        match = "MATCH" if remote_size == local_size else "MISMATCH"
        print(f"{fname}: Local={local_size}, Remote={remote_size} -> {match}")
    except:
        print(f"{fname}: uploaded (size check unavailable)")
    
    ftp.quit()

# Trigger restart
ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
restart_path = r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\restart.txt"
with open(restart_path, "w") as f:
    f.write(str(time.time()))
with open(restart_path, "rb") as f:
    ftp.storbinary("STOR /xcomic_backend/tmp/restart.txt", f)
with open(restart_path, "rb") as f:
    ftp.storbinary("STOR /xcomic_backend/restart.txt", f)
ftp.quit()
print("App restart triggered!")
os.remove(restart_path)

print("\nAll done!")
