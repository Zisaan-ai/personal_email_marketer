import ftplib, os, sys
sys.path.append(os.getcwd())
from custom_deploy import FTP_HOST, FTP_USER, FTP_PASS, FTP_BACKEND_REMOTE

ftp = ftplib.FTP(timeout=60)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(FTP_BACKEND_REMOTE)
with open('live_stderr.log', 'wb') as f:
    ftp.retrbinary('RETR stderr.log', f.write)
ftp.quit()
print("Downloaded live_stderr.log")
