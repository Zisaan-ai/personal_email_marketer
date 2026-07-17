import ftplib
import io

host = '167.235.11.154'
user = 'terapkco'
password = '(3#JCk2Vyn94hY'

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    content = b'''import sys, os

INTERP = os.path.expanduser("/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from main import app as application
'''
    ftp.storbinary('STOR passenger_wsgi.py', io.BytesIO(content))
    ftp.cwd('../tmp')
    ftp.storbinary('STOR restart.txt', io.BytesIO(b''))
    ftp.quit()
    print("Done")
except Exception as e:
    print(f"Error: {e}")
