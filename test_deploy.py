import ftplib
FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'
try:
    with open('main_live.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace('"health_score": acc.health_score}', '"health_score": acc.health_score, "test_deploy": "WORKS!"}')
    
    with open('main_live_test.py', 'w', encoding='utf-8') as f:
        f.write(text)

    ftp = ftplib.FTP(FTP_HOST, timeout=20)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd('xcomic_backend')
    with open('main_live_test.py', 'rb') as f:
        ftp.storbinary('STOR main.py', f)
    ftp.cwd('../tmp')
    with open('restart.txt', 'wb') as f:
        f.write(b'')
    with open('restart.txt', 'rb') as f:
        ftp.storbinary('STOR restart.txt', f)
    ftp.quit()
    print('Uploaded main.py with test modification.')
except Exception as e:
    print('FTP failed:', e)
