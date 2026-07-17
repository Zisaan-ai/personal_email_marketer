import os
import sys

def application(environ, start_response):
    try:
        # LiteSpeed strips '/api' from PATH_INFO. We need to add it back for FastAPI.
        path = environ.get('PATH_INFO', '')
        if not path.startswith('/api'):
            environ['PATH_INFO'] = '/api' + path
            
        # Set up the path to your FastAPI app directory
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Import the FastAPI app
        from main import app as fastapi_app
        
        from a2wsgi import ASGIMiddleware
        return ASGIMiddleware(fastapi_app)(environ, start_response)
        
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [err.encode('utf-8')]
