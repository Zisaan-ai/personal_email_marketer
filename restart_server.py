import ftplib
import io

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

print("Connecting...")
ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

ftp.cwd('xcomic_backend')

# Touch tmp/restart.txt to restart Passenger app
try:
    ftp.cwd('tmp')
    print("In tmp dir, creating restart.txt...")
    empty = io.BytesIO(b'')
    ftp.storbinary('STOR restart.txt', empty)
    print("restart.txt created - server will restart!")
except Exception as e:
    print(f"tmp dir error: {e}")
    # Try creating tmp first
    try:
        ftp.cwd('/xcomic_backend')
        ftp.mkd('tmp')
        ftp.cwd('tmp')
        empty = io.BytesIO(b'')
        ftp.storbinary('STOR restart.txt', empty)
        print("Created tmp/restart.txt - server will restart!")
    except Exception as e2:
        print(f"Failed: {e2}")

ftp.quit()
