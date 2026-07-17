import sys, os
import traceback
import logging

INTERP = os.path.expanduser("/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.getcwd())

# Setup logging to a file we can inspect
logging.basicConfig(
    filename='wsgi_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

logging.info("passenger_wsgi.py: Importing main.py...")
try:
    from main import app as fastapi_app
    logging.info("passenger_wsgi.py: Import main SUCCESS")
except Exception as e:
    logging.error(f"passenger_wsgi.py: Import main FAILED: {e}")
    logging.error(traceback.format_exc())
    raise

try:
    from a2wsgi import ASGIMiddleware
    # Wrap it
    asgi_middleware = ASGIMiddleware(fastapi_app)
    logging.info("passenger_wsgi.py: Created ASGIMiddleware")
except Exception as e:
    logging.error(f"passenger_wsgi.py: Failed to create ASGIMiddleware: {e}")
    logging.error(traceback.format_exc())
    raise

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    logging.info(f"--- Request Start: {environ.get('REQUEST_METHOD')} {path} ---")
    
    # Custom start_response wrapper to log response status
    def logged_start_response(status, headers, exc_info=None):
        logging.info(f"Request response start: status={status}")
        return start_response(status, headers, exc_info)
        
    try:
        # Call ASGIMiddleware
        result = asgi_middleware(environ, logged_start_response)
        logging.info(f"Request finished successfully: {path}")
        return result
    except Exception as e:
        logging.error(f"Exception during request {path}: {e}")
        logging.error(traceback.format_exc())
        logged_start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f"WSGI Request Error: {e}\n{traceback.format_exc()}".encode('utf-8')]
