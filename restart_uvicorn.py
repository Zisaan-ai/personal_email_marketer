import ftplib
import io
import time

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
ftp.cwd('/xcomic_backend')

buf = io.BytesIO()
ftp.retrbinary('RETR passenger_wsgi.py', buf.write)
content = buf.getvalue().decode('utf-8')

if 'os.system("pkill -f uvicorn")' not in content:
    content = content.replace(
        'def ensure_uvicorn_running(port=47300):',
        'def ensure_uvicorn_running(port=47300):\n    os.system("pkill -f uvicorn")\n    time.sleep(1)'
    )
    ftp.storbinary('STOR passenger_wsgi.py', io.BytesIO(content.encode('utf-8')))

ftp.storbinary('STOR tmp/restart.txt', io.BytesIO(str(time.time()).encode()))
ftp.quit()
print('[OK] Modified passenger_wsgi and restarted')
