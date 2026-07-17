import sqlite3
conn = sqlite3.connect("C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/xcomic_backend/sql_app.db")
cursor = conn.cursor()
cursor.execute("SELECT id FROM users WHERE email='zmonemrahman@gmail.com'")
admin = cursor.fetchone()
if admin:
    cursor.execute("SELECT email FROM sending_accounts WHERE user_id=?", (admin[0],))
    print("Accounts:", cursor.fetchall())
else:
    print("Admin not found")
