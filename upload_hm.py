import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading health_monitor.py...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('xcomic_backend/health_monitor.py', 'rb') as f:
    ftp.storbinary('STOR health_monitor.py', f)
print('Uploaded.')
ftp.quit()
