import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')
with open('live_wsgi_check.py', 'wb') as f:
    ftp.retrbinary('RETR passenger_wsgi.py', f.write)
ftp.quit()
