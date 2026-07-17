import ftplib
import os

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

print('--- /xcomic_backend ---')
ftp.cwd('/xcomic_backend')
ftp.retrlines('LIST')

print('--- / --- (root)')
ftp.cwd('/')
ftp.retrlines('LIST')

ftp.quit()
