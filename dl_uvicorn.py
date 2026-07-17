import ftplib

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Downloading uvicorn.log...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd('/xcomic_backend')

with open('live_uvicorn.log', 'wb') as f:
    # Try to download the last few KB if possible, but retrbinary gets all
    ftp.retrbinary('RETR uvicorn.log', f.write)

print('Downloaded uvicorn.log')
ftp.quit()
