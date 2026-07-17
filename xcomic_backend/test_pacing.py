
import sys, os, datetime, pytz
sys.path.insert(0, os.path.dirname(__file__))
import database
import warmup_service

BD_TZ = pytz.timezone("Asia/Dhaka")
now_bd = datetime.datetime.now(BD_TZ)
now_utc = datetime.datetime.now(pytz.utc)

last_reset_utc = now_utc.replace(hour=18, minute=0, second=0, microsecond=0)
if now_utc < last_reset_utc:
    last_reset_utc -= datetime.timedelta(days=1)

minutes_passed = (now_utc - last_reset_utc).total_seconds() / 60.0
adjusted_minutes = min(1440.0, minutes_passed + 5.0)
fraction_of_day = adjusted_minutes / 1440.0

print("--- Pacing Info ---")
print("BD Time: " + now_bd.strftime("%Y-%m-%d %H:%M:%S"))
print("Minutes passed since last 18:00 UTC: " + str(minutes_passed))
print("Fraction of day: " + str(fraction_of_day))
print("-------------------")

db = database.SessionLocal()
accounts = db.query(database.SendingAccount).filter(database.SendingAccount.warmup_enabled == True).all()

for acc in accounts:
    daily_target = acc.warmup_daily_limit or 0
    if daily_target <= 0: continue
    
    sent_today = acc.warmup_sent_today or 0
    expected = int(daily_target * fraction_of_day)
    
    status = "SEND NEXT" if sent_today < daily_target and sent_today < expected else "WAIT"
    
    # Simple formatting
    email_pad = acc.email.ljust(35)
    limit_pad = str(daily_target).ljust(5)
    sent_pad = str(sent_today).ljust(5)
    exp_pad = str(expected).ljust(5)
    
    print(email_pad + " | Limit: " + limit_pad + " | Sent: " + sent_pad + " | Expected by now: " + exp_pad + " | Status: " + status)

db.close()
