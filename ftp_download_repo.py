import ftplib

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    print("Navigating to personal_email_marketer...")
    ftp.cwd('personal_email_marketer')
    
    print("Downloading database.py from repository...")
    with open(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\repo_database.py", 'wb') as f:
        ftp.retrbinary('RETR xcomic_backend/database.py', f.write)
    print("Downloaded successfully.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
