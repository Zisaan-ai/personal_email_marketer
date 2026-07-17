import time
import requests
import ftplib
import io

print("Waiting 15 seconds for Passenger to reload...")
time.sleep(15)

url1 = "https://xcomic.xyz/api/ping"
print(f"Requesting {url1}...")
try:
    r = requests.get(url1, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Request failed: {e}")

url2 = "https://xcomic.xyz/api/test-db"
print(f"\nRequesting {url2}...")
try:
    r = requests.get(url2, timeout=15)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Request failed: {e}")

# Download wsgi_debug.log via FTP
print("\nDownloading wsgi_debug.log via FTP...")
FTP_HOST = "167.235.11.154"
FTP_USER = "terapkco"
FTP_PASS = "(3#JCk2Vyn94hY"

try:
    ftp = ftplib.FTP(timeout=15)
    ftp.connect(FTP_HOST, 21)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    ftp.cwd('xcomic_backend')
    
    buf = io.BytesIO()
    ftp.retrbinary('RETR wsgi_debug.log', buf.write)
    content = buf.getvalue().decode('utf-8', errors='replace')
    
    print("\n=== wsgi_debug.log content ===")
    print(content)
    print("==============================")
    
    ftp.quit()
except Exception as ftp_err:
    print("Failed to download wsgi_debug.log:", ftp_err)
