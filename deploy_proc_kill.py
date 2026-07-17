import ftplib
import io
import time
import requests

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"

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

run_command("ps -u terapkco -f");
run_command("pkill -9 -f python");
run_command("pkill -9 -f uvicorn");
run_command("ps -u terapkco -f");
?>
"""

try:
    print("Connecting to FTP...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    
    print("Uploading proc_kill.php to xcomic.xyz...")
    ftp.cwd('xcomic.xyz')
    ftp.storbinary('STOR proc_kill.php', io.BytesIO(php_script.encode('utf-8')))
    ftp.quit()
    print("FTP upload completed.")
except Exception as e:
    print(f"FTP Error: {e}")

# Request PHP
print("Sending GET request to proc_kill.php...")
url = "https://xcomic.xyz/proc_kill.php"
try:
    r = requests.get(url, timeout=30)
    print(f"Status Code: {r.status_code}")
    print("Response Content:")
    print(r.text)
except Exception as e:
    print(f"HTTP Request failed: {e}")

# Delete PHP
try:
    print("Connecting to FTP to delete proc_kill.php...")
    ftp = ftplib.FTP(host, user, password, timeout=15)
    ftp.set_pasv(True)
    ftp.cwd('xcomic.xyz')
    ftp.delete('proc_kill.php')
    ftp.quit()
    print("Deleted proc_kill.php from server.")
except Exception as e:
    print(f"FTP Delete Error: {e}")
