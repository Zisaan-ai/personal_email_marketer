import os
import sys
import threading

sys.path.insert(0, os.path.dirname(__file__))

from main import app as fastapi_app
from a2wsgi import ASGIMiddleware

_app = None
_lock = threading.Lock()

# Routes that should NOT get /api prefix (they are handled directly by FastAPI)
NO_API_PREFIX_PATHS = ('/unsubscribe/', '/track/', '/static/', '/favicon')

def application(environ, start_response):
    global _app
    if _app is None:
        with _lock:
            if _app is None:
                _app = ASGIMiddleware(fastapi_app)

    path = environ.get('PATH_INFO', '/')

    # Don't prepend /api for paths that are already correct or need no prefix
    if not path.startswith('/api') and not any(path.startswith(p) for p in NO_API_PREFIX_PATHS):
        environ['PATH_INFO'] = '/api' + path

    return _app(environ, start_response)
