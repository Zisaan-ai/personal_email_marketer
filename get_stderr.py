import ftplib

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

ftp.cwd('xcomic_backend')

# Download last part of stderr.log (it's big, get last 50KB)
import io
buf = io.BytesIO()
ftp.retrbinary('RETR stderr.log', buf.write)
content = buf.getvalue()

# Get last 8000 bytes
last_part = content[-8000:].decode('utf-8', errors='replace')
print("=== LAST 8000 bytes of stderr.log ===")
print(last_part)

ftp.quit()
