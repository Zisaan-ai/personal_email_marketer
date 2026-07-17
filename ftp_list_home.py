import ftplib

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    directories = []
    ftp.retrlines('LIST -a', directories.append)
    for d in directories:
        print(d)
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
