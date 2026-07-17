import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

# get list of files
files = []
ftp.retrlines('LIST', files.append)
print('--- FILES ---')
for line in files:
    print(line)

print('--- CHECKING LOGS ---')
try:
    with open('stderr.log', 'wb') as f:
        ftp.retrbinary('RETR stderr.log', f.write)
    print('stderr.log downloaded')
except Exception as e:
    print('No stderr.log found:', e)

ftp.quit()
