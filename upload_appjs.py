import ftplib
import os

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading app.js...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic.xyz/assets')

with open('xcomic.xyz/assets/app.js', 'rb') as f:
    ftp.storbinary('STOR app.js', f)
print('Uploaded.')
ftp.quit()
