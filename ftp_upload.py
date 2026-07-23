import ftplib
import os
import sys

# Reconfigure stdout to avoid encoding errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

GIT_ROOT = r'C:\Users\higan\.gemini\antigravity\scratch\github_sync'

files_to_upload = [
    ('xcomic.xyz/assets/app.js', '/xcomic.xyz/assets/app.js'),
    ('xcomic.xyz/index.html', '/xcomic.xyz/index.html'),
]

ftp = ftplib.FTP('terapk.com', timeout=30)
ftp.login('terapkco', '(3#JCk2Vyn94hY')

for local_rel, remote_abs in files_to_upload:
    local_path = os.path.join(GIT_ROOT, local_rel.replace('/', os.sep))
    if os.path.exists(local_path):
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_abs}', f)
        print(f"Uploaded {local_rel}")
    else:
        print(f"File not found: {local_path}")

ftp.quit()
