import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Count accounts
$res = $db->query("SELECT id, email, total_opened FROM sending_accounts");
echo "Accounts:\\n";
while ($row = $res->fetchArray()) {
    echo "  " . $row['id'] . " - " . $row['email'] . " - total_opened: " . $row['total_opened'] . "\\n";
}
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'list_accounts.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/list_accounts.php', verify=False)
print('Output:\\n', r2.text)
unlink_url = 'https://xcomic.xyz/cleanup.php'
# wait we need to delete list_accounts.php
php_cleanup = '''<?php
@unlink('/home/terapkco/xcomic.xyz/list_accounts.php');
@unlink('/home/terapkco/xcomic.xyz/check_opens.php');
echo "Cleaned up list_accounts and check_opens.\\n";
@unlink(__FILE__);
?>'''
data_cleanup = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'cleanup2.php',
    'content': php_cleanup
}
requests.post(url, headers=headers, data=data_cleanup, verify=False)
requests.get('https://xcomic.xyz/cleanup2.php', verify=False)
