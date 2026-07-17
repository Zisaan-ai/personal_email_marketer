import ftplib
import os
import sys

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
REMOTE_DIR = "/xcomic_backend"

FILES_TO_UPLOAD = [
    ("xcomic_backend/database.py", "database.py"),
    ("xcomic_backend/health_monitor.py", "health_monitor.py"),
    ("xcomic_backend/main.py", "main.py"),
    ("xcomic_backend/warmup_service.py", "warmup_service.py"),
    ("xcomic_backend/main_live.py", "main_live.py")
]

def upload_files():
    print("Connecting to FTP...")
    ftp = ftplib.FTP_TLS(timeout=30)
    try:
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.prot_p()
        ftp.set_pasv(True)
        print("Connected!")
        
        for local, remote in FILES_TO_UPLOAD:
            if not os.path.exists(local):
                print(f"Skipping {local} (not found)")
                continue
                
            remote_path = f"{REMOTE_DIR}/{remote}"
            remote_folder = os.path.dirname(remote_path)
            
            try:
                ftp.cwd(remote_folder)
            except:
                pass
                
            print(f"Uploading {local} to {remote_path}...")
            with open(local, 'rb') as f:
                ftp.storbinary(f'STOR {os.path.basename(remote_path)}', f)
                
        # restart the app via tmp/restart.txt
        ftp.cwd(REMOTE_DIR + "/tmp")
        with open("restart.txt", 'w') as f:
            f.write("restart")
        with open("restart.txt", 'rb') as f:
            ftp.storbinary(f'STOR restart.txt', f)
        print("Uploaded restart.txt")
        
        print("SUCCESS! Uploaded all files.")
        ftp.quit()
        return True
    except Exception as e:
        print(f"FTP failed: {e}")
        return False

if __name__ == '__main__':
    upload_files()
