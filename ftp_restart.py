import ftplib
import io

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend/tmp')
    
    empty_file = io.BytesIO(b"")
    ftp.storbinary('STOR restart.txt', empty_file)
        
    print("Touched tmp/restart.txt")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
