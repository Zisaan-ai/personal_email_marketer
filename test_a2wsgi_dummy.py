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

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading dummy_wsgi passenger_wsgi.py...")
    ftp.cwd('xcomic_backend')
    ftp.storbinary('STOR passenger_wsgi.py', io.BytesIO(dummy_wsgi.encode('utf-8')))
        
    print("Restarting Passenger...")
    ftp.cwd('../tmp')
    ftp.storbinary('STOR restart.txt', io.BytesIO(b''))
    ftp.quit()
    print("FTP upload and restart completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Wait and request
print("Waiting for Passenger to reload (10 seconds)...")
time.sleep(10)

url = "https://xcomic.xyz/api/ping"
print(f"Sending GET request to {url}...")
try:
    r = requests.get(url, timeout=15)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")
