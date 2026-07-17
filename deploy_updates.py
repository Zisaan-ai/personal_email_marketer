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

# 1. Upload warmup_service.py
print("Uploading warmup_service.py...")
with open('xcomic_backend/warmup_service.py', 'rb') as f:
    ftp.storbinary('STOR warmup_service.py', f)

# 2. Upload bounce_processor.py
print("Uploading bounce_processor.py...")
with open('xcomic_backend/bounce_processor.py', 'rb') as f:
    ftp.storbinary('STOR bounce_processor.py', f)

print("Triggering reload...")
ftp.cwd('tmp')
ftp.storbinary('STOR restart.txt', io.BytesIO(b'restart'))

ftp.quit()
print("Success!")
