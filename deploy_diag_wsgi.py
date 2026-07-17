import ftplib
import io

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    with open(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\ftp_check_live_accounts.py", "rb") as f:
        ftp.storbinary('STOR passenger_wsgi.py', f)
        
    print("Uploaded passenger_wsgi.py")
    
    ftp.cwd('../tmp')
    ftp.storbinary('STOR restart.txt', io.BytesIO(b''))
    print("Restarted passenger")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
