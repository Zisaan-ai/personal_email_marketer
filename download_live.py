import ftplib
import os

FTP_HOST = '167.235.11.154'
FTP_USER = 'terapkco'
FTP_PASS = '(3#JCk2Vyn94hY'

print('Connecting to FTP...')
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)

if not os.path.exists('live_code'):
    os.makedirs('live_code')

files_to_download = [
    ('/xcomic_backend', 'main.py'),
    ('/xcomic_backend', 'database.py'),
    ('/xcomic_backend', 'ai_core.py'),
    ('/xcomic_backend', 'bounce_processor.py'),
    ('/xcomic_backend', 'health_monitor.py'),
    ('/xcomic_backend', 'warmup_service.py'),
    ('/xcomic_backend', 'passenger_wsgi.py'),
    ('/xcomic.xyz', 'index.html'),
    ('/xcomic.xyz/assets', 'app.js'),
    ('/xcomic.xyz/assets', 'sending_accounts.js'),
]

for directory, filename in files_to_download:
    try:
        ftp.cwd(directory)
        local_path = os.path.join('live_code', filename)
        with open(local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {filename}', f.write)
        print(f"Downloaded {directory}/{filename}")
    except Exception as e:
        print(f"Failed to download {directory}/{filename}: {e}")

ftp.quit()
print('Done downloading live files.')
