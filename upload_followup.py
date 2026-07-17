import sys
from ftplib import FTP
import os
from datetime import datetime

# Files to upload (local_path, remote_dir, filename)
files = [
    (r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\database.py", "xcomic_backend", "database.py"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\main.py", "xcomic_backend", "main.py"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\bounce_processor.py", "xcomic_backend", "bounce_processor.py"),
    (r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic.xyz\assets\app.js", "xcomic.xyz/assets", "app.js")
]

try:
    ftp = FTP('xcomic.xyz', timeout=30)
    ftp.login('terapkco', '(3#JCk2Vyn94hY')
    
    for local_path, remote_dir, filename in files:
        print(f"Uploading {filename} to {remote_dir}...")
        ftp.cwd(f'/{remote_dir}')
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
            
    # Trigger restart
    print("Triggering restart...")
    ftp.cwd('/xcomic_backend/tmp')
    with open('restart.txt', 'w') as f:
        f.write(str(datetime.now()))
    with open('restart.txt', 'rb') as f:
        ftp.storbinary('STOR restart.txt', f)
        
    ftp.quit()
    print("Upload and restart complete.")
except Exception as e:
    print(f"Error: {e}")
