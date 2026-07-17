import ftplib
import io
import time
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

dummy_wsgi = """import sys, os
sys.path.insert(0, os.getcwd())

from fastapi import FastAPI
from a2wsgi import ASGIMiddleware

dummy_app = FastAPI()

@dummy_app.get("/api/ping")
def ping():
    return {"status": "ok", "msg": "Dummy FastAPI works!"}

application = ASGIMiddleware(dummy_app)
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
    
    print("Uploading dummy_wsgi passenger_wsgi.py...")
    ftp.cwd('xcomic_backend')
    ftp.storbinary('STOR passenger_wsgi.py', io.BytesIO(dummy_wsgi.encode('utf-8')))
    
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

# Wait and request dummy app
print("Waiting 5 seconds...")
time.sleep(5)

url = "https://xcomic.xyz/api/ping"
print(f"Sending GET request to {url}...")
try:
    r = requests.get(url, timeout=20)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")
