import ftplib
import io
import time

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

# Just touch tmp/restart.txt inside xcomic.xyz
try:
    ftp.storbinary('STOR xcomic.xyz/tmp/restart.txt', io.BytesIO(b''))
    print("Restarted xcomic.xyz")
except Exception as e:
    print(e)

ftp.quit()
