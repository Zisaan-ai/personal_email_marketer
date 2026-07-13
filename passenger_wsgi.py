import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Set database path
db_path = os.path.join(BASE_DIR, "sql_app.db")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path}")

# Auto-install missing dependencies on cPanel
try:
    import dns.resolver
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "dnspython"])

# One-time fix: reset all accounts send_window to 0/24 (send 24/7)
try:
    import sqlite3
    _fix_db = os.path.join(BASE_DIR, "sql_app.db")
    if os.path.exists(_fix_db):
        _conn = sqlite3.connect(_fix_db)
        _cur = _conn.cursor()
        _cur.execute("UPDATE sending_accounts SET send_window_start=0, send_window_end=24 WHERE send_window_start != 0 OR send_window_end != 24")
        _conn.commit()
        _conn.close()
except Exception as _e:
    pass

_application = None

def application(environ, start_response):
    global _application
    if _application is None:
        from main import app as asgi_app
        from a2wsgi import ASGIMiddleware
        _application = ASGIMiddleware(asgi_app)
        
    # Fix for Passenger stripping /api prefix
    path = environ.get('PATH_INFO', '')
    
    # If the path is missing /api, and it's not the root or unsubscribe route, prepend /api
    if (path and 
        not path.startswith('/api') and 
        not path.startswith('/unsubscribe/') and 
        not path.startswith('/assets') and 
        not path.startswith('/pixel') and
        path != '/'):
        environ['PATH_INFO'] = '/api' + (path if path.startswith('/') else '/' + path)

    return _application(environ, start_response)
# touch to restart
