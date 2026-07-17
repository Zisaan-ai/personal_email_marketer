import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading index.html...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic.xyz')

with open('xcomic.xyz/index.html', 'rb') as f:
    ftp.storbinary('STOR index.html', f)
print('Uploaded.')
ftp.quit()
