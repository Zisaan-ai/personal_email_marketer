import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Count events
$res = $db->query("SELECT event_type, COUNT(*) as c FROM tracking_logs GROUP BY event_type");
echo "Tracking Logs:\\n";
while ($row = $res->fetchArray()) {
    echo "  " . $row['event_type'] . " = " . $row['c'] . "\\n";
}

// Check some campaign lead statuses
$res2 = $db->query("SELECT status, COUNT(*) as c FROM campaign_leads GROUP BY status");
echo "Campaign Leads:\\n";
while ($row2 = $res2->fetchArray()) {
    echo "  " . $row2['status'] . " = " . $row2['c'] . "\\n";
}
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'check_opens.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/check_opens.php', verify=False)
print('Output:\\n', r2.text)
