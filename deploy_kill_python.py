import ftplib
import io
import time
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

php_script = """<?php
header('Content-Type: text/plain');
echo "Running ps...\\n";
echo shell_exec("ps aux | grep python");
echo "\\nKilling python...\\n";
echo shell_exec("pkill -9 -u terapkco python");
echo shell_exec("pkill -9 -u terapkco python3.11");
echo "\\nAfter kill ps...\\n";
echo shell_exec("ps aux | grep python");
?>
"""

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading kill_python.php to xcomic.xyz...")
    ftp.cwd('xcomic.xyz')
    ftp.storbinary('STOR kill_python.php', io.BytesIO(php_script.encode('utf-8')))
    ftp.quit()
    print("FTP upload completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Wait and request PHP
print("Sending GET request to kill_python.php...")
url = "https://xcomic.xyz/kill_python.php"
try:
    r = requests.get(url, timeout=20)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")

# Delete PHP
try:
    print("Connecting to FTP to delete kill_python.php...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic.xyz')
    ftp.delete('kill_python.php')
    ftp.quit()
    print("Deleted kill_python.php from server.")
except Exception as e:
    print(f"FTP Delete Error: {e}")
