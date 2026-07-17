import ftplib

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

ftp.cwd('xcomic_backend')

# Download passenger_wsgi.py to see which file it uses
lines = []
ftp.retrlines('RETR passenger_wsgi.py', lines.append)
print("=== passenger_wsgi.py ===")
print('\n'.join(lines))

ftp.quit()
