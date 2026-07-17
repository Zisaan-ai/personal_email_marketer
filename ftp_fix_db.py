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
"""

with open("fix_db.py", "w") as f:
    f.write(script)

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=10)
    ftp.cwd('xcomic_backend')
    
    with open("fix_db.py", "rb") as f:
        ftp.storbinary('STOR fix_db.py', f)
        
    print("Uploaded fix_db.py")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ftp.quit()
    except:
        pass
