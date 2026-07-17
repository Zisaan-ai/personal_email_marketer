import ftplib
import io
import os

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

print("Connecting...")
ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
ftp.cwd('xcomic_backend')

# Upload passenger_wsgi.py
print("Uploading passenger_wsgi.py...")
with open('passenger_wsgi.py', 'rb') as f:
    ftp.storbinary('STOR passenger_wsgi.py', f)
print(f"  Done! ({os.path.getsize('passenger_wsgi.py'):,} bytes)")

# Touch restart.txt
print("Triggering restart...")
ftp.cwd('tmp')
empty = io.BytesIO(b'restart')
ftp.storbinary('STOR restart.txt', empty)
print("  restart.txt updated!")

ftp.quit()
print("All done!")
