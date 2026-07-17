import ftplib
import os

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Uploading warmup_service.py...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('xcomic_backend/warmup_service.py', 'rb') as f:
    ftp.storbinary('STOR warmup_service.py', f)
print('Uploaded.')

# Now upload a PHP script to kill all python processes
php_code = b"<?php system('pkill -f python'); echo 'Killed Python processes'; ?>"
from io import BytesIO
ftp.cwd('/public_html')
ftp.storbinary('STOR kill.php', BytesIO(php_code))
ftp.quit()
print('Uploaded kill.php')

