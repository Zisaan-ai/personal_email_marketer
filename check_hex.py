import sqlite3
conn = sqlite3.connect('C:/Users/higan/.gemini/antigravity/scratch/xcomic_sync/xcomic_backend/sql_app.db')
c = conn.cursor()
c.execute("SELECT id, hex(id) FROM users WHERE email='zmonemrahman@gmail.com'")
print('User ID:', c.fetchone())
c.execute("SELECT user_id, hex(user_id) FROM sending_accounts LIMIT 1")
print('Sending Account user_id:', c.fetchone())
conn.close()
