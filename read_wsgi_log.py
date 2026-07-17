import ftplib
import io

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic_backend')
    
    # Retrieve wsgi_debug.log
    buf = io.BytesIO()
    ftp.retrbinary('RETR wsgi_debug.log', buf.write)
    content = buf.getvalue().decode('utf-8', errors='replace')
    
    print("\n=== wsgi_debug.log content ===")
    lines = content.splitlines()
    for line in lines[-100:]:
        print(line)
    print("==============================")
    
    ftp.quit()
except Exception as e:
    print(f"Error: {e}")
