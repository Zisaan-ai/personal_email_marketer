import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))
os.environ.setdefault('DATABASE_URL', f"sqlite:///{os.path.join(BACKEND_DIR, 'sql_app.db')}")

import database
from email_service import send_single_email

db = database.SessionLocal()
acc = db.query(database.SendingAccount).filter(database.SendingAccount.email == 'zmonemrahman@gmail.com').first()
if acc:
    try:
        res = send_single_email("Test subject", "Test body", "zisan7619@gmail.com", account=acc)
        print("Result:", res)
    except Exception as e:
        print("Exception:", e)
else:
    print("Account not found")
