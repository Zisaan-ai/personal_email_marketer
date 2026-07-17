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

# Upload passenger_wsgi_diag.py as passenger_wsgi.py
print("Uploading passenger_wsgi_diag.py...")
with open('passenger_wsgi_diag.py', 'rb') as f:
    ftp.storbinary('STOR passenger_wsgi.py', f)

print("Triggering restart...")
ftp.cwd('tmp')
ftp.storbinary('STOR restart.txt', io.BytesIO(b'restart'))
print("Restart triggered!")

ftp.quit()
print("Done!")
