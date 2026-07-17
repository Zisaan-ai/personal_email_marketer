import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sql_app.db")

try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(campaigns)")
    cols = cur.fetchall()
    print([c[1] for c in cols])
    conn.close()
except Exception as e:
    print("Error:", e)
