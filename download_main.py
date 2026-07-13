import ftplib
import io

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('server_main.py', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/main.py', f.write)

ftp.quit()
