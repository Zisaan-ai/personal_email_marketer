import ftplib
import io
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

php_script = """<?php
header('Content-Type: text/plain');

$db_path = '/home/terapkco/xcomic_backend/sql_app.db';
if (!file_exists($db_path)) {
    echo "DB file does not exist at $db_path\\n";
    exit(1);
}

$db = new SQLite3($db_path);

echo "=== USERS ===\\n";
$res = $db->query("SELECT id, email, is_admin, is_approved, is_email_verified FROM users");
while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
    print_r($row);
}

echo "\\n=== SENDING ACCOUNTS ===\\n";
$res = $db->query("SELECT id, user_id, name, email, is_active, auto_paused, daily_limit, sent_today FROM sending_accounts");
while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
    print_r($row);
}
?>
"""

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading query_db.php to xcomic.xyz...")
    ftp.cwd('xcomic.xyz')
    ftp.storbinary('STOR query_db.php', io.BytesIO(php_script.encode('utf-8')))
    ftp.quit()
    print("FTP upload completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Request PHP
print("Sending GET request to query_db.php...")
url = "https://xcomic.xyz/query_db.php"
try:
    r = requests.get(url, timeout=20)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")

# Delete PHP
try:
    print("Connecting to FTP to delete query_db.php...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic.xyz')
    ftp.delete('query_db.php')
    ftp.quit()
    print("Deleted query_db.php from server.")
except Exception as e:
    print(f"FTP Delete Error: {e}")
