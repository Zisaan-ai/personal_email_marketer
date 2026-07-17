import sys
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
