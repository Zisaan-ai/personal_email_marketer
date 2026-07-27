import os
import sys
import threading

sys.path.insert(0, os.path.dirname(__file__))

from main import app as fastapi_app
from a2wsgi import ASGIMiddleware

_app = None
_lock = threading.Lock()

def application(environ, start_response):
    global _app
    if _app is None:
        with _lock:
            if _app is None:
                _app = ASGIMiddleware(fastapi_app)
    
    # Prepend /api if missing, to match FastAPI routes
    path = environ.get('PATH_INFO', '')
    if not path.startswith('/api'):
        environ['PATH_INFO'] = '/api' + path
        
    return _app(environ, start_response)
