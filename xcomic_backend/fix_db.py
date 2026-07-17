import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sql_app.db")

try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("ALTER TABLE campaigns ADD COLUMN name VARCHAR")
    conn.commit()
    conn.close()
    print("Successfully added name column to campaigns")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column already exists.")
    else:
        print("OperationalError:", e)
except Exception as e:
    print("Error:", e)
