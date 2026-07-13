import ftplib
import io
import time

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

try:
    ftp.delete('xcomic_backend/tmp/restart.txt')
    print('Deleted old restart.txt')
except Exception as e:
    print('Could not delete old restart.txt:', e)

ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', io.BytesIO(b'restart\n'))
print('Created new restart.txt')
ftp.quit()
