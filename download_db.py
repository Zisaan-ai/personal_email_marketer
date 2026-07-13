import ftplib
import io

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('live_mailclone.db', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/mailclone.db', f.write)

ftp.quit()
print('Downloaded DB!')
