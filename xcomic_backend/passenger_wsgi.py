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
import traceback
import datetime

sys.stdout = SafeStream(sys.stdout)
sys.stderr = SafeStream(sys.stderr)

# Set up the path to your FastAPI app directory
sys.path.insert(0, os.path.dirname(__file__))

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wsgi_debug.log')

def log_debug(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{datetime.datetime.now()}] {msg}\n")
    except:
        pass

wsgi_app = None

def application(environ, start_response):
    global wsgi_app
    
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')
    
    try:
        if wsgi_app is None:
            log_debug("Initializing WSGI app...")
            from main import app as fastapi_app
            from a2wsgi import ASGIMiddleware
            wsgi_app = ASGIMiddleware(fastapi_app)
            log_debug("WSGI app initialized successfully")

        # LiteSpeed strips '/api' from PATH_INFO. We need to add it back for FastAPI.
        if not path.startswith('/api'):
            environ['PATH_INFO'] = '/api' + path

        # Log POST requests to auth/token for debugging
        if 'auth/token' in path and method == 'POST':
            log_debug(f"LOGIN REQUEST: {path} | Content-Type: {environ.get('CONTENT_TYPE', 'N/A')} | Content-Length: {environ.get('CONTENT_LENGTH', 'N/A')}")
            
            # Read and re-wrap the input for debugging
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                body = environ['wsgi.input'].read(content_length)
                log_debug(f"LOGIN BODY: {body[:500]}")
                # Re-wrap for consumption by ASGI
                import io
                environ['wsgi.input'] = io.BytesIO(body)
            except Exception as be:
                log_debug(f"BODY READ ERROR: {be}")

        result = wsgi_app(environ, start_response)
        return result

    except Exception as e:
        err = traceback.format_exc()
        log_debug(f"WSGI ERROR on {method} {path}: {err}")
        sys.stderr.write(f"\n[PASSENGER ERROR] {err}\n")
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [err.encode('utf-8')]
