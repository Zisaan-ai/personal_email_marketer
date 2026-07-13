import ftplib
import io

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

def upload(local_file, remote_file):
    with open(local_file, 'rb') as f:
        ftp.storbinary(f'STOR {remote_file}', f)
        print(f"Uploaded {local_file} to {remote_file}")

upload('backend/main.py', 'xcomic_backend/main.py')
upload('backend/database.py', 'xcomic_backend/database.py')
upload('backend/email_service.py', 'xcomic_backend/email_service.py')
upload('backend/bounce_processor.py', 'xcomic_backend/bounce_processor.py')
upload('backend/health_monitor.py', 'xcomic_backend/health_monitor.py')
upload('frontend/assets/app.js', 'xcomic.xyz/assets/app.js')

upload('frontend/index.html', 'xcomic.xyz/index.html')

ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', io.BytesIO(b''))
ftp.quit()
print('Done!')
