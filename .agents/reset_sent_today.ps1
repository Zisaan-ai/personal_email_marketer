Add-Type @"
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
public class TrustCerts8 {
    public static void Enable() {
        ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
    }
}
"@
[TrustCerts8]::Enable()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$pair = "terapkco:(3#JCk2Vyn94hY"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [Convert]::ToBase64String($bytes)
$headers = @{ Authorization = "Basic $base64" }

$pythonScript = @"
import sqlite3
db_path = '/home/terapkco/xcomic_backend/sql_app.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Show current state
cur.execute('SELECT id, email, sent_today, daily_limit FROM sending_accounts')
rows = cur.fetchall()
print('Before reset:')
for r in rows:
    print(f'  {r[1]}: sent_today={r[2]}, daily_limit={r[3]}')

# Reset sent_today so campaigns can continue sending
cur.execute('UPDATE sending_accounts SET sent_today = 0')
conn.commit()

cur.execute('SELECT id, email, sent_today, daily_limit FROM sending_accounts')
rows = cur.fetchall()
print('After reset:')
for r in rows:
    print(f'  {r[1]}: sent_today={r[2]}, daily_limit={r[3]}')

conn.close()
print('Done - sent_today reset to 0')
"@

$body = @{
    dir = "/home/terapkco/xcomic_backend"
    filename = "reset_sent_today.py"
    content = $pythonScript
}
$result = Invoke-RestMethod -Uri "https://167.235.11.154:2083/execute/Fileman/save_file_content" -Method POST -Headers $headers -Body $body
Write-Host "Upload result: status=$($result.status) errors=$($result.errors)"
