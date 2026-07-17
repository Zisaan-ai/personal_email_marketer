import ftplib
import io
import time
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

php_script = """<?php
header('Content-Type: text/plain');
echo "Disable functions: " . ini_get('disable_functions') . "\\n\\n";
foreach (array('exec', 'system', 'passthru', 'shell_exec', 'proc_open', 'popen') as $func) {
    echo "$func is " . (function_exists($func) ? "exists" : "not exists") . "\\n";
}
?>
"""

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading probe_functions.php to xcomic.xyz...")
    ftp.cwd('xcomic.xyz')
    ftp.storbinary('STOR probe_functions.php', io.BytesIO(php_script.encode('utf-8')))
    ftp.quit()
    print("FTP upload completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Request PHP
print("Sending GET request to probe_functions.php...")
url = "https://xcomic.xyz/probe_functions.php"
try:
    r = requests.get(url, timeout=20)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")

# Delete PHP
try:
    print("Connecting to FTP to delete probe_functions.php...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic.xyz')
    ftp.delete('probe_functions.php')
    ftp.quit()
    print("Deleted probe_functions.php from server.")
except Exception as e:
    print(f"FTP Delete Error: {e}")
