import ftplib

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    print("Connected.")
    
    print("Navigating to xcomic_backend...")
    ftp.cwd('xcomic_backend')
    
    # Download the live database
    print("Downloading live sql_app.db...")
    with open(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\sql_app.db", 'wb') as f:
        ftp.retrbinary('RETR sql_app.db', f.write)
    print("Database downloaded successfully.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
        print("Disconnected.")
    except:
        pass
