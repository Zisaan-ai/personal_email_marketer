import os
import sys
import ftplib
import time

# FTP Configurations
FTP_HOST = "terapk.com"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
FTP_FRONTEND_REMOTE = "/xcomic.xyz"
FTP_BACKEND_REMOTE = "/xcomic_backend"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

FILES_TO_UPLOAD = [
    (os.path.join(ROOT_DIR, "xcomic.xyz", "index.html"), FTP_FRONTEND_REMOTE + "/index.html"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "app.js"), FTP_FRONTEND_REMOTE + "/assets/app.js"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "sending_accounts.js"), FTP_FRONTEND_REMOTE + "/assets/sending_accounts.js"),
    (os.path.join(ROOT_DIR, "xcomic.xyz", "assets", "support_patch.js"), FTP_FRONTEND_REMOTE + "/assets/support_patch.js"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "main.py"), FTP_BACKEND_REMOTE + "/main.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "database.py"), FTP_BACKEND_REMOTE + "/database.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "bulk_campaign_sender.py"), FTP_BACKEND_REMOTE + "/bulk_campaign_sender.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "bounce_processor.py"), FTP_BACKEND_REMOTE + "/bounce_processor.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "payment.py"), FTP_BACKEND_REMOTE + "/payment.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "payment_lemonsqueezy.py"), FTP_BACKEND_REMOTE + "/payment_lemonsqueezy.py"),
    (os.path.join(ROOT_DIR, "xcomic_backend", "lemonsqueezy_config.json"), FTP_BACKEND_REMOTE + "/lemonsqueezy_config.json"),
]

def upload_with_retry(local_path, remote_path, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Uploading {local_path} to {remote_path} (Attempt {attempt}/{max_attempts})...")
            ftp = ftplib.FTP(timeout=60)
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASS)
            
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_path}", f)
            
            ftp.quit()
            print(f"  Successfully uploaded {local_path}")
            return True
        except Exception as e:
            print(f"  Warning: Attempt {attempt} failed: {e}")
            time.sleep(2)
    print(f"  Error: Failed to upload {local_path} after {max_attempts} attempts.")
    return False

def trigger_app_restart():
    print("\n--- Triggering Live App Restart ---")
    restart_local_path = os.path.join(ROOT_DIR, "restart.txt")
    with open(restart_local_path, "w") as f:
        f.write(str(time.time()))
    upload_with_retry(restart_local_path, FTP_BACKEND_REMOTE + "/tmp/restart.txt")
    upload_with_retry(restart_local_path, FTP_BACKEND_REMOTE + "/restart.txt")
    if os.path.exists(restart_local_path):
        os.remove(restart_local_path)
    print("Application restart triggered on live server.")

def main():
    print("Starting custom robust deploy for changed files...")
    for local, remote in FILES_TO_UPLOAD:
        if os.path.exists(local):
            upload_with_retry(local, remote)
        else:
            print(f"File not found: {local}")
    
    trigger_app_restart()
    print("Done!")

if __name__ == "__main__":
    main()
