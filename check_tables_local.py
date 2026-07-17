import sqlite3
conn = sqlite3.connect(r'C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\sql_app.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])
conn.close()
