class SafeStream:
    def __init__(self, original):
        self.original = original
    def write(self, data):
        try:
            if self.original:
                self.original.write(data)
                self.original.flush()
        except Exception:
            pass
    def flush(self):
        try:
            if self.original:
                self.original.flush()
        except Exception:
            pass
    def __getattr__(self, attr):
        return getattr(self.original, attr)

import sys
import os

sys.stdout = SafeStream(sys.stdout)
sys.stderr = SafeStream(sys.stderr)

# Set up the path to your FastAPI app directory
sys.path.insert(0, os.path.dirname(__file__))

wsgi_app = None

def application(environ, start_response):
    global wsgi_app
    if wsgi_app is None:
        # Import and instantiate lazily INSIDE the worker process post-fork
        from main import app as fastapi_app
        from a2wsgi import ASGIMiddleware
        wsgi_app = ASGIMiddleware(fastapi_app)

    try:
        # LiteSpeed strips '/api' from PATH_INFO. We need to add it back for FastAPI.
        path = environ.get('PATH_INFO', '')
        if not path.startswith('/api'):
            environ['PATH_INFO'] = '/api' + path

        return wsgi_app(environ, start_response)

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [err.encode('utf-8')]
