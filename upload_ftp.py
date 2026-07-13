import os
import ftplib
import time

def upload_dir(ftp, local_dir, remote_dir):
    try:
        ftp.mkd(remote_dir)
    except ftplib.error_perm:
        pass # Directory likely already exists

    for item in os.listdir(local_dir):
        if item in ['venv', '__pycache__', '.git', '.idea', 'node_modules', 'frontend_update.zip', 'mailclone.db', 'sql_app.db', '.env', 'upload_ftp.py', 'test_run.log', 'test_app.js', 'live_app.js']:
            continue
            
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isfile(local_path):
            if item.endswith(('.py', '.html', '.js', '.css', '.txt', '.json', '.md', '.yaml', '.example', '.env')):
                with open(local_path, 'rb') as f:
                    print(f"Uploading file: {local_path} -> {remote_path}")
                    try:
                        ftp.storbinary(f'STOR {remote_path}', f)
                    except Exception as e:
                        print(f"Failed to upload {item}: {e}")
            else:
                with open(local_path, 'rb') as f:
                    print(f"Uploading binary file: {local_path} -> {remote_path}")
                    try:
                        ftp.storbinary(f'STOR {remote_path}', f)
                    except Exception as e:
                        print(f"Failed to upload {item}: {e}")
        elif os.path.isdir(local_path):
            upload_dir(ftp, local_path, remote_path)

if __name__ == "__main__":
    ftp = ftplib.FTP('terapk.com')
    ftp.login('terapkco', '(3#JCk2Vyn94hY')
    print("Logged in!")
    upload_dir(ftp, '.', 'xcomic_backend')
    
    # Restart the app by touching the tmp/restart.txt file
    try:
        ftp.mkd('xcomic_backend/tmp')
    except ftplib.error_perm:
        pass
    import io
    restart_file = io.BytesIO(b'')
    ftp.storbinary('STOR xcomic_backend/tmp/restart.txt', restart_file)
    print("Restarted the Python App!")
    
    ftp.quit()
    print("Upload complete!")
