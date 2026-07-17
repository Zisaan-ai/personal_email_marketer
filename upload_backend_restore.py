import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading restored backend files...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

ftp.cwd('/xcomic_backend')
with open('xcomic_backend/main.py', 'rb') as f:
    ftp.storbinary('STOR main.py', f)
with open('xcomic_backend/database.py', 'rb') as f:
    ftp.storbinary('STOR database.py', f)
with open('xcomic_backend/ai_core.py', 'rb') as f:
    ftp.storbinary('STOR ai_core.py', f)

print('Restarting passenger app...')
try:
    ftp.cwd('../tmp')
except Exception:
    ftp.cwd('/')
    try:
        ftp.mkd('tmp')
        ftp.cwd('tmp')
    except:
        pass

from io import BytesIO
ftp.storbinary('STOR restart.txt', BytesIO(b'restart'))

ftp.quit()
print('Done.')
