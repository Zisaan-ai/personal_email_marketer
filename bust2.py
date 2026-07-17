import ftplib
import time

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Busting cache on live index again just in case...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

ftp.cwd('/xcomic.xyz')
with open('xcomic.xyz/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
new_ver = f"{time.time()}_v2"
html = re.sub(r'app\.js\?v=[\d\._v]+', f'app.js?v={new_ver}', html)

with open('xcomic.xyz/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('xcomic.xyz/index.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)

ftp.quit()
print('Cache busted.')
