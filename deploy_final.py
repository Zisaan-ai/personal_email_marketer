import ftplib
import io
import os

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

print("Connecting to FTP...")
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
ftp.cwd('xcomic_backend')

# 1. Upload main_live.py as main.py
print("Uploading main_live.py -> main.py...")
with open('main_live.py', 'rb') as f:
    ftp.storbinary('STOR main.py', f)
print("Uploaded main.py")

# 2. Upload passenger_wsgi.py
print("Uploading passenger_wsgi.py...")
with open('passenger_wsgi.py', 'rb') as f:
    ftp.storbinary('STOR passenger_wsgi.py', f)
print("Uploaded passenger_wsgi.py")

# 3. Delete cached bytecode
try:
    ftp.cwd('__pycache__')
    files = ftp.nlst()
    print(f"Deleting {len(files)} cached files...")
    for f in files:
        try:
            ftp.delete(f)
        except Exception as e:
            print(f"Could not delete {f}: {e}")
    ftp.cwd('..')
    try:
        ftp.rmd('__pycache__')
        print("Deleted __pycache__ directory")
    except Exception as e:
        print(f"Could not rmdir __pycache__: {e}")
except Exception as e:
    print(f"__pycache__ issue: {e}")

# 4. Trigger reload
print("Triggering reload...")
ftp.cwd('/xcomic_backend/tmp')
ftp.storbinary('STOR restart.txt', io.BytesIO(b'restart'))
print("Reload triggered!")

ftp.quit()
print("Deployment successful!")
