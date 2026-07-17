import ftplib
import time

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading restored files...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

# Upload index.html
ftp.cwd('/xcomic.xyz')
with open('xcomic.xyz/index.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)

# Upload app.js
ftp.cwd('/xcomic.xyz/assets')
with open('xcomic.xyz/assets/app.js', 'rb') as f:
    ftp.storbinary('STOR app.js', f)

print('Done uploading frontend files.')

# Bust cache
print('Busting cache...')
ftp.cwd('/xcomic.xyz')
with open('xcomic.xyz/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
import random
new_ver = f"{time.time()}"
html = re.sub(r'app\.js\?v=[\d\.]+', f'app.js?v={new_ver}', html)

with open('xcomic.xyz/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('xcomic.xyz/index.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)

ftp.quit()
print('All restored and cache busted.')
