import ftplib
import os

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
LOCAL_FILE = "main_live.py"  # Our updated file
REMOTE_FILE = "main.py"      # Server runs this!

print("Connecting to FTP...")
ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

ftp.cwd('xcomic_backend')
print("Current dir:", ftp.pwd())
print(f"Uploading {LOCAL_FILE} -> {REMOTE_FILE} ...")

with open(LOCAL_FILE, 'rb') as f:
    ftp.storbinary(f'STOR {REMOTE_FILE}', f)

print("SUCCESS! Upload complete.")
print(f"File size: {os.path.getsize(LOCAL_FILE):,} bytes")
ftp.quit()
