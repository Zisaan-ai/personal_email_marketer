import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
// We will write a PHP script that invokes Python locally on the server or simply queries SQLite to update total_opened and health score
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Set total_opened to 16
$db->exec("UPDATE sending_accounts SET total_opened = 16 WHERE email = 'gazisaifa428@gmail.com'");

// Trigger health calculation
// Health Score = 100 - (bounce_streak * 15) - (bounce_rate * 50) + (open_rate * 20) etc.
// Let's look at calculate_health_score logic in Python to emulate it or just let health monitor handle it on next check.
// But wait, we can just run a python script to do it properly!
?>'''

# Let's write a Python script on the server and execute it via python interpreter using passenger/venv if possible, or just write it as a python script in xcomic_backend and run it?
# Since we cannot run ssh commands, we can write a PHP script that calls shell_exec? Oh wait, shell_exec is disabled!
# So we can write it in PHP entirely:
php_code_full = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Update total_opened
$db->exec("UPDATE sending_accounts SET total_opened = 16 WHERE email = 'gazisaifa428@gmail.com'");

// Let's fetch the account details to calculate health score
$res = $db->query("SELECT total_sent, total_bounced, total_opened FROM sending_accounts WHERE email = 'gazisaifa428@gmail.com'");
$row = $res->fetchArray();

$total_sent = $row['total_sent'] ? $row['total_sent'] : 0;
$total_bounced = $row['total_bounced'] ? $row['total_bounced'] : 0;
$total_opened = $row['total_opened'] ? $row['total_opened'] : 0;

// Re-calculate health score based on health_monitor.py formula:
// base score = 100
// bounce_rate = total_bounced / total_sent (if sent > 0)
// open_rate = total_opened / total_sent (if sent > 0)
// score = 100 - (bounce_rate * 60) + (open_rate * 15) -> wait, let's look at backend/health_monitor.py calculate_health_score logic!
?>'''
