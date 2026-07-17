import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic.xyz')
with open('live_htaccess.txt', 'wb') as f:
    try:
        ftp.retrbinary('RETR .htaccess', f.write)
    except:
        pass
ftp.quit()
