
import sys
sys.path.append('.')
import database
import warmup_service

db = database.SessionLocal()
accounts = db.query(database.SendingAccount).filter(database.SendingAccount.warmup_enabled == True).all()
print('Before reset:')
for acc in accounts:
    print(f'Email: {acc.email}, Sent Today: {acc.warmup_sent_today}, Daily Limit: {acc.warmup_daily_limit}, Increment: {acc.warmup_increment_per_day}')

warmup_service.reset_daily_warmup_counts()
print('-' * 20)

accounts = db.query(database.SendingAccount).filter(database.SendingAccount.warmup_enabled == True).all()
print('After reset:')
for acc in accounts:
    print(f'Email: {acc.email}, Sent Today: {acc.warmup_sent_today}, Daily Limit: {acc.warmup_daily_limit}, Increment: {acc.warmup_increment_per_day}')
