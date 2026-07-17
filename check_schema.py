import sqlite3
conn = sqlite3.connect(r"C:\Users\higan\.gemini\antigravity\scratch\xcomic_sync\xcomic_backend\sql_app.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(sending_accounts)")
for col in cursor.fetchall():
    print(col[1])
conn.close()
