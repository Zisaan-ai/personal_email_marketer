import sys
import os
import time
import traceback

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    output = []
    output.append("=== WSGI dispatch diagnostics starting ===")
    
    try:
        t0 = time.time()
        from main import app as fastapi_app
        from a2wsgi import ASGIMiddleware
        output.append(f"Imported main & a2wsgi in {time.time() - t0:.4f}s")
        
        # Instantiate the middleware
        t1 = time.time()
        wsgi_app = ASGIMiddleware(fastapi_app)
        output.append(f"Created ASGIMiddleware in {time.time() - t1:.4f}s")
        
        # Mock environment for a simple /api/settings/all request
        mock_environ = environ.copy()
        mock_environ['PATH_INFO'] = '/api/settings/all'
        mock_environ['REQUEST_METHOD'] = 'GET'
        
        # We need a start_response interceptor to see what ASGI returns
        headers = []
        status_code = []
        
        def mock_start_response(s, h, exc_info=None):
            status_code.append(s)
            headers.extend(h)
            return lambda d: None
            
        t2 = time.time()
        output.append("\nInvoking wsgi_app with mock request...")
        
        # Execute the request
        res = wsgi_app(mock_environ, mock_start_response)
        res_list = list(res)
        
        output.append(f"Request finished in {time.time() - t2:.4f}s")
        output.append(f"Status: {status_code}")
        output.append(f"Headers: {headers}")
        output.append(f"Response: {[r.decode('utf-8', errors='ignore') for r in res_list]}")
        
    except Exception as e:
        output.append(f"\nFailed during mock request: {e}")
        output.append(traceback.format_exc())
        
    return ["\n".join(output).encode('utf-8')]
