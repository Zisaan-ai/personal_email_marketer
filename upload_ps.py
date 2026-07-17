import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

php_code = b"<?php system('ps aux | grep python'); ?>"

from io import BytesIO
ftp.cwd('/public_html')
ftp.storbinary('STOR ps.php', BytesIO(php_code))
ftp.quit()
print('Uploaded ps.php')
