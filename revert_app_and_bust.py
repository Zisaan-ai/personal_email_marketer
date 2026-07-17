import ftplib
import time
import re

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading app.js and busting cache...')

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

# Upload reverted app.js
ftp.cwd('/xcomic.xyz/assets')
with open('xcomic.xyz/assets/app.js', 'rb') as f:
    ftp.storbinary('STOR app.js', f)

# Bust cache in index.html
ftp.cwd('/xcomic.xyz')
with open('live_index.html', 'wb') as f:
    ftp.retrbinary('RETR index.html', f.write)

with open('live_index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_v = int(time.time())
content = re.sub(r'assets/app\.js\?v=\d+', f'assets/app.js?v={new_v}', content)

with open('live_index_fixed.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('live_index_fixed.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)

print('Done uploading app.js and busting cache.')
ftp.quit()
