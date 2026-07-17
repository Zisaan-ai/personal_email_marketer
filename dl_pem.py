import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/personal_email_marketer')
with open('pem_index.html', 'wb') as f:
    try:
        ftp.retrbinary('RETR index.html', f.write)
    except Exception as e:
        print(f"Error downloading index.html: {e}")
ftp.quit()
