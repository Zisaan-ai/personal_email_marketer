import ftplib
import time

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Busting cache in index.html...')

with open('live_index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_v = int(time.time())
content = content.replace(
    'assets/sending_accounts.js?v=1783200000',
    f'assets/sending_accounts.js?v={new_v}'
)

with open('live_index_fixed.html', 'w', encoding='utf-8') as f:
    f.write(content)

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic.xyz')

with open('live_index_fixed.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)

print('Uploaded fixed index.html.')
ftp.quit()
