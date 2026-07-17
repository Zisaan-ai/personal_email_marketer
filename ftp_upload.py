import ftplib
import os

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"
LOCAL_FILE = "main_live.py"
REMOTE_PATH = "/home/terapkco/xcomic_backend/main_live.py"

def upload_file():
    print("Connecting to FTP...")
    
    # Try different FTP modes
    for mode in ['passive_true', 'passive_false', 'ftps']:
        try:
            if mode == 'ftps':
                ftp = ftplib.FTP_TLS(timeout=30)
                ftp.connect(FTP_HOST, 21)
                ftp.login(FTP_USER, FTP_PASS)
                ftp.prot_p()
                ftp.set_pasv(True)
            else:
                ftp = ftplib.FTP(timeout=30)
                ftp.connect(FTP_HOST, 21)
                ftp.login(FTP_USER, FTP_PASS)
                ftp.set_pasv(mode == 'passive_true')
            
            print(f"Connected! Mode: {mode}")
            print("Welcome:", ftp.getwelcome())
            
            # Change to target directory
            ftp.cwd('/home/terapkco/xcomic_backend')
            print("Current dir:", ftp.pwd())
            
            # Upload file
            with open(LOCAL_FILE, 'rb') as f:
                ftp.storbinary(f'STOR main_live.py', f)
            
            print(f"SUCCESS! Uploaded via {mode}")
            ftp.quit()
            return True
            
        except Exception as e:
            print(f"Mode {mode} failed: {e}")
            try:
                ftp.quit()
            except:
                pass
    
    return False

if __name__ == '__main__':
    success = upload_file()
    if not success:
        print("\nAll FTP modes failed!")
