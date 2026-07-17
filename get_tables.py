import sqlite3
conn = sqlite3.connect('xcomic_backend/xcomic.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(c.fetchall())
c.execute("SELECT email, password_hash FROM user")
print(c.fetchall())
