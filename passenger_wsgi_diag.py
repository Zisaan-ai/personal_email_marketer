import sys
import os
import sqlite3
import traceback

INTERP = os.path.expanduser("/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.getcwd())

def application(environ, start_response):
    output = []
    output.append(f"Python Executable: {sys.executable}")
    output.append(f"Python Version: {sys.version}")
    output.append(f"Current Directory: {os.getcwd()}")
    
    # 1. Check imports
    for lib in ['a2wsgi', 'uvicorn', 'asgiref', 'fastapi', 'sqlalchemy']:
        try:
            __import__(lib)
            output.append(f"Import {lib}: SUCCESS")
        except ImportError as e:
            output.append(f"Import {lib}: FAILED ({e})")
            
    # 2. Check Database
    try:
        db_path = 'sql_app.db'
        output.append(f"Database file exists: {os.path.exists(db_path)}")
        if os.path.exists(db_path):
            output.append(f"Database file size: {os.path.getsize(db_path)} bytes")
            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            
            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            output.append(f"Tables: {tables}")
            
            # Query users
            if 'users' in tables:
                cursor.execute("SELECT id, email, is_admin, is_approved FROM users")
                users = cursor.fetchall()
                output.append(f"Users in DB: {users}")
            else:
                output.append("Table 'users' does not exist")
                
            # Query sending accounts
            if 'sending_accounts' in tables:
                cursor.execute("SELECT id, user_id, email, is_active, auto_paused, health_score FROM sending_accounts")
                accounts = cursor.fetchall()
                output.append(f"Sending Accounts in DB ({len(accounts)}): {accounts}")
            else:
                output.append("Table 'sending_accounts' does not exist")
                
            conn.close()
    except Exception as e:
        output.append(f"Database error: {e}")
        output.append(traceback.format_exc())

    response_text = "\n".join(output)
    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
    return [response_text.encode('utf-8')]
