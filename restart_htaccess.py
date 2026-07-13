import ftplib

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('.htaccess', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/.htaccess', f.write)

with open('.htaccess', 'a') as f:
    f.write('\n# restart')

with open('.htaccess', 'rb') as f:
    ftp.storbinary('STOR xcomic_backend/.htaccess', f)

ftp.quit()
print('Modified .htaccess to trigger restart')
