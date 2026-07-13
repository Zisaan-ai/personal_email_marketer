import requests, urllib.parse, base64

creds = 'dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk='
headers = {'Authorization': f'Basic {creds}'}

php_code = '''<?php
$db = new SQLite3('/home/terapkco/xcomic_backend/sql_app.db');

// Set total_opened to 16
$db->exec("UPDATE sending_accounts SET total_opened = 16 WHERE email = 'gazisaifa428@gmail.com'");

// Fetch account details to recalculate health
$res = $db->query("SELECT total_sent, total_bounced, total_opened, total_replied, bounce_streak FROM sending_accounts WHERE email = 'gazisaifa428@gmail.com'");
$row = $res->fetchArray();

$total_sent = $row['total_sent'] ? $row['total_sent'] : 0;
$total_bounced = $row['total_bounced'] ? $row['total_bounced'] : 0;
$total_opened = $row['total_opened'] ? $row['total_opened'] : 0;
$total_replied = $row['total_replied'] ? $row['total_replied'] : 0;
$bounce_streak = $row['bounce_streak'] ? $row['bounce_streak'] : 0;

if ($total_sent > 0) {
    $bounce_rate = $total_bounced / $total_sent;
    $bounce_penalty = $bounce_rate * 80;
    
    $streak_penalty = min($bounce_streak * 5, 30);
    
    $open_rate = $total_opened / $total_sent;
    $open_bonus = min($open_rate * 20, 15);
    
    $reply_rate = $total_replied / $total_sent;
    $reply_bonus = min($reply_rate * 30, 10);
    
    $score = 100 - $bounce_penalty - $streak_penalty + $open_bonus + $reply_bonus;
    $score = max(0, min(100, round($score)));
} else {
    $score = 100;
}

$db->exec("UPDATE sending_accounts SET health_score = $score WHERE email = 'gazisaifa428@gmail.com'");

echo "Updated gazisaifa428@gmail.com: total_opened = 16, health_score = $score\\n";
?>'''

url = 'https://167.235.11.154:2083/execute/Fileman/save_file_content'
data = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'run_backfill.php',
    'content': php_code
}
r = requests.post(url, headers=headers, data=data, verify=False)
r2 = requests.get('https://xcomic.xyz/run_backfill.php', verify=False)
print('Output:\\n', r2.text)

# Cleanup
php_cleanup = '''<?php
@unlink('/home/terapkco/xcomic.xyz/run_backfill.php');
echo "Cleaned up run_backfill.\\n";
@unlink(__FILE__);
?>'''
data_cleanup = {
    'dir': '/home/terapkco/xcomic.xyz',
    'file': 'cleanup3.php',
    'content': php_cleanup
}
requests.post(url, headers=headers, data=data_cleanup, verify=False)
requests.get('https://xcomic.xyz/cleanup3.php', verify=False)
