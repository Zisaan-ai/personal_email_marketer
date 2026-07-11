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
    if path and not path.startswith('/api') and not path.startswith('/unsubscribe') and path != '/':
        environ['PATH_INFO'] = '/api' + (path if path.startswith('/') else '/' + path)

    return _application(environ, start_response)
