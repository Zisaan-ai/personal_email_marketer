import ftplib

FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

ftp = ftplib.FTP(timeout=30)
ftp.connect(FTP_HOST, 21)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)

print("Root dir:", ftp.pwd())
print("\nRoot listing:")
ftp.retrlines('LIST')

# Try going up
try:
    ftp.cwd('xcomic_backend')
    print("\nFound xcomic_backend!")
    ftp.retrlines('LIST')
except Exception as e:
    print("xcomic_backend not in root:", e)

# Try common paths
for path in ['public_html', 'www', 'xcomic.xyz', 'xcomic_backend', 'backend']:
    try:
        ftp.cwd('/')
        ftp.cwd(path)
        print(f"\n=== /{path} contents ===")
        ftp.retrlines('LIST')
    except Exception as e:
        print(f"/{path}: {e}")

ftp.quit()
