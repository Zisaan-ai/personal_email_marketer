import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Sync sent counts for all campaigns
$db->exec("UPDATE campaigns SET sent_count = (SELECT COUNT(*) FROM campaign_leads WHERE campaign_leads.campaign_id = campaigns.id AND campaign_leads.status = 'sent')");

echo "Sync complete!\\n";
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'sync_db.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/sync_db.php', verify=False)
print('Output:\\n', r2.text)
