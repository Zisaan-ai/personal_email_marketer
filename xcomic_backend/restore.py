import sys
sys.path.append('.')
import database

restore_data = [
  {"email":"gazisaifa428@gmail.com","sent":7,"limit":5,"inc":2},
  {"email":"n04510005@gmail.com","sent":1,"limit":5,"inc":2},
  {"email":"n22824685@gmail.com","sent":2,"limit":5,"inc":2},
  {"email":"n6001084@gmail.com","sent":1,"limit":5,"inc":2},
  {"email":"n19836701@gmail.com","sent":0,"limit":5,"inc":2},
  {"email":"openapkz11@gmail.com","sent":2,"limit":5,"inc":2},
  {"email":"c30229640@gmail.com","sent":1,"limit":5,"inc":2},
  {"email":"willamjosephmiller@gmail.com","sent":3,"limit":5,"inc":2},
  {"email":"williamhenrey2@gmail.com","sent":3,"limit":5,"inc":2},
  {"email":"williamjosephmiller01@gmail.com","sent":2,"limit":5,"inc":2}
]

db = database.SessionLocal()
try:
    for data in restore_data:
        acc = db.query(database.SendingAccount).filter(database.SendingAccount.email == data['email']).first()
        if acc:
            acc.warmup_sent_today = data['sent']
            acc.warmup_daily_limit = data['limit']
    db.commit()
    print("Data restored successfully.")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()
