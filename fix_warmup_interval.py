import ftplib
from io import BytesIO

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading fixed main.py...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

ftp.cwd('/xcomic_backend')
with open('xcomic_backend/main.py', 'rb') as f:
    ftp.storbinary('STOR main.py', f)
print('main.py uploaded.')

# Restart passenger
print('Triggering restart...')
ftp.cwd('/tmp')
ftp.storbinary('STOR restart.txt', BytesIO(b'restart'))
ftp.quit()
print('Done. Warmup interval is now 30 minutes.')
