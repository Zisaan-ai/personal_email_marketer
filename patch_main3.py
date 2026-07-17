import ftplib
import os

FTP_HOST = "194.164.77.235"
FTP_USER = "terapkco"
FTP_PASS = "Eftakhar@1234"

print("Connecting to FTP...")
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
print("Connected.")

ftp.cwd('xcomic_backend')

with open('main.py', 'wb') as f:
    ftp.retrbinary('RETR main.py', f.write)

with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'accounts = db.query(database.SendingAccount).filter(database.SendingAccount.user_id == str(current_user.id)).all()' in line:
        print(f"Found line at {i}")
        # Insert test endpoint right before it
        lines.insert(i+1, "    print(f'DEBUG: Found {len(accounts)} accounts for user {current_user.email}', flush=True)\n")
        break

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

with open('main.py', 'rb') as f:
    ftp.storbinary('STOR main.py', f)

# Restart passenger
import io
ftp.storbinary("STOR tmp/restart.txt", io.BytesIO(b""))

ftp.quit()
print("Patched and restarted.")
