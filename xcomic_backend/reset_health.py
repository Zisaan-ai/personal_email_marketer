
import database

db = database.SessionLocal()
db.query(database.SendingAccount).update({'health_score': 100})
db.commit()
db.close()
print('Health scores reset to 100')
