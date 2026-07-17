import ftplib
FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'
try:
    ftp = ftplib.FTP(FTP_HOST, timeout=20)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd('xcomic_backend')
    with open('main_remote.py', 'wb') as f:
        ftp.retrbinary('RETR main.py', f.write)
    ftp.quit()
    
    with open('main_remote.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'getattr(acc, "provider"' in content:
            print('Patch IS in main.py')
        else:
            print('Patch is NOT in main.py')
            if 'provider' in content:
                print('provider is in main.py, but not as getattr')
                idx = content.find('provider')
                print(content[max(0, idx-20):idx+20])
except Exception as e:
    print('FTP failed:', e)
