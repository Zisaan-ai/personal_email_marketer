import ftplib

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

script = """import sqlite3
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
"""

with open("check_db.py", "w") as f:
    f.write(script)

try:
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    with open("check_db.py", "rb") as f:
        ftp.storbinary('STOR check_db.py', f)
    print("Uploaded check_db.py")
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
