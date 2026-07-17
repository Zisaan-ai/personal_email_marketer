import ftplib
import io

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

print("Connecting to FTP...")
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
ftp.cwd('xcomic_backend')

print("Uploading main_live.py -> main.py...")
with open('main_live.py', 'rb') as f:
    ftp.storbinary('STOR main.py', f)

# Delete pycache
try:
    ftp.cwd('__pycache__')
    files = ftp.nlst()
    for f in files:
        try:
            ftp.delete(f)
        except:
            pass
    ftp.cwd('..')
    ftp.rmd('__pycache__')
except:
    pass

print("Triggering reload...")
ftp.cwd('/xcomic_backend/tmp')
ftp.storbinary('STOR restart.txt', io.BytesIO(b'restart'))

ftp.quit()
print("Success!")
