import ftplib
ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
with open('downloaded_main.py', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/main.py', f.write)
ftp.quit()
