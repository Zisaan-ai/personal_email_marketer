import ftplib
import io

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
ftp.cwd('xcomic_backend')

buf = io.BytesIO()
ftp.retrbinary('RETR stderr.log', buf.write)
content = buf.getvalue()

# Print last 5000 bytes
last_part = content[-5000:].decode('utf-8', errors='replace')
print("=== LAST 5000 bytes of stderr.log ===")
print(last_part)

ftp.quit()
