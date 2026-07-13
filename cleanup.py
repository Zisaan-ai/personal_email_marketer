import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
@unlink('/home/terapkco/xcomic.xyz/tail.php');
@unlink('/home/terapkco/xcomic.xyz/check_db.php');
@unlink('/home/terapkco/xcomic.xyz/check_db2.php');
@unlink('/home/terapkco/xcomic.xyz/sync_db.php');
@unlink('/home/terapkco/xcomic.xyz/dbtest.php');
echo "Deleted debug files.\\n";
@unlink(__FILE__);
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'cleanup.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/cleanup.php', verify=False)
print('Cleanup:', r2.text)
