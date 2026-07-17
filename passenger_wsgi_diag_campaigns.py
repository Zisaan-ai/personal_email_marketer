import sys
import os
import sqlite3

INTERP = os.path.expanduser("/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.getcwd())

def application(environ, start_response):
    output = []
    try:
        db_path = 'sql_app.db'
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            
            # Check campaigns
            cursor.execute("SELECT id, name, status FROM campaigns")
            campaigns = cursor.fetchall()
            output.append(f"Campaigns in DB: {campaigns}")
            
            # Check processing campaign count
            cursor.execute("SELECT COUNT(*) FROM campaigns WHERE status='processing'")
            proc_count = cursor.fetchone()[0]
            output.append(f"Processing campaigns count: {proc_count}")
            
            conn.close()
    except Exception as e:
        output.append(f"Error: {e}")

    response_text = "\n".join(output)
    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
    return [response_text.encode('utf-8')]
