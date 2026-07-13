import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');
$res = $db->query("SELECT id, status, sent_count FROM campaigns ORDER BY created_at DESC LIMIT 5");
while ($row = $res->fetchArray()) {
    echo "Campaign: " . $row['id'] . " - " . $row['status'] . " - sent_count: " . $row['sent_count'] . "\\n";
    $res2 = $db->query("SELECT status, COUNT(*) as c FROM campaign_leads WHERE campaign_id = '" . $row['id'] . "' GROUP BY status");
    while ($row2 = $res2->fetchArray()) {
        echo "  Lead status: " . $row2['status'] . " = " . $row2['c'] . "\\n";
    }
}
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'check_db.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/check_db.php', verify=False)
print('Output:\\n', r2.text)
