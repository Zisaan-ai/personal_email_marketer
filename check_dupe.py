import sqlite3
conn = sqlite3.connect('C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/xcomic_backend/sql_app.db')
c = conn.cursor()
c.execute("SELECT id, email FROM users WHERE email='zmonemrahman@gmail.com'")
print("Users:", c.fetchall())
conn.close()
