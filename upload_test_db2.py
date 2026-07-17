import ftplib
import io

host = '167.235.11.154'
user = 'terapkco'
password = '(3#JCk2Vyn94hY'

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    content = b'''import sys
import os
sys.path.append(os.getcwd())
from database import SessionLocal, User, SendingAccount

db = SessionLocal()
admin = db.query(User).filter(User.email == "zmonemrahman@gmail.com").first()
print("Admin ID:", admin.id)
accounts = db.query(SendingAccount).filter(SendingAccount.user_id == str(admin.id)).all()
print("Accounts found by SQLAlchemy:", len(accounts))

accounts2 = db.query(SendingAccount).all()
print("Total accounts found by SQLAlchemy:", len(accounts2))
'''
    ftp.storbinary('STOR test_db2.py', io.BytesIO(content))
    ftp.quit()
    print("Uploaded test_db2.py")
except Exception as e:
    print(f"Error: {e}")
