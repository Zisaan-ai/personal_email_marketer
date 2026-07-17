import ftplib
import sys

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('passenger_wsgi.py', 'wb') as f:
    ftp.retrbinary('RETR passenger_wsgi.py', f.write)

with open('passenger_wsgi.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "os.system('nohup python -m uvicorn main:app --host 127.0.0.1 --port 47300 --workers 1 > uvicorn.log 2>&1 &')",
    "import sys\n    os.system(f'nohup {sys.executable} -m uvicorn main:app --host 127.0.0.1 --port 47300 --workers 1 > uvicorn.log 2>&1 &')"
)

with open('passenger_wsgi.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('passenger_wsgi.py', 'rb') as f:
    ftp.storbinary('STOR passenger_wsgi.py', f)

ftp.quit()
print('Fixed passenger_wsgi.py')
