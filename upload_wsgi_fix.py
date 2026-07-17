import ftplib
import os

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading passenger_wsgi.py...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('xcomic_backend/passenger_wsgi.py', 'rb') as f:
    ftp.storbinary('STOR passenger_wsgi.py', f)

print('Restarting passenger app...')
try:
    ftp.cwd('tmp')
except Exception:
    ftp.mkd('tmp')
    ftp.cwd('tmp')

from io import BytesIO
ftp.storbinary('STOR restart.txt', BytesIO(b'restart'))

ftp.quit()
print('Done.')
