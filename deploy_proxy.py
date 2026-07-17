import ftplib
import io
import time
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

proxy_wsgi = """import sys, os, subprocess, socket, time
import urllib.request
import urllib.error

def is_port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False

def ensure_uvicorn_running(port=47300):
    if not is_port_open(port):
        python_bin = "/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python"
        cmd = [
            python_bin, "-m", "uvicorn", "main:app", 
            "--host", "127.0.0.1", "--port", str(port)
        ]
        # Start in background, write output to uvicorn.log
        subprocess.Popen(
            cmd, 
            stdout=open("uvicorn.log", "a"), 
            stderr=subprocess.STDOUT, 
            close_fds=True
        )
        # Wait up to 5 seconds for startup
        for _ in range(10):
            time.sleep(0.5)
            if is_port_open(port):
                break

def application(environ, start_response):
    PORT = 47300
    ensure_uvicorn_running(PORT)
    
    path = environ.get('PATH_INFO', '/')
    # Prepend /api if missing (due to Apache rewrite prefix stripping)
    if not path.startswith('/api/'):
        if path == '/':
            path = '/api/'
        else:
            path = '/api' + path
            
    query = environ.get('QUERY_STRING', '')
    url = f"http://127.0.0.1:{PORT}{path}"
    if query:
        url += f"?{query}"
        
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Headers
    headers = {}
    for key, val in environ.items():
        if key.startswith('HTTP_'):
            name = key[5:].replace('_', '-').title()
            headers[name] = val
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            name = key.replace('_', '-').title()
            if val:
                headers[name] = val
                
    # Read body
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        content_length = 0
        
    body = None
    if content_length > 0:
        body = environ['wsgi.input'].read(content_length)
        
    # Forward to local Uvicorn
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as res:
            res_headers = []
            for hkey, hval in res.getheaders():
                # Skip hop-by-hop headers if any
                if hkey.lower() not in ('connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'):
                    res_headers.append((hkey, hval))
            
            status = f"{res.status} {res.reason}"
            start_response(status, res_headers)
            return [res.read()]
    except urllib.error.HTTPError as e:
        res_headers = []
        for hkey, hval in e.headers.items():
            res_headers.append((hkey, hval))
        status = f"{e.code} {e.reason}"
        start_response(status, res_headers)
        return [e.read()]
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        # Log to a file for debugging
        with open("proxy_error.log", "a") as err_log:
            err_log.write(f"Proxy error for {url}: {e}\\n")
        return [f"Proxy Error: {e}".encode('utf-8')]
"""

php_script = """<?php
header('Content-Type: text/plain');
function run_command($cmd) {
    echo "=== Running command: $cmd ===\\n";
    $descriptorspec = array(
       0 => array("pipe", "r"),
       1 => array("pipe", "w"),
       2 => array("pipe", "w")
    );
    $process = proc_open($cmd, $descriptorspec, $pipes);
    if (is_resource($process)) {
        $stdout = stream_get_contents($pipes[1]);
        fclose($pipes[1]);
        $stderr = stream_get_contents($pipes[2]);
        fclose($pipes[2]);
        proc_close($process);
        echo "STDOUT:\\n$stdout\\nSTDERR:\\n$stderr\\n";
    } else {
        echo "Failed to start process.\\n";
    }
    echo "======================================\\n\\n";
}

run_command("pkill -9 -f python");
?>
"""

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading proxy passenger_wsgi.py...")
    ftp.cwd('xcomic_backend')
    ftp.storbinary('STOR passenger_wsgi.py', io.BytesIO(proxy_wsgi.encode('utf-8')))
    
    print("Uploading proc_kill.php to xcomic.xyz...")
    ftp.cwd('../xcomic.xyz')
    ftp.storbinary('STOR proc_kill.php', io.BytesIO(php_script.encode('utf-8')))
    
    ftp.quit()
    print("FTP upload completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Request PHP to kill processes
print("Sending GET request to proc_kill.php to kill old processes...")
try:
    r = requests.get("https://xcomic.xyz/proc_kill.php", timeout=20)
    print("Kill response:")
    print(r.text)
except Exception as e:
    print(f"Kill request failed: {e}")

# Delete PHP
try:
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic.xyz')
    ftp.delete('proc_kill.php')
    ftp.quit()
    print("Deleted proc_kill.php")
except Exception as e:
    print(f"Delete error: {e}")

# Wait and request app
print("Waiting 8 seconds for Uvicorn to boot up...")
time.sleep(8)

url = "https://xcomic.xyz/api/ping"
print(f"Sending GET request to {url}...")
try:
    r = requests.get(url, timeout=25)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")
