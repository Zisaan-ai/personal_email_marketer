import ftplib
import io
import time

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

try:
    restart_data = str(time.time()).encode('utf-8')
    ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', io.BytesIO(restart_data))
    print("Restarted backend")
except Exception as e:
    print(f"Failed to restart backend: {e}")

ftp.quit()
print('Done!')
