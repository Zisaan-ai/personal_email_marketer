import ftplib
ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
with open('downloaded_index.html', 'wb') as f:
    ftp.retrbinary('RETR xcomic.xyz/index.html', f.write)
ftp.quit()
