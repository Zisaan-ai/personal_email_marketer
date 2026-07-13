import ftplib

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
print('Root:', ftp.nlst())
try:
    print('xcomic_backend:', ftp.nlst('xcomic_backend'))
except: pass
try:
    print('tmp:', ftp.nlst('tmp'))
except: pass
ftp.quit()
