import ftplib

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    print("Connected.")
    
    directories = []
    ftp.retrlines('LIST', directories.append)
    for d in directories:
        print(d)
        
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
