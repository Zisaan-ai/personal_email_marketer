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

# 1. Verify our new main.py was uploaded (check size)
lines = []
ftp.retrlines('LIST main.py', lines.append)
print("main.py on server:", lines)

# 2. Delete __pycache__ files (compiled bytecode caches)
try:
    ftp.cwd('__pycache__')
    files = ftp.nlst()
    print(f"\nDeleting {len(files)} cached .pyc files...")
    for f in files:
        try:
            ftp.delete(f)
            print(f"  Deleted: {f}")
        except Exception as e:
            print(f"  Could not delete {f}: {e}")
    ftp.cwd('..')
    try:
        ftp.rmd('__pycache__')
        print("Deleted __pycache__ directory")
    except Exception as e:
        print(f"Could not rmdir __pycache__: {e}")
except Exception as e:
    print(f"__pycache__ issue: {e}")

# 3. Touch restart.txt again
ftp.cwd('/xcomic_backend/tmp')
empty = io.BytesIO(b'restart-' + str(hash('restart')).encode())
ftp.storbinary('STOR restart.txt', empty)
print("\nrestart.txt updated - server will reload!")

ftp.quit()
print("Done!")
