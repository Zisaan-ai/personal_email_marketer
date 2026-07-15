import ftplib, io, sqlite3, tempfile, os, datetime, pytz

# 1. Download DB
ftp = ftplib.FTP('terapk.com')
ftp.login('terapkco', '(3#JCk2Vyn94hY')
ftp.cwd('xcomic_backend')
buf = io.BytesIO()
ftp.retrbinary('RETR sql_app.db', buf.write)
ftp.quit()

with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
    f.write(buf.getvalue())
    tmp = f.name

# 2. Run Pacing Logic
BD_TZ = pytz.timezone("Asia/Dhaka")
now_bd = datetime.datetime.now(BD_TZ)
now_utc = datetime.datetime.now(pytz.utc)

last_reset_utc = now_utc.replace(hour=18, minute=0, second=0, microsecond=0)
if now_utc < last_reset_utc:
    last_reset_utc -= datetime.timedelta(days=1)

minutes_passed = (now_utc - last_reset_utc).total_seconds() / 60.0
adjusted_minutes = min(1440.0, minutes_passed + 5.0)
fraction_of_day = adjusted_minutes / 1440.0

print("--- LIVE PACING STATUS ---")
print("BD Time: " + now_bd.strftime("%Y-%m-%d %H:%M:%S"))
print(f"Minutes passed since 18:00 UTC: {minutes_passed:.2f}")
print(f"Fraction of day: {fraction_of_day:.4f}")
print("-" * 80)

conn = sqlite3.connect(tmp)
cur = conn.cursor()
cur.execute('SELECT email, warmup_daily_limit, warmup_sent_today FROM sending_accounts WHERE warmup_enabled=1')

for row in cur.fetchall():
    email = row[0]
    daily_target = row[1] or 0
    sent_today = row[2] or 0
    
    if daily_target <= 0: continue
    
    expected = int(daily_target * fraction_of_day)
    status = "SEND NEXT (WILL SEND NOW)" if sent_today < daily_target and sent_today < expected else "WAITING (ON PACE)"
    
    print(f"{email:<35} | Limit: {daily_target:<4} | Sent: {sent_today:<4} | Expected by now: {expected:<4} | {status}")

conn.close()
os.unlink(tmp)
