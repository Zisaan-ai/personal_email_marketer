import ftplib
import io

ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')

def upload(local_file, remote_file):
    try:
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
            print(f"Uploaded {local_file} to {remote_file}")
    except Exception as e:
        print(f"Failed to upload {local_file}: {e}")

upload('backend/main.py', 'xcomic_backend/main.py')
upload('backend/database.py', 'xcomic_backend/database.py')
upload('backend/health_monitor.py', 'xcomic_backend/health_monitor.py')
upload('backend/warmup_service.py', 'xcomic_backend/warmup_service.py')
upload('frontend/assets/app_v2.js', 'xcomic.xyz/assets/app_v2.js')
upload('frontend/assets/sending_accounts.js', 'xcomic.xyz/assets/sending_accounts.js')
upload('frontend/index.html', 'xcomic.xyz/index.html')

try:
    ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', io.BytesIO(b''))
    print("Restarted backend")
except Exception as e:
    print(f"Failed to restart backend: {e}")

ftp.quit()
print('Done!')
