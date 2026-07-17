import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Downloading xcomic.db...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('live_xcomic.db', 'wb') as f:
    ftp.retrbinary('RETR xcomic.db', f.write)
print('Downloaded.')
ftp.quit()
