import ftplib

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

with open('passenger_wsgi.py', 'wb') as f:
    ftp.retrbinary('RETR xcomic_backend/passenger_wsgi.py', f.write)

with open('passenger_wsgi.py', 'a') as f:
    f.write('\n# touch to restart\n')

with open('passenger_wsgi.py', 'rb') as f:
    ftp.storbinary('STOR xcomic_backend/passenger_wsgi.py', f)

ftp.quit()
print('Restarted passenger app by touching passenger_wsgi.py!')
