
import os
import sys

# Add current directory to path
cwd = os.getcwd()
sys.path.append(cwd)

# Ensure Uvicorn runs in background
def ensure_uvicorn_running():
    import os
    os.system('killall python')
    os.system('pkill -f uvicorn')
    
    # Check if uvicorn is running on the port
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 47300))
        s.close()
        
    except:
        pass
        
    os.system('nohup python -m uvicorn main:app --host 127.0.0.1 --port 47300 --workers 1 > uvicorn.log 2>&1 &')

# The actual WSGI application is just a proxy
def application(environ, start_response):
    ensure_uvicorn_running()
    
    import urllib.request
    
    # Extract path and query string
    path = environ.get('PATH_INFO', '/')
    if not path.startswith('/api'):
        path = '/api' + (path if path.startswith('/') else '/' + path)
        
    qs = environ.get('QUERY_STRING', '')
    if qs:
        path += '?' + qs
        
    url = 'http://127.0.0.1:47300' + path
    
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Extract headers
    headers = {}
    for key, value in environ.items():
        if key.startswith('HTTP_'):
            header_name = key[5:].replace('_', '-').title()
            headers[header_name] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH') and value:
            header_name = key.replace('_', '-').title()
            headers[header_name] = value
            
    # Read body
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError, TypeError):
        content_length = 0
        
    body = None
    if content_length > 0:
        body = environ['wsgi.input'].read(content_length)
        
    # Make request to Uvicorn
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        status_code = resp.getcode()
        # urllib doesn't give text descriptions easily, so map basic ones
        status = f"{status_code} OK"
        if status_code != 200:
            status = f"{status_code} Status"
            
        resp_headers = [(k, v) for k, v in resp.info().items() if k.lower() != 'transfer-encoding']
        
        start_response(status, resp_headers)
        return [resp.read()]
        
    except urllib.error.HTTPError as e:
        status = f"{e.code} Error"
        resp_headers = [(k, v) for k, v in e.info().items() if k.lower() != 'transfer-encoding']
        start_response(status, resp_headers)
        return [e.read()]
        
    except Exception as e:
        start_response('502 Bad Gateway', [('Content-Type', 'text/plain')])
        return [str(e).encode('utf-8')]
