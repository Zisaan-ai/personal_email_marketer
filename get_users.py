import sqlite3
conn = sqlite3.connect('sql_app_live.db')
c = conn.cursor()
c.execute("SELECT email, hashed_password FROM users")
print(c.fetchall())
